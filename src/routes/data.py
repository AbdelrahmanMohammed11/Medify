from fastapi import APIRouter, FastAPI, Depends, UploadFile, status, Request
from fastapi.responses import JSONResponse
import os
from helpers.config import get_settings , Settings
from controllers import DataController , ProjectController, ProcessController
from models import ResponseStatus
import aiofiles
import logging
from .schemes.data import MakeRequest
from models.ProjectModel import ProjectModel

logger = logging.getLogger("uvicorn.error")


data_router = APIRouter(prefix="/base/data",
                        tags=["data"])

@data_router.post("/upload/{project_id}")
async def upload_data(request: Request ,project_id: int, file: UploadFile,
                       app_settings: Settings = Depends(get_settings)):
    project_model = ProjectModel(
        db_clint= request.app.database_clint
    )

    project = await project_model.get_project_or_create_new_one(
        project_id=project_id
    )

    data_controller = DataController()

    # Check if the file type is allowed
    is_valid_file , result_message = data_controller.validate_uploaded_file(file = file)



    # implementation of the logic to handle the data upload in controllers
    # For now, we will just return a success message
    if not is_valid_file:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={
                                "Error": result_message
                                })
    
    
        
    # Save the file to the project directory
    project_directory = ProjectController().make_dir_file(project_id=project_id)
    file_path, file_id = data_controller.generate_cleaned_file_path(
        original_filename=file.filename,
        project_id=project_id
    )

    try:

        async with aiofiles.open(file_path, 'wb') as file_out:
            while chunk := await file.read(app_settings.FILE_CHUNK_SIZE):
                await file_out.write(chunk)
    
    
    except Exception as e:
        logger.error(f"Error while uploading file: {e}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content={
                                    "Error:": ResponseStatus.FILE_UPLOADED_FAILED.value
                                    })

    return JSONResponse(
        content={"File uploaded successfully": ResponseStatus.FILE_UPLOADED_SUCCESSFULLY.value,
                 "file_id": file_id,
                 "project_id": str(project.project_id)
                   })





@data_router.post("/process/{project_id}")
async def process_endpoint(project_id: str, 
                        request: MakeRequest):
    """
    Process the data for the given project ID.
    """

    file_id = request.file_id
    chunk_size = request.chunk_size
    overlap = request.overlap

    process_controller = ProcessController(project_id=project_id)
    
    # get the file content
    file_content = process_controller.get_file_content(file_id=file_id)

    
    file_chunks = process_controller.split_file_content(file_content=file_content,
                                                   file_id=file_id,
                                                   chunk_size=chunk_size,
                                                   overlap=overlap)
    if file_chunks is None or len(file_chunks) == 0:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"Error": ResponseStatus.PROCESSING_FAILED.value})
    
    return file_chunks






