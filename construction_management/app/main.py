from fastapi import FastAPI

from router.auth import router as auth_router
from router.health import router as health_router
from router.site import router as site_router
from router.user import router as user_router
from router.work_item import router as work_item_router
from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.db.database import check_db_connection, init_db

app = FastAPI(title="Construction Management API", debug=settings.DEBUG)

register_exception_handlers(app)
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(site_router)
app.include_router(work_item_router)


@app.on_event("startup")
def on_startup():
    if not check_db_connection():
        raise RuntimeError("Không thể kết nối database khi khởi động app")
    init_db()
    print("Database khởi tạo thành công")


@app.get("/")
def get_root():
    return {"message": "Đã khởi động API thành công"}
