from pydantic import BaseModel, EmailStr


class SignupRequest(BaseModel):
    name: str                    # ✅ NEW
    email: EmailStr
    password: str

class MagicLinkRequest(BaseModel):
    email: EmailStr

class MagicVerifyRequest(BaseModel):
    token: str