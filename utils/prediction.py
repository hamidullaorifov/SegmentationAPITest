import os

from nnunet.inference.predict import predict_from_folder
from core.config import TRAINING_RESULTS_FOLDER
from dotenv import load_dotenv
import subprocess


os.environ['RESULTS_FOLDER'] = TRAINING_RESULTS_FOLDER


def predict(nifti_output_path, prediction_result_folder):
    print("Prediction started...")
    model_path = "results/nnUNet/3d_fullres/Task01_BraTS_onlyT1ce/nnUNetTrainer__nnUNetPlans/fold_0/model_best.model"
    
    subprocess.run([
        'nnUNet_predict',
        '-i', nifti_output_path,               
        '-o', prediction_result_folder,        
        '-m', '3d_fullres',
        '-t', 'Task01_BraTS_onlyT1ce',                   
        '-f', '0',                             
        '--num_threads_preprocessing', '2',
        '--num_threads_nifti_save', '1',
    ])

