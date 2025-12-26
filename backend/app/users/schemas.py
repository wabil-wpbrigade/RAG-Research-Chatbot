from pydantic import BaseModel, EmailStr


class CreateUserRequest(BaseModel):
    """
    Request schema for creating a user or admin account.
    """
    name: str
    email: EmailStr
    password: str
    is_admin: bool = False