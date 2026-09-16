from fastapi import APIRouter, Depends
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User, Work
from ..schemas import AIQuery
from ..security import current_user
from ..services import serialize_user, update_overdue

router = APIRouter(prefix="/api/ai", tags=["ai"])


@router.post("/query")
def ai_query(payload: AIQuery, db: Session = Depends(get_db), user: User = Depends(current_user)) -> dict[str, object]:
    text = payload.query.lower()
    works = db.scalars(select(Work).where(or_(Work.requester_id == user.id, Work.assignee_id == user.id))).all()
    update_overdue(db, works)
    if any(word in text for word in ("overdue", "late", "due", "deadline", "tomorrow", "week")):
        matching = []
        for work in works:
            if "overdue" in text or "late" in text:
                if work.is_overdue or work.was_submitted_late:
                    matching.append(work)
            else:
                matching.append(work)
        return {"intent": "DEADLINE_QUERY", "message": f"I found {len(matching)} project{'s' if len(matching) != 1 else ''} connected to your deadline question.", "results": [{"id": item.id, "title": item.title, "status": item.status, "due_at": item.due_at, "is_overdue": item.is_overdue} for item in matching]}
    if any(word in text for word in ("job", "opportunity", "work", "project")) and any(word in text for word in ("find", "want", "need", "show")):
        opportunities = db.scalars(select(Work).where(Work.status == "OPEN", Work.requester_id != user.id).order_by(Work.created_at.desc()).limit(5)).all()
        return {"intent": "FIND_OPPORTUNITY", "message": f"I found {len(opportunities)} open opportunities you can explore.", "results": [{"id": item.id, "title": item.title, "budget": item.budget, "description": item.description} for item in opportunities]}
    people = db.scalars(select(User).where(User.id != user.id, or_(User.name.ilike(f"%{text}%"), User.bio.ilike(f"%{text}%"), User.location.ilike(f"%{text}%"))).limit(5)).all()
    if people:
        return {"intent": "FIND_PERSON", "message": f"I found {len(people)} people who may fit that request.", "results": [serialize_user(db, person) for person in people]}
    return {"intent": "GENERAL", "message": "I can help you find people, discover open opportunities, or answer questions about your work deadlines.", "results": []}