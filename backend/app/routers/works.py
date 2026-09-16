from datetime import datetime, timedelta
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Application, DeadlineExtension, Review, Transaction, User, Wallet, Work, WorkRequest
from ..schemas import ApplicationCreate, ExtendWork, ReviewCreate, WalletTopUp, WorkAction, WorkCreate
from ..security import current_user
from ..services import notify, update_overdue

router = APIRouter(prefix="/api", tags=["works"])


def work_json(db: Session, work: Work) -> dict[str, object]:
    requester = db.get(User, work.requester_id)
    assignee = db.get(User, work.assignee_id) if work.assignee_id else None
    return {
        "id": work.id, "requester_id": work.requester_id, "assignee_id": work.assignee_id, "title": work.title,
        "description": work.description, "status": work.status, "budget": work.budget, "deadline_duration_days": work.deadline_duration_days,
        "application_deadline": work.application_deadline, "accepted_at": work.accepted_at, "due_at": work.due_at,
        "submitted_at": work.submitted_at, "completed_at": work.completed_at, "is_overdue": work.is_overdue,
        "was_submitted_late": work.was_submitted_late, "location": work.location, "work_mode": work.work_mode,
        "progress": work.progress, "requester_name": requester.name if requester else "", "assignee_name": assignee.name if assignee else "",
    }


@router.get("/works")
def list_works(db: Session = Depends(get_db), user: User = Depends(current_user)) -> dict[str, object]:
    works = db.scalars(select(Work).order_by(Work.created_at.desc()).limit(60)).all()
    update_overdue(db, works)
    doing = [work_json(db, work) for work in works if work.assignee_id == user.id and work.status not in {"COMPLETED", "CANCELLED"}]
    given = [work_json(db, work) for work in works if work.requester_id == user.id and work.status not in {"COMPLETED", "CANCELLED"}]
    completed_by_me = [work_json(db, work) for work in works if work.assignee_id == user.id and work.status == "COMPLETED"]
    completed_for_me = [work_json(db, work) for work in works if work.requester_id == user.id and work.status == "COMPLETED"]
    open_work = [work_json(db, work) for work in works if work.status == "OPEN" and work.requester_id != user.id]
    return {"doing": doing, "given": given, "completed_by_me": completed_by_me, "completed_for_me": completed_for_me, "open": open_work}


@router.post("/works")
def create_work(payload: WorkCreate, db: Session = Depends(get_db), user: User = Depends(current_user)) -> dict[str, object]:
    work = Work(requester_id=user.id, title=payload.title, description=payload.description, budget=payload.budget, deadline_duration_days=payload.deadline_duration_days, application_deadline=payload.application_deadline, location=payload.location, work_mode=payload.work_mode, status="OPEN")
    db.add(work)
    db.commit()
    db.refresh(work)
    return work_json(db, work)


@router.get("/works/{work_id}")
def get_work(work_id: int, db: Session = Depends(get_db), user: User = Depends(current_user)) -> dict[str, object]:
    work = db.get(Work, work_id)
    if not work:
        raise HTTPException(404, detail={"success": False, "message": "Work not found.", "code": "NOT_FOUND"})
    applications = db.scalars(select(Application).where(Application.work_id == work.id)).all()
    return {**work_json(db, work), "applications": [{"id": app.id, "applicant_id": app.applicant_id, "applicant_name": db.get(User, app.applicant_id).name, "message": app.message, "status": app.status, "created_at": app.created_at} for app in applications if work.requester_id == user.id or app.applicant_id == user.id]}


@router.post("/works/{work_id}/apply")
def apply(work_id: int, payload: ApplicationCreate, db: Session = Depends(get_db), user: User = Depends(current_user)) -> dict[str, object]:
    work = db.get(Work, work_id)
    if not work or work.status != "OPEN" or work.requester_id == user.id:
        raise HTTPException(400, detail={"success": False, "message": "This opportunity is not available for an application.", "code": "NOT_AVAILABLE"})
    existing = db.scalar(select(Application).where(Application.work_id == work_id, Application.applicant_id == user.id))
    if existing:
        raise HTTPException(400, detail={"success": False, "message": "You already applied to this opportunity.", "code": "ALREADY_APPLIED"})
    item = Application(work_id=work_id, applicant_id=user.id, message=payload.message)
    db.add(item)
    notify(db, work.requester_id, "APPLICATION_RECEIVED", "New application", f"{user.name} applied to {work.title}.")
    db.commit()
    return {"success": True, "message": "Application sent."}


@router.post("/works/{work_id}/applications/{application_id}/accept")
def accept_application(work_id: int, application_id: int, db: Session = Depends(get_db), user: User = Depends(current_user)) -> dict[str, object]:
    work, application = db.get(Work, work_id), db.get(Application, application_id)
    if not work or not application or work.requester_id != user.id or application.work_id != work_id:
        raise HTTPException(403, detail={"success": False, "message": "You cannot accept this application.", "code": "FORBIDDEN"})
    now = datetime.utcnow()
    work.assignee_id, work.accepted_at, work.due_at, work.status, work.progress = application.applicant_id, now, now + timedelta(days=work.deadline_duration_days), "IN_PROGRESS", 0
    application.status = "ACCEPTED"
    notify(db, application.applicant_id, "APPLICATION_ACCEPTED", "Application accepted", f"You are now assigned to {work.title}.")
    db.commit()
    return work_json(db, work)


@router.post("/works/{work_id}/submit")
def submit_work(work_id: int, payload: WorkAction, db: Session = Depends(get_db), user: User = Depends(current_user)) -> dict[str, object]:
    work = db.get(Work, work_id)
    if not work or work.assignee_id != user.id or work.status not in {"IN_PROGRESS", "OVERDUE", "REVISION_REQUIRED"}:
        raise HTTPException(403, detail={"success": False, "message": "Only the current assignee can submit active work.", "code": "FORBIDDEN"})
    now = datetime.utcnow()
    work.submitted_at, work.submission_note, work.was_submitted_late = now, payload.note, bool(work.due_at and now > work.due_at)
    work.delay_duration = max(0, int((now - work.due_at).total_seconds())) if work.due_at and now > work.due_at else 0
    work.status, work.progress, work.is_overdue = "SUBMITTED", 100, False
    notify(db, work.requester_id, "WORK_SUBMITTED", f"{work.title} is ready for review", f"{user.name} submitted the work for review.")
    db.commit()
    return work_json(db, work)


@router.post("/works/{work_id}/revise")
def request_revision(work_id: int, payload: WorkAction, db: Session = Depends(get_db), user: User = Depends(current_user)) -> dict[str, object]:
    work = db.get(Work, work_id)
    if not work or work.requester_id != user.id or work.status != "SUBMITTED":
        raise HTTPException(403, detail={"success": False, "message": "Only the requester can ask for a revision.", "code": "FORBIDDEN"})
    work.status, work.progress = "REVISION_REQUIRED", 70
    notify(db, work.assignee_id or 0, "REVISION_REQUESTED", f"Revision requested for {work.title}", payload.note or "Please review the request and resubmit.")
    db.commit()
    return work_json(db, work)


@router.post("/works/{work_id}/approve")
def approve_work(work_id: int, db: Session = Depends(get_db), user: User = Depends(current_user)) -> dict[str, object]:
    work = db.get(Work, work_id)
    if not work or work.requester_id != user.id or work.status != "SUBMITTED":
        raise HTTPException(403, detail={"success": False, "message": "Only submitted work can be approved.", "code": "FORBIDDEN"})
    requester_wallet, assignee_wallet = db.scalar(select(Wallet).where(Wallet.user_id == user.id)), db.scalar(select(Wallet).where(Wallet.user_id == work.assignee_id))
    if not requester_wallet or not assignee_wallet or requester_wallet.balance < work.budget:
        work.status = "PAYMENT_PENDING"
        db.commit()
        raise HTTPException(400, detail={"success": False, "message": "The demo wallet needs more balance before payment can complete.", "code": "INSUFFICIENT_BALANCE"})
    requester_wallet.balance -= work.budget
    assignee_wallet.balance += work.budget
    work.status, work.completed_at, work.progress = "COMPLETED", datetime.utcnow(), 100
    transaction = Transaction(transaction_id=f"LL-{uuid.uuid4().hex[:10].upper()}", work_id=work.id, from_user_id=user.id, to_user_id=work.assignee_id, amount=work.budget, type="SIMULATED_PAYMENT", status="SUCCESS")
    db.add(transaction)
    notify(db, work.assignee_id or 0, "PAYMENT_RECEIVED", f"Payment received for {work.title}", f"₹{work.budget:,.0f} demo balance was credited.")
    notify(db, user.id, "WORK_COMPLETED", f"{work.title} completed", "Your demo payment was recorded.")
    db.commit()
    return work_json(db, work)


@router.post("/works/{work_id}/extend")
def extend_work(work_id: int, payload: ExtendWork, db: Session = Depends(get_db), user: User = Depends(current_user)) -> dict[str, object]:
    work = db.get(Work, work_id)
    if not work or work.requester_id != user.id or not work.due_at or work.status not in {"IN_PROGRESS", "OVERDUE"}:
        raise HTTPException(403, detail={"success": False, "message": "Only active work can be extended by its requester.", "code": "FORBIDDEN"})
    old_due = work.due_at
    work.due_at += timedelta(days=payload.days)
    work.extended_at, work.extension_count, work.status, work.is_overdue = datetime.utcnow(), work.extension_count + 1, "IN_PROGRESS", False
    db.add(DeadlineExtension(work_id=work.id, old_due_at=old_due, new_due_at=work.due_at, extended_by=user.id, reason=payload.reason))
    notify(db, work.assignee_id or 0, "DEADLINE_EXTENDED", f"Deadline extended for {work.title}", f"Your new deadline is {work.due_at.date().isoformat()}.")
    db.commit()
    return work_json(db, work)


@router.get("/requests")
def requests(db: Session = Depends(get_db), user: User = Depends(current_user)) -> dict[str, object]:
    incoming = db.scalars(select(Application).join(Work, Application.work_id == Work.id).where(Work.requester_id == user.id, Application.status == "PENDING")).all()
    outgoing = db.scalars(select(Application).where(Application.applicant_id == user.id)).all()
    return {"incoming": [{"id": item.id, "work_id": item.work_id, "work_title": db.get(Work, item.work_id).title, "applicant_id": item.applicant_id, "applicant_name": db.get(User, item.applicant_id).name, "message": item.message, "status": item.status} for item in incoming], "outgoing": [{"id": item.id, "work_id": item.work_id, "work_title": db.get(Work, item.work_id).title, "status": item.status} for item in outgoing]}


@router.get("/transactions")
def transactions(db: Session = Depends(get_db), user: User = Depends(current_user)) -> dict[str, object]:
    wallet = db.scalar(select(Wallet).where(Wallet.user_id == user.id))
    rows = db.scalars(select(Transaction).where(or_(Transaction.from_user_id == user.id, Transaction.to_user_id == user.id)).order_by(Transaction.created_at.desc())).all()
    return {"balance": wallet.balance if wallet else 0, "items": [{"id": row.transaction_id, "amount": row.amount, "type": row.type, "status": row.status, "created_at": row.created_at, "direction": "received" if row.to_user_id == user.id else "sent"} for row in rows]}


@router.post("/wallet/top-up")
def top_up(payload: WalletTopUp, db: Session = Depends(get_db), user: User = Depends(current_user)) -> dict[str, object]:
    wallet = db.scalar(select(Wallet).where(Wallet.user_id == user.id))
    wallet.balance += payload.amount
    db.add(Transaction(transaction_id=f"LL-{uuid.uuid4().hex[:10].upper()}", amount=payload.amount, type="DEMO_WALLET_TOPUP", status="SUCCESS", to_user_id=user.id))
    db.commit()
    return {"success": True, "balance": wallet.balance}


@router.post("/works/{work_id}/review")
def review(work_id: int, payload: ReviewCreate, db: Session = Depends(get_db), user: User = Depends(current_user)) -> dict[str, object]:
    work = db.get(Work, work_id)
    if not work or work.requester_id != user.id or work.status != "COMPLETED" or not work.assignee_id:
        raise HTTPException(400, detail={"success": False, "message": "Only completed work can be reviewed.", "code": "INVALID_REVIEW"})
    if db.scalar(select(Review).where(Review.work_id == work_id, Review.reviewer_id == user.id)):
        raise HTTPException(400, detail={"success": False, "message": "You already reviewed this work.", "code": "ALREADY_REVIEWED"})
    db.add(Review(work_id=work_id, reviewer_id=user.id, reviewee_id=work.assignee_id, rating=payload.rating, comment=payload.comment))
    notify(db, work.assignee_id, "NEW_RATING", "New review on your profile", f"{user.name} left you a {payload.rating}-star review.")
    db.commit()
    return {"success": True, "message": "Review published."}