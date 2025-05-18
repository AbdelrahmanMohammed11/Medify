from fastapi import FastAPI

from routes import base
from helpers.config import get_settings

app = FastAPI()
app.include_router(base.base_router)