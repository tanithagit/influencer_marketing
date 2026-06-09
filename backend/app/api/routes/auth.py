from fastapi import APIRouter, Depends, status, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserRegister, UserLogin, Token, UserResponse
from app.services.auth_service import register_user, login_user
from app.services.email_service import send_welcome_email
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    user_data: UserRegister,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    user = register_user(db, user_data)
    # Send welcome email in background
    background_tasks.add_task(
        send_welcome_email,
        user.email,
        user.full_name
    )
    return user

@router.post("/login", response_model=Token)
def login(
    user_data: UserLogin,
    db: Session = Depends(get_db)
):
    result = login_user(db, user_data.email, user_data.password)
    return {
        "access_token": result["access_token"],
        "token_type":   "bearer",
        "user":         result["user"]
    }

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user