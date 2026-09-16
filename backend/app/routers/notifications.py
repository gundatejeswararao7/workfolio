from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Notification, User
from ..security import current_user

router = APIRouter(prefix="/api/notifications", tags=["notifications"])


@router.get("")
def notifications(db: Session = Depends(get_db), user: User = Depends(current_user)) -> list[dict[str, object]]:
    items = db.scalars(select(Notification).where(Notification.user_id == user.id).order_by(Notification.created_at.desc()).limit(50)).all()
    return [{"id": item.id, "type": item.type, "title": item.title, "body": item.body, "is_read": item.is_read, "created_at": item.created_at} for item in items]


@router.post("/read-all")
def read_all(db: Session = Depends(get_db), user: User = Depends(current_user)) -> dict[str, object]:
    for item in db.scalars(select(Notification).where(Notification.user_id == user.id, Notification.is_read.is_(False))).all():
        item.is_read = True
    db.commit()
    return {"success": True}