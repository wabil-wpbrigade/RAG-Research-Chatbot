from pydantic import BaseModel, EmailStr


#Defined Structure for Login and Signup
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class SignupRequest(BaseModel):
    name: str                    # ✅ NEW
    email: EmailStr
    password: str

class MagicLinkRequest(BaseModel):
    email: EmailStr

class MagicVerifyRequest(BaseModel):
    token: str