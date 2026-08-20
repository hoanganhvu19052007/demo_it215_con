from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.db.database import get_db
from app.models.user import User

# FastAPI lấy JWT từ:
# Authorization: Bearer <token>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Lấy user hiện tại từ JWT.

    Quy trình:
    1. Lấy token từ Authorization header.
    2. Decode và kiểm tra token.
    3. Kiểm tra token phải là access token.
    4. Lấy user_id từ token.
    5. Tìm user trong database.
    6. Kiểm tra tài khoản có active không.
    """

    # Decode JWT
    data = decode_token(token)

    if not data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không hợp lệ hoặc đã hết hạn",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Chỉ Access Token mới được dùng
    # để truy cập API
    if data.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không hợp lệ",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Lấy user ID từ JWT
    user_id = data.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không chứa user ID",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Tìm user trong database
    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID không hợp lệ",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Không tìm thấy người dùng",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # User bị khóa / inactive
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tài khoản đã bị vô hiệu hóa",
        )

    return user
