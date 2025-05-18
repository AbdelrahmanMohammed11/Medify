from fastapi import APIRouter, FastAPI, Depends, UploadFile
import os
from helpers.config import get_settings , Settings
from controllers import DataController

data_router = APIRouter(prefix="/base/data",
                        tags=["data"])

@data_router.get("/upload/")
async def upload_data(file: UploadFile,
                       app_settings: Settings = Depends(get_settings)):
    # Check if the file type is allowed
    is_valid_file = DataController().validate_uploaded_file(file = file)



    # implementation of the logic to handle the data upload in controllers
    # For now, we will just return a success message
    return  is_valid_file