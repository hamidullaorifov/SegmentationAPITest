from celery import Celery
import os
import zipfile
import shutil


from utils.image_utils import convert_dicom_to_nifti
# from utils.file_utils import validate_zipfile_type, save_upload, extract_zip, cleanup, get_nifti_filename
from core.config import TEMP_ZIP_INPUT_DIR, TEMP_EXTRACTED_DICOM, TEMP_INPUT_NIFTI
from services.file_services import save_file_to_db

celery = Celery(
    __name__,
    broker="redis://localhost:6379/0", 
    backend="redis://localhost:6379/0",
    broker_connection_retry_on_startup=True
)

celery.autodiscover_tasks(['utils'])


celery.conf.update(
    task_track_started=True,  # Track task start
    worker_concurrency=1,  # Single worker concurrency (adjust as needed)
)
