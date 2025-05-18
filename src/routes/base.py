from fastapi import APIRouter, FastAPI 
import os
from helpers.config import get_settings


base_router = APIRouter(prefix="/base",
                        tags=["base"])
@base_router.get("/")
async def read_root():
    app_settings = get_settings()
    app_name = app_settings.APP_NAME
    app_version = app_settings.APP_VERSION
    return {"app_name": app_name, "app_version": app_version}