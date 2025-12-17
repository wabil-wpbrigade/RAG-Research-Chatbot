from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.db.models import User
from app.auth.security import hash_password, verify_password, create_access_token
from app.auth.dependencies import require_active_user
from app.auth.schemas import LoginRequest, SignupRequest

router = APIRouter(prefix="/auth", tags=["auth"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    """
    Endpoint: Logins the User or Admin
    Checks: User or Admin credentials
    Returns: Access Tokens
    """
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )
    token = create_access_token(
        {
            "sub": user.email,
            "is_admin": user.is_admin,
        }
    )
    return {
        "access_token": token,
        "token_type": "bearer",
    }

@router.post("/signup")
def signup(data: SignupRequest, db: Session = Depends(get_db)):
    """
    Endpoint: Creates new User or Admin
    Checks: If email already exists
    Saves: New User or Admin to the database
    """
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(
        name=data.name,                              # ✅ NEW
        email=data.email,
        hashed_password=hash_password(data.password),
        is_admin=False,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "Account created successfully"}


@router.get("/me")
def get_me(current_user: User = Depends(require_active_user)):
    """
    Returns: Current User or Admin Detail
    Used for Swagger UI
    """
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "is_admin": current_user.is_admin,
        "is_active": current_user.is_active,
    }
