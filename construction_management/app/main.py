from fastapi import FastAPI

from app.core.config import settings
from app.core.exceptions import register_exception_handlers

from app.router.auth import router as auth_router
from app.router.health import router as health_router
from app.router.user import router as user_router

# Nếu sau này hoàn thiện 2 router này
# thì bỏ comment để đăng ký:
#
# from app.router.site import router as site_router
# from app.router.work_item import router as work_item_router


# =========================================================
# CREATE APP
# =========================================================

app = FastAPI(
    title="Construction Management API",
    debug=settings.DEBUG,
)


# =========================================================
# EXCEPTION HANDLERS
# =========================================================

register_exception_handlers(app)


# =========================================================
# ROUTERS
# =========================================================

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(user_router)

# Khi hoàn thiện:
# app.include_router(site_router)
# app.include_router(work_item_router)


# =========================================================
# ROOT
# =========================================================


@app.get("/")
def root():
    return {"message": "Construction Management API is running"}
