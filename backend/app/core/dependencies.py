from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.utils.jwt import decode_access_token
from app.models.user import User, UserRole

# Use HTTPBearer instead of OAuth2PasswordBearer
# This shows a proper token input box in Swagger UI
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception

    return user

def get_current_brand(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role != UserRole.brand:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only brands can access this"
        )
    return current_user

def get_current_influencer(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role != UserRole.influencer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only influencers can access this"
        )
    return current_user

def get_current_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can access this"
        )
    return current_user