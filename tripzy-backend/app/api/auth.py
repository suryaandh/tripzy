from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db

from app.schemas.user_schema import UserCreate, UserResponse, UserProfileResponse
from app.schemas.auth_schema import LoginRequest
from app.schemas.response import ApiResponse

from app.repositories.user_repository import get_user_by_email, create_user
from app.repositories.profile_repository import create_profile

from app.core.security import hash_password
from app.core.security import verify_password
from app.core.jwt import create_access_token
from app.core.deps_auth import get_current_user

router = APIRouter()


@router.post("/register", response_model=ApiResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user.email)

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)

    new_user = create_user(db, user.email, hashed_password)
    new_profile = create_profile(db, new_user.id)

    return {
        "success": True,
        "message": "Register success",
        "data": {
            "user": {
                "id": new_user.id,
                "email": new_user.email,
            },
            "profile": UserProfileResponse.model_validate(new_profile).model_dump()
        }
    }


@router.post("/login", response_model=ApiResponse)
def login(user: LoginRequest, db: Session = Depends(get_db)):

    db_user = get_user_by_email(db, user.email)

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )
    
    token = create_access_token(
        data={"sub":str(db_user.id)}
    )

    return {
        "success": True,
        "message": "Login success",
        "data": {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": db_user.id,
                "email": db_user.email
            }
        }
    }

@router.get("/me", response_model=ApiResponse)
def me(current_user: UserResponse = Depends(get_current_user)):
    return {
        "success": True,
        "message": "User profile retrieved successfully",
        "data": {
            "id": current_user.id,
            "email": current_user.email
        }
    }