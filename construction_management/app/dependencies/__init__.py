from typing import Optional

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.exceptions import BadRequestException
from app.core.security import decode_token
from app.db.database import get_db
from app.models.user import User


def get_current_user_from_token(token: str, db: Session = Depends(get_db)) -> User:
    data = decode_token(token)
    if not data:
        raise BadRequestException(message="Invalid token")
    user_id = data.get("sub")
    if not user_id:
        raise BadRequestException(message="Invalid token payload")
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise BadRequestException(message="User not found")
    return user
