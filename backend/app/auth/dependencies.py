from jose import JWTError, jwt
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.db.schemas import User
from app.auth.schemas import get_db
from app.auth.security import SECRET_KEY, ALGORITHM

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),) -> User:
    """
    Authenticates a request using JWT credentials.
    Returns the corresponding user from the database.
    """
    email = decode_token(credentials.credentials)
    return fetch_user(db, email)


def decode_token(token: str) -> str:
    """
    Decodes a JWT token and extracts the user email (subject).
    Raises an authentication error if the token is invalid.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub") or raise_auth_error()
    except JWTError:
        raise_auth_error()


def fetch_user(db: Session, email: str) -> User:
    """
    Fetches a user from the database using the provided email.
    Raises an authentication error if the user does not exist.
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise_auth_error()
    return user


def require_active_user(
    current_user: User = Depends(get_current_user),) -> User:
    """
    Ensures the authenticated user account is active.
    Raises a forbidden error if the account is inactive.
    """
    if not current_user.is_active:
        raise_forbidden("User account is inactive")
    return current_user


def require_admin_user(
    current_user: User = Depends(require_active_user),) -> User:
    """
    Ensures the authenticated user has admin privileges.
    Raises a forbidden error if the user is not an admin.
    """
    if not current_user.is_admin:
        raise_forbidden("Admin privileges required")
    return current_user


def raise_auth_error():
    """
    Raises a standardized authentication error
    for invalid or expired JWT tokens.
    """
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
    )


def raise_forbidden(message: str):
    """
    Raises a standardized forbidden error with a custom message.
    Used for authorization and permission checks.
    """
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=message,
    )
