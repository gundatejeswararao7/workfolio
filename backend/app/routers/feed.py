from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from ..database import get_db
from ..models import Post, User
from ..schemas import PostCreate
from ..security import current_user
from ..services import serialize_user

router = APIRouter(prefix="/api/feed", tags=["feed"])


def post_json(db: Session, post: Post) -> dict[str, object]:
    return {
        "id": post.id, "content": post.content, "media_url": post.media_url, "media_type": post.media_type,
        "likes_count": post.likes_count, "comments_count": post.comments_count, "created_at": post.created_at,
        "author": serialize_user(db, post.author),
    }


@router.get("")
def feed(db: Session = Depends(get_db), _user: User = Depends(current_user)) -> list[dict[str, object]]:
    posts = db.scalars(select(Post).options(joinedload(Post.author)).order_by(Post.created_at.desc()).limit(30)).all()
    return [post_json(db, post) for post in posts]


@router.post("")
def create_post(payload: PostCreate, db: Session = Depends(get_db), user: User = Depends(current_user)) -> dict[str, object]:
    post = Post(user_id=user.id, content=payload.content, media_url=payload.media_url, media_type=payload.media_type)
    db.add(post)
    db.commit()
    db.refresh(post)
    post.author = user
    return post_json(db, post)


@router.post("/{post_id}/like")
def like_post(post_id: int, db: Session = Depends(get_db), _user: User = Depends(current_user)) -> dict[str, object]:
    post = db.get(Post, post_id)
    if not post:
        raise HTTPException(404, detail={"success": False, "message": "Post not found.", "code": "NOT_FOUND"})
    post.likes_count += 1
    db.commit()
    return {"success": True, "likes_count": post.likes_count}