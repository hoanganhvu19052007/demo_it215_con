# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from typing import Dict

# from app.core.exceptions import BadRequestException
# from app.core.security import (
#     create_access_token,
#     create_refresh_token,
#     decode_token,
#     hash_password,
#     verify_password,
# )
# from app.db.database import get_db
# from app.models.user import User
# from app.schemas.user import UserCreate, UserResponse
# from app.schemas.auth import LoginRequest, Token

# router = APIRouter(prefix="/auth", tags=["auth"]) 


# @router.post("/register", response_model=UserResponse)
# def register(payload: UserCreate, db: Session = Depends(get_db)):
#     existing = db.query(User).filter(User.email == payload.email).first()
#     if existing:
#         raise BadRequestException(message="Email đã được sử dụng")

#     user = User(
#         email=payload.email,
#         full_name=payload.full_name,
#         password_hash=hash_password(payload.password),
#     )
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     return user


# @router.post("/login", response_model=Token)
# def login(payload: LoginRequest, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.email == payload.email).first()
#     if not user or not verify_password(payload.password, user.password_hash):
#         raise BadRequestException(message="Email hoặc mật khẩu không đúng")
#     if not user.is_active:
#         raise BadRequestException(message="Tài khoản đã bị vô hiệu hóa")

#     access_token = create_access_token({"sub": str(user.id), "role": user.role})
#     refresh_token = create_refresh_token({"sub": str(user.id), "role": user.role})
#     return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}


# @router.post("/refresh", response_model=Token)
# def refresh_token_endpoint(payload: Dict[str, str], db: Session = Depends(get_db)):
#     """Expect payload: {"refresh_token": "..."}  """
#     token = payload.get("refresh_token")
#     if not token:
#         raise BadRequestException(message="refresh_token is required")

#     data = decode_token(token)
#     if not data or data.get("type") != "refresh":
#         raise BadRequestException(message="Invalid refresh token")

#     user_id = data.get("sub")
#     user = db.query(User).filter(User.id == int(user_id)).first()
#     if not user:
#         raise BadRequestException(message="User not found")
#     if not user.is_active:
#         raise BadRequestException(message="User is not active")

#     access_token = create_access_token({"sub": str(user.id), "role": user.role})
#     refresh_token = create_refresh_token({"sub": str(user.id), "role": user.role})
#     return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}
