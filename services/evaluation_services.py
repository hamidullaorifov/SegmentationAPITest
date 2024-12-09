from db.setup import db
from models.evaluations import Evaluation
from bson import ObjectId
from fastapi.exceptions import HTTPException

evaluations_collection = db['evaluations']

async def add_evaluation(evaluation_data: dict) -> dict:

    result = await evaluations_collection.insert_one(evaluation_data)
    new_evaluation = await evaluations_collection.find_one({"_id": result.inserted_id})
    return {
        "id": str(new_evaluation["_id"]),
        "patient_id": new_evaluation["patient_id"],
        "cases": new_evaluation.get("cases", [])
    }

async def evaluation_exists(patient_id: str) -> bool:
    
    evaluation = await evaluations_collection.find_one({"patient_id": patient_id})
    return evaluation is not None 


async def get_evaluation_with_cases(patient_id: str) -> dict|None:
    evaluation = await evaluations_collection.find_one({"patient_id": patient_id})
    if evaluation:
        return {
            "id": str(evaluation["_id"]),
            "patient_id": evaluation["patient_id"],
            "cases": evaluation.get("cases", [])
        }
    return evaluation

async def delete_evaluation(evaluation_id: str):
    result = await evaluations_collection.delete_one({"_id": ObjectId(evaluation_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    return result

async def add_case_to_evaluation(patient_id: str, case_data: dict) -> dict|None:
    update_result = await evaluations_collection.update_one(
        {"patient_id": patient_id},
        {"$push": {"cases": case_data}}
    )
    if update_result.modified_count == 0:
        return None
    return case_data


async def update_case(case_id: str, case_update: dict) -> dict:
    
    evaluation = await evaluations_collection.find_one({"cases.case_id": case_id})
    if not evaluation:
        raise HTTPException(status_code=404, detail=f"Case with ID {case_id} not found")

    # remove case_id to keep case_id unchanged
    if "case_id" in case_update:
        del case_update["case_id"]

    update_fields = {f"cases.$.{key}": value for key, value in case_update.items()}
    print("Update fields:", update_fields)
    if not update_fields:
        raise HTTPException(status_code=400, detail="No fields provided to update")

    result = await evaluations_collection.update_one(
        {"cases.case_id": case_id},
        {"$set": update_fields}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail=f"Failed to update case with ID {case_id}")

    updated_evaluation = await evaluations_collection.find_one({"cases.case_id": case_id})
    if not updated_evaluation:
        raise HTTPException(status_code=500, detail="Unexpected error after updating case")
    
    updated_case = next((case for case in updated_evaluation["cases"] if case["case_id"] == case_id), None)
    if not updated_case:
        raise HTTPException(status_code=500, detail="Failed to retrieve the updated case data")
    
    return updated_case


async def remove_case(case_id: str) -> dict:
    evaluation = await evaluations_collection.find_one({"cases.case_id": case_id})
    if not evaluation:
        raise HTTPException(status_code=404, detail=f"Case with ID {case_id} not found")

    result = await evaluations_collection.update_one(
        {"_id": evaluation["_id"]},
        {"$pull": {"cases": {"case_id": case_id}}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail=f"Failed to remove case with ID {case_id}")

    return {"detail": f"Case with ID {case_id} has been successfully removed"}