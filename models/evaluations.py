from bson import ObjectId
from pydantic import BaseModel, Field
from typing import List, Optional, Annotated
from enum import Enum
from datetime import datetime



class Accuracy(str, Enum):
    Correct = "Correct"
    PartiallyCorrect = "PartiallyCorrect"
    Incorrect = "Incorrect"

class Case(BaseModel):
    case_id: str = Field(default_factory=lambda: str(ObjectId())) 
    accuracy: Accuracy
    comment: str
    date_time: datetime = datetime.now()


    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True
        

class Evaluation(BaseModel):
    patient_id : str
    cases: List[Case] = []

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True