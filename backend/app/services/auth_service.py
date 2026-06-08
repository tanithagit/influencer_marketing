from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import timedelta
from app.models.user import User
from app.models.subscription import Subscription, SubscriptionPlan
from app.schemas.user import UserRegister
from app.utils.password import hash_password, verify_password
from app.utils.jwt import create_access_token
from app.core.config import settings

def register_user(db: Session, user_data: UserRegister) -> User:
    # Check if email already exists
    existing = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create user
    new_user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        full_name=user_data.full_name,
        role=user_data.role
    )
    db.add(new_user)
    db.flush()  # Get the user id without committing

    # Create free subscription automatically
    subscription = Subscription(
        user_id=new_user.id,
        plan=SubscriptionPlan.free
    )
    db.add(subscription)
    db.commit()
    db.refresh(new_user)

    return new_user


def login_user(db: Session, email: str, password: str) -> dict:
    # Find user
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Check password
    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Check if active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated"
        )

    # Create token
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role},
        expires_delta=timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    return {"access_token": access_token, "user": user}