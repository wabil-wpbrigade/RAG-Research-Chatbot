import secrets, os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from app.auth.security import hash_token
from app.db.database import SessionLocal
from app.email.eml_writer import write_eml_file
from app.db.models import User, MagicLoginToken
from datetime import datetime, timedelta, timezone
from app.auth.dependencies import require_active_user
from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.auth.security import hash_password, verify_password, create_access_token
from app.auth.schemas import LoginRequest, SignupRequest, MagicLinkRequest, MagicVerifyRequest

# ✅ Load environment variables
load_dotenv()
FRONTEND_URL = os.getenv("FRONTEND_URL")

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



@router.post("/magic/request")
def request_magic_link(
    data: MagicLinkRequest,
    request: Request,
    db: Session = Depends(get_db),):
    """
    Send a magic login link to a user's email address.

    Generates a secure, time-limited login token for an active user
    and emails it as a magic link. The token is stored in hashed form
    and can be used only once.
    """
    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="No account found with this email.",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Your account is inactive. Please contact an administrator.",
        )

    raw_token = secrets.token_urlsafe(32)
    token_hash = hash_token(raw_token)

    expires_at = datetime.now(timezone.utc) + timedelta(minutes=15)

    magic_token = MagicLoginToken(
        user_id=user.id,
        token_hash=token_hash,
        expires_at=expires_at,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("User-Agent"),
    )

    db.add(magic_token)
    db.commit()

    magic_link = f"{FRONTEND_URL}/auth/magic?token={raw_token}"

    write_eml_file(
        to=user.email,
        subject="Your secure login link",
        body=f"Click here to login:\n\n{magic_link}",
    )

    return {"message": "Magic login link sent successfully."}



@router.post("/magic/verify")
def verify_magic_link(
    data: MagicVerifyRequest,
    db: Session = Depends(get_db),):
    """
    Verify a magic login token and authenticate the user.

    Validates the provided magic token and, if successful, marks it
    as used and returns a JWT access token for the associated user.
    """
    token_hash = hash_token(data.token)

    magic_token = (
        db.query(MagicLoginToken)
        .filter(MagicLoginToken.token_hash == token_hash)
        .first()
    )

    if not magic_token:
        raise HTTPException(status_code=400, detail="Invalid magic link")

    if magic_token.used:
        raise HTTPException(status_code=400, detail="Magic link already used")

    expires_at = magic_token.expires_at

    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Magic link expired")

    # Mark token as used
    magic_token.used = True
    magic_token.used_at = datetime.now(timezone.utc)

    user = magic_token.user

    if not user.is_active:
        raise HTTPException(status_code=403, detail="User is inactive")

    db.commit()

    # Issue normal JWT
    access_token = create_access_token(
    data={
        "sub": user.email,
        "is_admin": user.is_admin,
    }
)
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }





@router.get("/me")
def get_me(current_user: User = Depends(require_active_user)):
    """
    Returns: Current User or Admin Detail
    """
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "is_admin": current_user.is_admin,
        "is_active": current_user.is_active,
    }
