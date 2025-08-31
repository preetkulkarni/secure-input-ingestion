from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt as jose_jwt

from ..database import UserCollection
from ..models.user import UserCreate, UserPublic, TokenData, UserInDB
from ..auth.security import get_password_hash
from ..config import settings

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jose_jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user_data = UserCollection.find_one({"username": token_data.username})
    if user_data is None:
        raise credentials_exception
    
    return UserInDB(**user_data)

async def get_current_active_admin(current_user: UserInDB = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user

@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    existing_user = UserCollection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already registered.",
        )
    
    hashed_password = get_password_hash(user.password)

    new_user = UserInDB(
        email = user.email,
        username = user.username,
        hashed_password=hashed_password
    )

    UserCollection.insert_one(new_user.model_dump()) # .dict() is deprecated

    return new_user

@router.get("/me", response_model=UserPublic)
async def read_users_me(current_user: UserInDB = Depends(get_current_user)):
    return current_user

@router.get("/admin/dashboard", response_model=dict)
async def read_admin_dashboard(current_user: UserInDB = Depends(get_current_active_admin)):
    return {"message": f"Welcome Admin {current_user.username}!"}