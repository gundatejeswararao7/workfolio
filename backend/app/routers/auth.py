from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User, Wallet
from ..schemas import CompleteRegistration, LoginRequest, RegisterStart, ResetPassword, APIMessage, OTPVerify
from ..security import create_token, hash_password, verify_password
from ..services import generate_otp, verify_otp

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/send-otp")
def send_otp(payload: RegisterStart, db: Session = Depends(get_db)) -> dict[str, object]:
    if db.scalar(select(User).where(User.email == payload.email)):
        raise HTTPException(400, detail={"success": False, "message": "That Gmail address is already registered.", "code": "EMAIL_EXISTS"})
    code = generate_otp(db, payload.email, "register")
    return {"success": True, "message": "OTP sent. In development, use the code shown below.", "dev_otp": code}


@router.post("/verify-otp", response_model=APIMessage)
def verify_registration_otp(payload: OTPVerify, db: Session = Depends(get_db)) -> APIMessage:
    if not verify_otp(db, payload.email, payload.otp, "register"):
        raise HTTPException(400, detail={"success": False, "message": "That OTP is invalid or expired.", "code": "INVALID_OTP"})
    return APIMessage(message="Email verified. Create your account.")


@router.post("/register")
def register(payload: CompleteRegistration, db: Session = Depends(get_db)) -> dict[str, object]:
    if not payload.email.lower().endswith("@gmail.com"):
        raise HTTPException(400, detail={"success": False, "message": "Only Gmail addresses can register.", "code": "GMAIL_REQUIRED"})
    if payload.password != payload.confirm_password:
        raise HTTPException(400, detail={"success": False, "message": "Passwords do not match.", "code": "PASSWORD_MISMATCH"})
    if db.scalar(select(User).where((User.email == payload.email) | (User.username == payload.username.lower()))):
        raise HTTPException(400, detail={"success": False, "message": "Email or username is already in use.", "code": "ACCOUNT_EXISTS"})
    if not verify_otp(db, payload.email, payload.otp, "register"):
        raise HTTPException(400, detail={"success": False, "message": "Verify your Gmail OTP before creating an account.", "code": "INVALID_OTP"})
    user = User(email=payload.email.lower(), password_hash=hash_password(payload.password), name=payload.name, username=payload.username.lower())
    db.add(user)
    db.flush()
    db.add(Wallet(user_id=user.id, balance=0))
    db.commit()
    return {"success": True, "token": create_token(user.id), "user": {"id": user.id, "name": user.name, "username": user.username, "email": user.email}}


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> dict[str, object]:
    user = db.scalar(select(User).where(User.email == payload.email.lower()))
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(401, detail={"success": False, "message": "Email or password is incorrect.", "code": "INVALID_CREDENTIALS"})
    return {"success": True, "token": create_token(user.id), "user": {"id": user.id, "name": user.name, "username": user.username, "email": user.email}}


@router.post("/forgot-password")
def forgot_password(payload: RegisterStart, db: Session = Depends(get_db)) -> dict[str, object]:
    if not db.scalar(select(User).where(User.email == payload.email)):
        raise HTTPException(404, detail={"success": False, "message": "No account was found for that Gmail.", "code": "NOT_FOUND"})
    code = generate_otp(db, payload.email, "reset")
    return {"success": True, "message": "Reset OTP sent.", "dev_otp": code}


@router.post("/reset-password", response_model=APIMessage)
def reset_password(payload: ResetPassword, db: Session = Depends(get_db)) -> APIMessage:
    if payload.password != payload.confirm_password:
        raise HTTPException(400, detail={"success": False, "message": "Passwords do not match.", "code": "PASSWORD_MISMATCH"})
    user = db.scalar(select(User).where(User.email == payload.email.lower()))
    if not user or not verify_otp(db, payload.email, payload.otp, "reset"):
        raise HTTPException(400, detail={"success": False, "message": "That OTP is invalid or expired.", "code": "INVALID_OTP"})
    user.password_hash = hash_password(payload.password)
    db.commit()
    return APIMessage(message="Password updated. You can sign in now.")