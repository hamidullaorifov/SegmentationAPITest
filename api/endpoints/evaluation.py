import os
from typing import List

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from models.evaluations import Evaluation, Case
from schemas.evaluations import EvaluationSchema, CaseSchema, EvaluationResponseSchema, CaseResponseSchema
from services.evaluation_services import (
    add_evaluation, 
    get_evaluation_with_cases,
    delete_evaluation, 
    add_case_to_evaluation, 
    evaluation_exists, 
    update_case, 
    remove_case)

router = APIRouter(prefix='/evaluations',tags=['Evaluation'])


@router.post('/', response_model=EvaluationResponseSchema, status_code=201)
async def create_evaluation(evaluation: EvaluationSchema):
    if await evaluation_exists(evaluation.patient_id):
        raise HTTPException(status_code=400, detail="Evaluation exists with this patient_id")
    evaluation_data = Evaluation(**evaluation.model_dump()).model_dump()
    
    new_evaluation = await add_evaluation(evaluation_data)
    if not new_evaluation:
        raise HTTPException(status_code=500, detail="Failed to create evaluation")
    return new_evaluation


@router.get('/{patient_id}', response_model=EvaluationResponseSchema)
async def get_evaluation(patient_id: str):
    evaluation = await get_evaluation_with_cases(patient_id)
    
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    return evaluation

@router.delete('/{evaluation_id}', status_code=204)
async def remove_evaluation(evaluation_id: str):
    result = await delete_evaluation(evaluation_id)
    print(result)
    return {"message":f"Evaluation successfully deleted with ID: {evaluation_id}"}
    

@router.post("/{patient_id}/cases/", response_model=CaseResponseSchema)
async def create_case(patient_id: str, case: CaseSchema):
    case_data = Case(**case.model_dump()).model_dump()
    new_case = await add_case_to_evaluation(patient_id, case_data)
    if not new_case:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    return new_case


@router.put('/cases/{case_id}')
async def update_case_by_id(case_id: str, case: CaseSchema):
    case_update = Case(**case.model_dump()).model_dump()
    return await update_case(case_id, case_update)
    

@router.delete('/cases/{case_id}', status_code=204)
async def delete_case(case_id: str):
    return await remove_case(case_id)