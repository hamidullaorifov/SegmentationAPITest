import os
from typing import List

from fastapi import APIRouter, Request, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException


from core.config import TEMP_ZIP_INPUT_DIR
from utils.file_utils import validate_zipfile_type, save_upload
from utils.tasks import process_file

router = APIRouter(tags=['Segmentation'])

@router.post("/segmentation/task/", status_code=200)
async def upload_file(file: UploadFile = File(...)):
    
    # Check if uploaded file is a ZIP file
    validate_zipfile_type(file)

    patient_id = os.path.splitext(file.filename)[0]
    zip_path = os.path.join(TEMP_ZIP_INPUT_DIR, file.filename)

    # Create necessary directories
    os.makedirs(TEMP_ZIP_INPUT_DIR, exist_ok=True)

    # Process the upload: save, extract, convert, and clean up
    await save_upload(file, zip_path)
    task = process_file.delay(zip_path, patient_id)
    return {"message": "File processing started", "task_id": task.id}


@router.get("/segmentation/status/{task_id}")
async def get_task_status(request: Request, task_id: str):
    task_result = process_file.AsyncResult(task_id)
    if task_result.state == "SUCCESS":
        file_path = task_result.result['file_path'][1:]  # Removing leading slash
        full_file_path = f"{request.base_url}{file_path}" # file_path starts with /
        return {"status": "Completed", "file_path": full_file_path}
    else:
        return {"status": task_result.state}


