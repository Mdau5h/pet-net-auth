from pydantic import BaseModel, Field, EmailStr


class UserRequest(BaseModel):
    full_name: str = Field(..., alias='fullName')
    phone: str = Field(..., alias='phone', pattern=r'^\d{10,}$', min_length=10, max_length=10)
    email: EmailStr = Field('', alias='email')
    login: str = Field(..., alias='login')
    password: str = Field(..., alias='password')


class UserResponse(BaseModel):
    id: int


class UserAuth(BaseModel):
    login: str
    password: str


class TokenInfo(BaseModel):
    access_token: str
    token_type: str
