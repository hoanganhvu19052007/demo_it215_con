from fastapi import Depends, HTTPException, status

from app.dependencies.auth import get_current_user
from app.models.user import User


def require_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Yêu cầu người dùng đã đăng nhập.

    USER và ADMIN đều được phép.
    """

    return current_user


def require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Chỉ ADMIN mới được phép truy cập.
    """

    if current_user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ ADMIN mới có quyền thực hiện thao tác này",
        )

    return current_user
