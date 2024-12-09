from bson import ObjectId
from pydantic import BaseModel, Field
from typing import List
from enum import Enum
from datetime import datetime


class Accuracy(str, Enum):
    Correct = "Correct"
    PartiallyCorrect = "PartiallyCorrect"
    Incorrect = "Incorrect"

class CaseSchema(BaseModel):
    accuracy: Accuracy
    comment: str

class CaseResponseSchema(BaseModel):
    case_id: str
    accuracy: Accuracy
    comment: str
    date_time: datetime



class EvaluationSchema(BaseModel):
    patient_id : str
    cases: List[CaseSchema] = []

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "patient_id": "12345",
                "cases": [
                    {
                        "accuracy": "Correct",
                        "comment": "Diagnosis is accurate."
                    }
                ]
            }
        }


class EvaluationResponseSchema(BaseModel):
    id : str = Field(alias='_id')
    patient_id : str
    cases: List[CaseResponseSchema] = []

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "674eee36328cf6f64ca083df",
                "patient_id": "12345",
                "cases": [
                    {
                        "case_id": "674eee36328cf6f64ca083de",
                        "accuracy": "Correct",
                        "comment": "Diagnosis is accurate.",
                        "date_time": "2024-12-03T16:40:34.319000"
                    }
                ]
            }
        }
