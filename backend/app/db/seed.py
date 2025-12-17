from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.db.models import User
from app.auth.security import hash_password


def seed_admin():
    """
    Initializes a User and an Admin Account
    """
    db: Session = SessionLocal()
    try:
        admin = db.query(User).filter(User.email == "admin@example.com").first()
        if not admin:
            admin = User(
                name="Admin",
                email="admin@example.com",
                password_hash=hash_password("admin123"),
                is_admin=True,
                is_active=True,
            )
            db.add(admin)

        user = db.query(User).filter(User.email == "user@example.com").first()
        if not user:
            user = User(
                name="Normal User",
                email="user@example.com",
                password_hash=hash_password("user123"),
                is_admin=False,
                is_active=True,
            )
            db.add(user)

        db.commit()
    finally:
        db.close()
