from sqlalchemy.orm import Session

from app.db.schemas import User
from app.db.database import SessionLocal
from app.auth.security import hash_password

def seed_admin():
    """
    Seeds the database with a default admin and a normal user.
    """
    db = SessionLocal()
    try:
        seed_user(db, "Admin", "admin@example.com", "admin123", True)
        seed_user(db, "Normal User", "user@example.com", "user123", False)
        db.commit()
    finally:
        db.close()



def seed_user(db: Session,name: str,email: str,password: str,is_admin: bool,):
    """
    Creates a user if one does not already exist.
    """
    if user_exists(db, email):
        return
    user = build_user(name, email, password, is_admin)
    db.add(user)


def user_exists(db: Session, email: str) -> bool:
    """
    Checks whether a user with the given email exists.
    """
    return db.query(User).filter(User.email == email).first() is not None


def build_user(name: str,email: str,password: str,is_admin: bool,) -> User:
    """
    Builds a User model with hashed credentials.
    """
    return User(
        name=name,
        email=email,
        password_hash=hash_password(password),
        is_admin=is_admin,
        is_active=True,
    )
