from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.schemas.user_schema import UserCreate, UserResponse, UserProfileResponse, MeResponse
from app.schemas.auth_schema import LoginRequest
from app.schemas.response import ApiResponse, success_response
from app.repositories.user_repository import get_user_by_email, create_user
from app.core.security import hash_password, verify_password
from app.core.jwt import create_access_token
from app.core.deps_auth import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=ApiResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = create_user(db, user.email, hash_password(user.password))

    return success_response(
        message="Register success",
        data={
            "user": {"id": new_user.id, "email": new_user.email},
            "profile": UserProfileResponse.model_validate(new_user.profile).model_dump(),
        },
    )


@router.post("/login", response_model=ApiResponse)
def login(user: LoginRequest, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"sub": str(db_user.id)})

    return success_response(
        message="Login success",
        data={
            "access_token": token,
            "token_type": "bearer",
            "user_id": db_user.id,
            "email": db_user.email,
            "profile": UserProfileResponse.model_validate(db_user.profile).model_dump(),
        },
    )


@router.get("/me", response_model=ApiResponse)
def me(current_user: UserResponse = Depends(get_current_user)):
    return success_response(
        message="User retrieved successfully",
        data=MeResponse(
            id=current_user.id,
            email=current_user.email,
            **UserProfileResponse.model_validate(current_user.profile).model_dump(exclude={"id"}),
        ).model_dump(),
    )