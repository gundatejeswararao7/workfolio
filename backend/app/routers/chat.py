from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Chat, ChatParticipant, Message, User
from ..schemas import MessageCreate
from ..security import current_user

router = APIRouter(prefix="/api/chats", tags=["chat"])


@router.get("")
def chats(db: Session = Depends(get_db), user: User = Depends(current_user)) -> list[dict[str, object]]:
    participant_rows = db.scalars(select(ChatParticipant).where(ChatParticipant.user_id == user.id)).all()
    output = []
    for participant in participant_rows:
        members = db.scalars(select(ChatParticipant).where(ChatParticipant.chat_id == participant.chat_id)).all()
        other = next((db.get(User, item.user_id) for item in members if item.user_id != user.id), None)
        last = db.scalar(select(Message).where(Message.chat_id == participant.chat_id).order_by(Message.created_at.desc()))
        output.append({"id": participant.chat_id, "other_user": {"name": other.name, "username": other.username} if other else None, "last_message": last.content if last else "Start a conversation", "unread_count": participant.unread_count})
    return output


@router.post("")
def create_chat(other_user_id: int, db: Session = Depends(get_db), user: User = Depends(current_user)) -> dict[str, int]:
    existing = db.scalar(select(Chat.id).join(ChatParticipant, Chat.id == ChatParticipant.chat_id).where(ChatParticipant.user_id == user.id))
    if existing:
        members = db.scalars(select(ChatParticipant).where(ChatParticipant.chat_id == existing)).all()
        if any(member.user_id == other_user_id for member in members):
            return {"id": existing}
    chat = Chat()
    db.add(chat)
    db.flush()
    db.add_all([ChatParticipant(chat_id=chat.id, user_id=user.id), ChatParticipant(chat_id=chat.id, user_id=other_user_id)])
    db.commit()
    return {"id": chat.id}


@router.get("/{chat_id}")
def chat_detail(chat_id: int, db: Session = Depends(get_db), user: User = Depends(current_user)) -> dict[str, object]:
    participant = db.scalar(select(ChatParticipant).where(ChatParticipant.chat_id == chat_id, ChatParticipant.user_id == user.id))
    if not participant:
        raise HTTPException(403, detail={"success": False, "message": "Chat not found.", "code": "FORBIDDEN"})
    messages = db.scalars(select(Message).where(Message.chat_id == chat_id).order_by(Message.created_at.asc())).all()
    participant.unread_count = 0
    db.commit()
    return {"messages": [{"id": item.id, "content": item.content, "sender_id": item.sender_id, "created_at": item.created_at} for item in messages]}


@router.post("/{chat_id}/messages")
def send_message(chat_id: int, payload: MessageCreate, db: Session = Depends(get_db), user: User = Depends(current_user)) -> dict[str, object]:
    participant = db.scalar(select(ChatParticipant).where(ChatParticipant.chat_id == chat_id, ChatParticipant.user_id == user.id))
    if not participant:
        raise HTTPException(403, detail={"success": False, "message": "Chat not found.", "code": "FORBIDDEN"})
    receiver = db.scalar(select(ChatParticipant).where(ChatParticipant.chat_id == chat_id, ChatParticipant.user_id != user.id))
    item = Message(chat_id=chat_id, sender_id=user.id, content=payload.content)
    db.add(item)
    if receiver:
        receiver.unread_count += 1
    db.commit()
    return {"id": item.id, "content": item.content, "sender_id": item.sender_id, "created_at": item.created_at}