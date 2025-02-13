# backend/api/routes.py
from fastapi import APIRouter, UploadFile, File, Form

from agents.supervisor import SupervisorAgent

router = APIRouter()
supervisor = SupervisorAgent()

@router.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    # Save the uploaded file temporarily
    file_location = f"temp/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())

    prediction, confidence = supervisor.handle_image_prediction(file_location)
    # Optionally, delete the file after prediction
    return {"prediction": prediction, "confidence": confidence}

@router.post("/book_appointment")
async def book_appointment(patient_id: int = Form(...), date: str = Form(...), time: str = Form(...)):
    result =  supervisor.handle_book_appointment(patient_id, date, time)
    return result

@router.get("/search_info")
async def search_info(query: str):
    result = supervisor.handle_information_search(query)
    return result