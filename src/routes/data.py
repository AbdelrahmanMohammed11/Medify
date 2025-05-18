from fastapi import APIRouter, FastAPI, Depends, UploadFile, status
from fastapi.responses import JSONResponse
import os
from helpers.config import get_settings , Settings
from controllers import DataController , ProjectController
from models import ResponseStatus
import aiofiles


data_router = APIRouter(prefix="/base/data",
                        tags=["data"])

@data_router.get("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile,
                       app_settings: Settings = Depends(get_settings)):
    
    data_controller = DataController()

    # Check if the file type is allowed
    is_valid_file , result_message = data_controller.validate_uploaded_file(file = file)



    # implementation of the logic to handle the data upload in controllers
    # For now, we will just return a success message
    if not is_valid_file:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"Error": result_message})
    
    
        
    # Save the file to the project directory
    project_directory = ProjectController().make_dir_file(project_id=project_id)
    file_path = data_controller.generate_cleaned_file_path(
        original_filename=file.filename,
        project_id=project_id
    )
    
    async with aiofiles.open(file_path, 'wb') as file_out:
        while chunk := await file.read(app_settings.FILE_CHUNK_SIZE):
            await file_out.write(chunk)
    

    return JSONResponse(content={"File uploaded successfully": ResponseStatus.FILE_UPLOADED_SUCCESSFULLY.value})