from fastapi import APIRouter, FastAPI, Depends, UploadFile, status
from fastapi.responses import JSONResponse
import os
from helpers.config import get_settings , Settings
from controllers import DataController

data_router = APIRouter(prefix="/base/data",
                        tags=["data"])

@data_router.get("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile,
                       app_settings: Settings = Depends(get_settings)):
    # Check if the file type is allowed
    is_valid_file , result_message = DataController().validate_uploaded_file(file = file)



    # implementation of the logic to handle the data upload in controllers
    # For now, we will just return a success message
    if not is_valid_file:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"Error": result_message})
        
    
    
    