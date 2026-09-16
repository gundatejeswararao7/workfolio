from datetime import datetime, timedelta
import hashlib
import secrets

from sqlalchemy import select
from sqlalchemy.orm import Session

from .config import settings
from .models import Notification, OTPRecord, User, Work


def gmail(value: str) -> str:
    return value.strip().lower()


def generate_otp(db: Session, email: str, purpose: str) -> str:
    code = f"{secrets.randbelow(1_000_000):06d}"
    record = OTPRecord(
        email=gmail(email),
        purpose=purpose,
        otp_hash=hashlib.sha256(code.encode()).hexdigest(),
        expires_at=datetime.utcnow() + timedelta(seconds=settings.otp_expiry_seconds),
    )
    db.add(record)
    db.commit()
    print(f"[Loopline development OTP] {email} / {purpose}: {code}")
    return code


def verify_otp(db: Session, email: str, code: str, purpose: str) -> bool:
    record = db.scalar(
        select(OTPRecord)
        .where(OTPRecord.email == gmail(email), OTPRecord.purpose == purpose, OTPRecord.verified.is_(False))
        .order_by(OTPRecord.created_at.desc())
    )
    if not record:
        record = db.scalar(
            select(OTPRecord)
            .where(OTPRecord.email == gmail(email), OTPRecord.purpose == purpose, OTPRecord.verified.is_(True))
            .order_by(OTPRecord.created_at.desc())
        )
        if record and record.expires_at >= datetime.utcnow() and hashlib.sha256(code.encode()).hexdigest() == record.otp_hash:
            return True
        return False
    if record.expires_at < datetime.utcnow() or record.attempts >= 5:
        return False
    record.attempts += 1
    valid = hashlib.sha256(code.encode()).hexdigest() == record.otp_hash
    if valid:
        record.verified = True
    db.commit()
    return valid


def notify(db: Session, user_id: int, notification_type: str, title: str, body: str) -> Notification:
    item = Notification(user_id=user_id, type=notification_type, title=title, body=body)
    db.add(item)
    return item


def update_overdue(db: Session, works: list[Work]) -> None:
    now = datetime.utcnow()
    changed = False
    for work in works:
        if work.due_at and work.due_at < now and work.status in {"ASSIGNED", "IN_PROGRESS"}:
            work.status = "OVERDUE"
            work.is_overdue = True
            notify(db, work.requester_id, "WORK_OVERDUE", f"{work.title} is overdue", "The completion deadline has passed.")
            if work.assignee_id:
                notify(db, work.assignee_id, "WORK_OVERDUE", f"{work.title} is overdue", "You can still submit the work or ask for an extension.")
            changed = True
    if changed:
        db.commit()


def serialize_user(db: Session, user: User) -> dict[str, object]:
    from .models import Review, UserSkill, Work
    skills = [row.skill.name for row in db.scalars(select(UserSkill).where(UserSkill.user_id == user.id)).all()]
    reviews = db.scalars(select(Review).where(Review.reviewee_id == user.id)).all()
    completed = len(db.scalars(select(Work).where(Work.assignee_id == user.id, Work.status == "COMPLETED")).all())
    rating = round(sum(item.rating for item in reviews) / len(reviews), 1) if reviews else 0
    return {
        "id": user.id, "name": user.name, "username": user.username, "email": user.email,
        "bio": user.bio, "location": user.location, "availability": user.availability,
        "profile_image": user.profile_image, "skills": skills, "rating": rating, "completed_works": completed,
    }