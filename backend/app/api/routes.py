import os
from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel

from backend.app.core.oral_disease_classifier import OralDiseaseClassifier
from app.core.agent import run_agent

router = APIRouter()

# Add a model for chat request, including session_id
class ChatRequest(BaseModel):
    session_id: str
    message: str

@router.post("/chat")
async def chat_endpoint(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message is required.")

    final_response = run_agent(req.session_id, req.message)
    return {"final_response": final_response}

# Initialize the CVAgent with the model path.
model_path = os.path.join(os.path.dirname(__file__), "../models/oral_disease_model.h5")
cv_agent = OralDiseaseClassifier(model_path)

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
        prediction, confidence = cv_agent.predict(file_location)
    except Exception as e:
        # Log the error for debugging.
        print(f"Error during prediction: {e}")
        return {"error": f"Error in prediction: {str(e)}"}
    
    # Optionally, remove the temporary file after processing.
    os.remove(file_location)
    return {"prediction": prediction, "confidence": confidence}