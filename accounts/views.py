from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from server.settings import get_db
from .models import User, BlackListTokens
from .schemas import *
from .helpers import *
from .security import *
from .validators import *
from .permissions import *

auth = APIRouter()

@auth.post("/register", response_model=UserSchema)
async def register_api_view(data:RegisterShcema, db:Session=Depends(get_db)):
    print(data.username)
    user = get_user(username=data.username, db=db)
    if user is not None:
        return HTTPException(detail="User already exists!", status_code=status.HTTP_400_BAD_REQUEST)
    password_hash = hash_password(data.password)
    new_user = User(username=data.username, password=password_hash)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@auth.post("/login")
async def register_api_view(data:LoginShcema, db:Session=Depends(get_db)):
    user = authenticate(username=data.username, password=data.password, db=db)
    if not user:
        return HTTPException(detail="Invalid credentials!", status_code=status.HTTP_400_BAD_REQUEST)
    
    return {
        "refresh":create_refresh_token(user.username, user.id),
        "access":create_access_token(user.username, user.id)
    }



@auth.post("/logout", dependencies=[Depends(is_authenticated)])
async def logout_api_view(token:str, db:Session=Depends(get_db)):
    is_valid_token = validate_refresh_token(token, db)
    if is_valid_token is not None:
        blocked_token = BlackListTokens(token=token)
        db.add(blocked_token)
        db.commit()
        db.refresh(blocked_token)
        return {
            "message":"logged out user",
            "status":status.HTTP_200_OK
        }
    return HTTPException("Invalid or expired token!")



@auth.post("/refresh", dependencies=[Depends(is_authenticated)])
async def refresh_token(token:str, db:Session=Depends(get_db)):
    is_valid_token = validate_refresh_token(token=token, db=db)
    if is_valid_token:
        return {
            "refresh":token,
            "access":create_access_token(
                username=is_valid_token["username"],
                user_id=int(is_valid_token["sub"]))
        }
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid token"
    )


@auth.get("/me", response_model=UserSchema)
async def get_profile(user=Depends(get_current_user)):
    return user

