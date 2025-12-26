import os, secrets

from dotenv import load_dotenv
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status, Request

from app.db.database import SessionLocal
from app.email.eml_writer import write_eml_file
from app.db.schemas import User, MagicLoginToken
from app.auth.dependencies import require_active_user
from app.auth.schemas import (MagicLinkRequest,MagicVerifyRequest)
from app.auth.security import (hash_password,verify_password,create_access_token,hash_token,)

load_dotenv()

FRONTEND_URL = os.getenv("FRONTEND_URL")

router = APIRouter(prefix="/auth", tags=["auth"])

MAGIC_TOKEN_EXPIRY_MINUTES = 15

def get_db():
    """
    Provides a database session for request handling.
    Ensures the session is closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/magic/request")
def request_magic_link(
    data: MagicLinkRequest,
    request: Request,db: Session = Depends(get_db),):
    """
    Generates and emails a secure magic login link.
    """
    user = fetch_user_by_email(db, data.email)
    ensure_active(user)
    token = create_magic_token(db, user, request)
    send_magic_email(user.email, token)
    return {"message": "Magic login link sent successfully."}


@router.post("/magic/verify")
def verify_magic_link(
    data: MagicVerifyRequest,db: Session = Depends(get_db),):
    """
    Verifies a magic login token and issues a JWT.
    """
    magic_token = validate_magic_token(db, data.token)
    user = activate_magic_token(db, magic_token)
    ensure_active(user)
    return issue_token(user)


@router.get("/me")
def get_me(current_user: User = Depends(require_active_user)):
    """
    Returns details of the currently authenticated user.
    """
    return serialize_user(current_user)


def fetch_user_by_email(db: Session, email: str) -> User:
    """
    Retrieves a user by email or raises a 404 error.
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="No account found with this email.")
    return user


def validate_password(password: str, user: User):
    """
    Validates a user's password.
    """
    if not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )


def ensure_active(user: User):
    """
    Ensures a user account is active.
    """
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )


def ensure_email_available(db: Session, email: str):
    """
    Ensures no existing account uses the provided email.
    """
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")


def issue_token(user: User):
    """
    Issues a JWT access token for a user.
    """
    token = create_access_token(
        {"sub": user.email, "is_admin": user.is_admin}
    )
    return {"access_token": token, "token_type": "bearer"}


def create_magic_token(db: Session, user: User, request: Request) -> str:
    """
    Creates and stores a hashed magic login token.
    """
    raw = secrets.token_urlsafe(32)
    token = MagicLoginToken(
        user_id=user.id,
        token_hash=hash_token(raw),
        expires_at=expiry_time(),
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("User-Agent"),
    )
    db.add(token)
    db.commit()
    return raw


def validate_magic_token(db: Session, raw_token: str) -> MagicLoginToken:
    """
    Validates a magic token and ensures it is unused and unexpired.
    """
    token = db.query(MagicLoginToken).filter(
        MagicLoginToken.token_hash == hash_token(raw_token)
    ).first()
    if not token or token.used or is_expired(token.expires_at):
        raise HTTPException(status_code=400, detail="Invalid or expired magic link")
    return token


def activate_magic_token(db: Session, token: MagicLoginToken) -> User:
    """
    Marks a magic token as used and returns the associated user.
    """
    token.used = True
    token.used_at = datetime.now(timezone.utc)
    db.commit()
    return token.user


def send_magic_email(email: str, token: str):
    """
    Sends a magic login email to the user.
    """
    link = f"{FRONTEND_URL}/auth/magic?token={token}"
    write_eml_file(
        to=email,
        subject="Your secure login link",
        body=f"Click here to login:\n\n{link}",
    )


def expiry_time():
    """
    Returns the expiry timestamp for a magic token.
    """
    return datetime.now(timezone.utc) + timedelta(minutes=MAGIC_TOKEN_EXPIRY_MINUTES)


def is_expired(expires_at: datetime) -> bool:
    """
    Checks whether a datetime value is expired.
    """
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    return expires_at < datetime.now(timezone.utc)


def serialize_user(user: User) -> dict:
    """
    Serializes a user model into a response dictionary.
    """
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "is_admin": user.is_admin,
        "is_active": user.is_active,
    }
