from sqlalchemy.orm import Session
from app.users.schemas import CreateUserRequest
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends, HTTPException

from app.db.schemas import User
from app.db.database import SessionLocal
from app.auth.security import hash_password
from app.auth.dependencies import require_admin_user


router = APIRouter(prefix="/users", tags=["users"])



def get_db():
    """
    Provides a database session for request handling.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.get("/")
def list_users(
    _: User = Depends(require_admin_user),
    db: Session = Depends(get_db),):
    """
    Returns a list of all users and admins.
    """
    return serialize_users(db.query(User).all())




@router.patch("/{user_id}/active")
def toggle_user_active(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_user),):
    """
    Toggles the active status of a user.
    Prevents admins from deactivating themselves.
    """
    ensure_not_self(user_id, current_user)
    user = fetch_user_by_id(db, user_id)
    toggle_active(db, user)
    return user



@router.post("/")
def create_user(
    data: CreateUserRequest,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin_user),):
    """
    Creates a new user or admin account.
    """
    ensure_email_available(db, data.email)
    user = build_user(data)
    persist_user(db, user)
    return user


def serialize_users(users: list[User]) -> list[dict]:
    """
    Serializes user models into response dictionaries.
    """
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



def ensure_not_self(user_id: int, current_user: User):
    """
    Prevents admins from modifying their own active status.
    """
    if user_id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="Admins cannot deactivate themselves",
        )


def fetch_user_by_id(db: Session, user_id: int) -> User:
    """
    Retrieves a user by ID or raises a 404 error.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user



def toggle_active(db: Session, user: User):
    """
    Toggles a user's active status and persists the change.
    """
    user.is_active = not user.is_active
    db.commit()
    db.refresh(user)


def ensure_email_available(db: Session, email: str):
    """
    Ensures no existing user uses the provided email.
    """
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="User already exists")



def build_user(data: CreateUserRequest) -> User:
    """
    Builds a new User model from request data.
    """
    return User(
        name=data.name,
        email=data.email,
        password_hash=hash_password(data.password),
        is_admin=data.is_admin,
        is_active=True,
    )


def persist_user(db: Session, user: User):
    """
    Persists a user to the database with integrity handling.
    """
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already exists")
    db.refresh(user)
