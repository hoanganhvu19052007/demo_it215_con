from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

# Không hard-code URL nữa — đọc từ .env qua settings
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

sessionlocal = sessionmaker(autoflush=False, bind=engine, expire_on_commit=False)

Base = declarative_base()


def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()


def check_db_connection() -> bool:
    """Kiểm tra kết nối DB thành công hay không."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


def init_db() -> None:
    """Tạo bảng nếu chưa tồn tại (đủ dùng cho bài tập; project thật nên dùng Alembic)."""
    from app import models  # noqa: F401  (import để SQLAlchemy nhận diện hết model trước khi create_all)

    Base.metadata.create_all(bind=engine)
