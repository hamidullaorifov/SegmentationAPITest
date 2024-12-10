import os
from pyngrok import ngrok
from fastapi import FastAPI
from dotenv import load_dotenv
from api.endpoints import segmentation, evaluation
from core.config import TEMP_FILES, TRAINING_RESULTS_FOLDER, STATIC_FILES
from fastapi.staticfiles import StaticFiles
from services.file_services import save_file_to_db

os.environ['nnUNet_preprocessed'] = os.path.join(TEMP_FILES, 'preprocessed')
os.environ['RESULTS_FOLDER'] = TRAINING_RESULTS_FOLDER

load_dotenv()

# nest_asyncio.apply()
app = FastAPI()
os.makedirs(STATIC_FILES, exist_ok=True)
app.mount(STATIC_FILES, StaticFiles(directory=STATIC_FILES), name="files")

@app.get("/")
async def hello_world():
    file_path = os.path.join(TEMP_FILES,'files','nifti','BraTS20-Training-008-t1ce','1_postprocessing_0000.nii.gz')
    result = await save_file_to_db(file_path, 'test_file.nii')
    print(result)
    return {"message":"123"}


app.include_router(segmentation.router)
app.include_router(evaluation.router)

ngrok.set_auth_token(token='2cWwv5uMeHXGNtquH0vNa0REn2K_7BeDTmcs2BFXG1UW8Fsdk')
public_url = ngrok.connect(8000)
print("Public URL:", public_url)
