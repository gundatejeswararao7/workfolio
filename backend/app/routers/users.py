from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Review, Skill, User, UserSkill, Work
from ..schemas import UserUpdate
from ..security import current_user
from ..services import serialize_user

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me")
def me(user: User = Depends(current_user), db: Session = Depends(get_db)) -> dict[str, object]:
    return serialize_user(db, user)


@router.put("/me")
def update_me(payload: UserUpdate, user: User = Depends(current_user), db: Session = Depends(get_db)) -> dict[str, object]:
    conflict = db.scalar(select(User).where(User.username == payload.username.lower(), User.id != user.id))
    if conflict:
        raise HTTPException(400, detail={"success": False, "message": "That username is already taken.", "code": "USERNAME_EXISTS"})
    user.name, user.username, user.bio, user.location, user.availability = payload.name, payload.username.lower(), payload.bio, payload.location, payload.availability
    db.query(UserSkill).filter(UserSkill.user_id == user.id).delete()
    for name in payload.skills:
        skill = db.scalar(select(Skill).where(func.lower(Skill.name) == name.lower()))
        if not skill:
            skill = Skill(name=name)
            db.add(skill)
            db.flush()
        db.add(UserSkill(user_id=user.id, skill_id=skill.id))
    db.commit()
    return serialize_user(db, user)


@router.get("/search")
def search_people(q: str = Query(default=""), location: str = Query(default=""), skill: str = Query(default=""), db: Session = Depends(get_db), _user: User = Depends(current_user)) -> list[dict[str, object]]:
    query = select(User)
    if q:
        query = query.where(or_(User.name.ilike(f"%{q}%"), User.username.ilike(f"%{q}%"), User.bio.ilike(f"%{q}%")))
    if location:
        query = query.where(User.location.ilike(f"%{location}%"))
    people = db.scalars(query.order_by(User.created_at.desc()).limit(30)).all()
    results = [serialize_user(db, person) for person in people]
    if skill:
        results = [person for person in results if any(skill.lower() in item.lower() for item in person["skills"])]
    return results


@router.get("/{username}")
def profile(username: str, db: Session = Depends(get_db), _user: User = Depends(current_user)) -> dict[str, object]:
    user = db.scalar(select(User).where(User.username == username.lower()))
    if not user:
        raise HTTPException(404, detail={"success": False, "message": "Profile not found.", "code": "NOT_FOUND"})
    works = db.scalars(select(Work).where(Work.assignee_id == user.id, Work.status == "COMPLETED").order_by(Work.completed_at.desc())).all()
    reviews = db.scalars(select(Review).where(Review.reviewee_id == user.id).order_by(Review.created_at.desc())).all()
    return {**serialize_user(db, user), "completed": [{"id": work.id, "title": work.title, "budget": work.budget, "completed_at": work.completed_at} for work in works], "reviews": [{"rating": item.rating, "comment": item.comment, "created_at": item.created_at} for item in reviews]}