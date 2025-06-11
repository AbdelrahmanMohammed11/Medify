from fastapi import APIRouter, FastAPI, Depends, UploadFile, status, Request
from fastapi.responses import JSONResponse
import os
from helpers.config import get_settings , Settings
from controllers import DataController , ProjectController, ProcessController
from models import ResponseStatus
from models.enums.AssetTypeEnums import AssetTypeEnums
import aiofiles
import logging
from .schemes.data import MakeRequest
from models.ProjectModel import ProjectModel
from models.DataChunkModel import DataChunkModel
from models.DB_Schema.Med_Rag.schemes import DataChunk
from models.DB_Schema.Med_Rag.schemes import Project
from models.DB_Schema.Med_Rag.schemes import Asset
from models.AssetModel import AssetModel
from controllers import NLPController




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


    # Create an asset record in the database
    asset_model = AssetModel(
        db_clint= request.app.database_clint
    )

    asset = Asset(
        asset_project_id = int(project.project_id),
        asset_type = AssetTypeEnums.FILE.value,
        asset_name = file_id,
        asset_size = os.path.getsize(file_path),
        asset_metadata = {
            "original_filename": file.filename,
            "file_path": file_path
        })

    # Save the asset to the database
    asset_rec = await asset_model.create_asset(asset=asset)


    return JSONResponse(
        content={"File uploaded successfully": ResponseStatus.FILE_UPLOADED_SUCCESSFULLY.value,
                 "file_id": asset_rec.asset_id,
                 "project_id": str(project.project_id)
                   })





@data_router.post("/process/{project_id}")
async def process_endpoint(apprequest: Request, project_id: str, 
                        request: MakeRequest):
    """
    Process the data for the given project ID.
    """

    # Extract the parameters from the request
    chunk_size = request.chunk_size
    overlap = request.overlap
    do_reset = request.do_reset


    project_model = ProjectModel(
        db_clint= apprequest.app.database_clint
    )

    chunk_model = DataChunkModel(
            db_clint= apprequest.app.database_clint
        )

    project = await project_model.get_project_or_create_new_one(
        project_id=int(project_id)
    )
    
    nlp_controller = NLPController(
        vectordb_client = apprequest.app.vectordb_client,
        generation_client=apprequest.app.generation_client,
        embedding_client=apprequest.app.embedding_client,
        template_parser=apprequest.app.template_parser
    )

    


    """

    the next block of code handles the retrieval of file assets associated with a given project.

    Pipeline:
    1. Initialize an instance of the AssetModel using the database client from the request context.
    2. Check if a specific `file_id` is provided in the incoming request:
        - If yes, fetch the corresponding asset from the database.
        - If the asset is not found, return a 400 error response indicating an invalid file ID.
        - If found, store the file ID for further processing.
    3. If no `file_id` is provided:
        - Retrieve all file-type assets associated with the project.
        - Build a dictionary mapping asset IDs to asset names.
    4. If no assets are found (either specific or all), return a 400 error response indicating that no files were found.


    """

    # Create an instance of the AssetModel
    asset_model = AssetModel(
        db_clint= apprequest.app.database_clint
        )




    file_name_and_id = {}

    if request.file_id:
        asset_record = await asset_model.get_asset(
            asset_project_id=int(project.project_id),
            asset_name=request.file_id
        )
        if asset_record is None:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content={"Error": ResponseStatus.FILE_ID_ERROR.value})
        
        # If a specific file_id is provided, use it directly

        file_name_and_id = {
            asset_record.asset_id: asset_record.asset_name
        }
        
    else:
        
        # Get all file assets for the project
        file_assets = await asset_model.get_all_assets_of_project(
            asset_project_id=int(project.project_id),
            asset_type=AssetTypeEnums.FILE.value
        )

        # Extract the file names and IDs from the assets
        file_name_and_id = {
            records.asset_id: records.asset_name for records in file_assets
        }

    if len(file_name_and_id) == 0:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"Error": ResponseStatus.NO_FILES_FOUND.value})




    process_controller = ProcessController(project_id=project_id)

    records = 0
    num_of_files = 0
    
    if do_reset== 1:
        #delete associated vectors collection
        collection_name = nlp_controller.create_collection_name(project_id=project.project_id)
        _ = await apprequest.app.vectordb_client.delete_collection(collection_name=collection_name)
        
        #delete associated Chunks
        _ = await chunk_model.delete_chunk_by_projectID(
            project_id=int(project.project_id)
        )
        

    for asset_id, file_id in file_name_and_id.items():
        # get the file content
        file_content = process_controller.get_file_content(file_id=file_id)
        if file_content is None or len(file_content) == 0:
            logger.error(f"File content is empty or None for file_id: {file_id}")
            continue

        
        file_chunks = process_controller.split_file_content(file_content=file_content,
                                                    file_id=file_id,
                                                    chunk_size=chunk_size,
                                                    overlap=overlap)
        if file_chunks is None or len(file_chunks) == 0:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content={"Error": ResponseStatus.PROCESSING_FAILED.value})
        
        # Save the chunks to the database



        project = await project_model.get_project_or_create_new_one(
            project_id=int(project_id)
        )
        
        # create the chunks
        chunks = [
            DataChunk(
                    chunk_content=chunk.page_content,
                    chunk_project_id= project.project_id,
                    chunk_metadata= chunk.metadata,
                    chunk_asset_id= asset_id,
                    #chunk_size = os.path.getsize(file_id),
                )
            for i, chunk in enumerate(file_chunks)
        ]

        
        # insert the chunks into the database
        records += await chunk_model.insert_many_chunks(chunks)
        num_of_files += 1

    return JSONResponse(
        content={
            "File processed successfully": ResponseStatus.PROCESSING_SUCCESS.value,
            "Chunks": records,
            'Number of files processed': num_of_files,
                      })

    



