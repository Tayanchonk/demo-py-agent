from fastapi import APIRouter, Depends, HTTPException, status
from ...application import (
    AuthUseCase,
    LoginDTO,
    TokenResponseDTO,
    UserCreateDTO,
)
from ..dependencies import get_auth_use_case


router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
async def register(
    user_data: UserCreateDTO,
    auth_use_case: AuthUseCase = Depends(get_auth_use_case),
):
    """Register a new user"""
    success = await auth_use_case.create_user(user_data)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists or invalid data",
        )
    return {"message": "User created successfully"}


@router.post(
    "/login",
    response_model=TokenResponseDTO,
    summary="Login and get access token",
)
async def login(
    login_data: LoginDTO,
    auth_use_case: AuthUseCase = Depends(get_auth_use_case),
):
    """Login and get access token"""
    token = await auth_use_case.login(login_data)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    return token