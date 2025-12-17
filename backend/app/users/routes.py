from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.auth.security import hash_password
from app.db.database import SessionLocal
from app.db.models import User
from app.auth.dependencies import require_admin_user
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException


#Defined Structure for User/Admin Creation
class CreateUserRequest(BaseModel):
    name: str                    # ✅ NEW
    email: EmailStr
    password: str
    is_admin: bool = False


router = APIRouter(prefix="/users", tags=["users"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🔐 Admin-only: list all users
@router.get("/")
def list_users(
    _: User = Depends(require_admin_user),
    db: Session = Depends(get_db),):
    """
    Returns: List of All User and Admin Details
    """
    users = db.query(User).all()
    return [
        {
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "is_admin": u.is_admin,
            "is_active": u.is_active,
        }
        for u in users
    ]


#Admin-only: activate/deactivate user
@router.patch("/{user_id}/active")
def toggle_user_active(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_user),):
    """
    Checks: If admin try to deactivate himself (Doesnt allow)
    Switch: User or Admin's Status to active or in active
    """
    if user_id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="Admins cannot deactivate themselves"
        )

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = not user.is_active
    db.commit()
    db.refresh(user)

    return user



@router.post("/")
def create_user(
    data: CreateUserRequest,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin_user),):
    """
    Checks: If Email Already Exists in Database
    Adds: New User OR Admin to the database
    """
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="User already exists")

    user = User(
        name=data.name,                             # ✅ NEW
        email=data.email,
        password_hash=hash_password(data.password),
        is_admin=data.is_admin,
        is_active=True,
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already exists")
    db.refresh(user)
    return user
