from pydantic import BaseModel, EmailStr
from app.db.database import SessionLocal

class MagicLinkRequest(BaseModel):
    email: EmailStr

class MagicVerifyRequest(BaseModel):
    token: str

def get_db():
    """
    Creates and yields a database session.
    Ensures the session is closed after request completion.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
