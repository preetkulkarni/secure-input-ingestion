from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..auth.security import create_access_token, verify_password
from ..config import settings
from ..database import UserCollection
from ..models.user import Token, UserInDB
from typing import Optional

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    user_data = UserCollection.find_one({"username": username})
    if not user_data:
        return None
    
    user = UserInDB(**user_data)
    if not verify_password(password, user.hashed_password):
        return None
    
    return user

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub":user.username,
            "role":user.role
        },
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}