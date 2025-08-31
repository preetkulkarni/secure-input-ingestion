from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# documenation needed.

PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"

class UserBase(BaseModel):
    """
    Foundational model for a user, defines core fields common across all user-related data objects.
    """
    email: EmailStr = Field(..., example="user@example.com")
    username: str = Field(..., min_length=3, max_length=50, example="john_doe")

class UserCreate(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        example="Strong_Password123!",
        regex=PASSWORD_REGEX,
        description="Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character."
    )

class UserInDB(UserBase):
    hashed_password: str
    role: str = Field("user", example="user")

class UserPublic(UserBase):
    role: str = Field(..., example="user")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
