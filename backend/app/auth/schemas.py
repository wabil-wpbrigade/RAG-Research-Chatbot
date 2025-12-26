from pydantic import BaseModel, EmailStr


class MagicLinkRequest(BaseModel):
    email: EmailStr

class MagicVerifyRequest(BaseModel):
    token: str