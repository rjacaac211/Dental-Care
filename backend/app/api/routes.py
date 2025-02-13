# backend/app/api/routes.py
import os
from fastapi import APIRouter, UploadFile, File
from app.agents.supervisor_agent import SupervisorAgent

router = APIRouter()
supervisor = SupervisorAgent()

@router.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    temp_dir = "temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    file_location = os.path.join(temp_dir, file.filename)
    with open(file_location, "wb") as f:
        content = await file.read()
        f.write(content)
    print(f"File saved to: {file_location} (Size: {len(content)} bytes)")
    
    try:
        prediction, confidence = supervisor.handle_image_prediction(file_location)
    except Exception as e:
        # Log the detailed exception for debugging purposes
        print(f"Error during prediction: {e}")
        # For debugging, return the full error message (remove this in production)
        return {"error": f"Error in prediction: {str(e)}"}
    
    # Optionally, you can comment out file removal for debugging so you can inspect the file
    os.remove(file_location)
    return {"prediction": prediction, "confidence": confidence}


# @router.post("/book_appointment")
# async def book_appointment(patient_id: int = Form(...), date: str = Form(...), time: str = Form(...)):
#     result =  supervisor.handle_book_appointment(patient_id, date, time)
#     return result

# @router.get("/search_info")
# async def search_info(query: str):
#     result = supervisor.handle_information_search(query)
#     return result