from fastapi import FastAPI,APIRouter,Depends,UploadFile,status
from fastapi.responses import JSONResponse
import os
from helpers.config import get_settings,Settings
from controllers import DataController,ProjectController
import aiofiles
from models.enums.ResponseEnums import ResponseSignal
import logging

logger = logging.getLogger('uvicorn.error')

file_upload_router = APIRouter(
    prefix="/api/data",
    tags= ['data']
)

@file_upload_router.post("upload_file/{project_id}")
async def upload_files(project_id: str , file:UploadFile,
                    settings: Settings = Depends(get_settings)):
    
    data_controller = DataController()
    is_valid, result_signal = data_controller.validate_updoaded_file(file = file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": result_signal}
        )
    
    project_dir_path = ProjectController().ProjectPath(project_id= project_id)

    file_path, file_code = data_controller.generate_unique_filepath(
        original_name= file.filename, 
        project_id = project_id
        )

    try: 
        async with aiofiles.open(file_path ,"wb") as f:
            while chunk := await file.read(settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)

    except Exception as e:
        logger.error(f"Error while uploading file: {e}")

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal":ResponseSignal.FILE_UPLOAD_FAILED.value}
        )
    
    return JSONResponse(
        content={
            "siganl":ResponseSignal.FILE_UPLOAD_SUCCESS.value,
            "file_code": file_code
        }
    )
