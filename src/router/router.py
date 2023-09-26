from fastapi import APIRouter
from src.router.image_router import img_router
router = APIRouter(prefix="/api/v1")
router.include_router(img_router, tags=["image"])