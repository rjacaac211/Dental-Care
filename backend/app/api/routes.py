import os
import httpx
from datetime import datetime
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel

from app.core.oral_disease_classifier import OralDiseaseClassifier
from app.core.agent import run_agent
from backend.app.core.chat_history_db import db

router = APIRouter()

# ----------------- Chatbot Endpoint ----------------- #

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

# ----------------- Save Chat History Endpoint ----------------- #
class ChatMessage(BaseModel):
    session_id: str
    sender: str
    message: str

@router.post("/save_chat")
async def save_chat_history(chat: ChatMessage):
    print("Received chat:", chat)
    chat_dict = chat.dict()
    chat_dict["timestamp"] = datetime.utcnow()
    
    result = await db.chat_history.insert_one(chat_dict)
    if result.inserted_id:
        return {"message": "Chat saved successfully", "id": str(result.inserted_id)}
    raise HTTPException(status_code=500, detail="Failed to save chat history")

@router.get("/chat_history/{session_id}")
async def get_chat_history(session_id: str):
    history = await db.chat_history.find({"session_id": session_id}).to_list(length=100)
    # Convert MongoDB-specific types to JSON-serializable types
    for doc in history:
        doc["_id"] = str(doc["_id"])
        if "timestamp" in doc:
            doc["timestamp"] = str(doc["timestamp"])
    return {"chat_history": history}

# ----------------- Speech-to-Text Endpoint ----------------- #
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
if not DEEPGRAM_API_KEY:
    print("WARNING: DEEPGRAM_API_KEY is not set. STT endpoint will fail if called.")

@router.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
    session_id: str = Form(...)
):
    """
    Receives an audio file (e.g. from the frontend),
    calls Deepgram for transcription, and returns the transcript.
    """
    # Read the raw audio bytes
    audio_bytes = await file.read()
    if not audio_bytes:
        raise HTTPException(status_code=400, detail="No audio data received.")

    if not DEEPGRAM_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="Deepgram API key is missing on the server."
        )

    # Example: Using Deepgram's /listen endpoint
    headers = {
        "Authorization": f"Token {DEEPGRAM_API_KEY}",
        "Content-Type": "application/octet-stream"
    }

    params = {
        "model": "nova",        # or 'general', etc.
        "punctuate": "true",
        # "language": "en",     # optionally specify language
        # Additional STT params as needed...
    }

    # Make async call to Deepgram
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.deepgram.com/v1/listen",
            headers=headers,
            params=params,
            content=audio_bytes  # raw audio
        )

    if response.status_code != 200:
        print("Deepgram error:", response.text)
        raise HTTPException(
            status_code=500,
            detail=f"Deepgram API error: {response.text}"
        )

    data = response.json()
    # Extract transcript from Deepgram response
    transcript = (
        data.get("results", {})
            .get("channels", [{}])[0]
            .get("alternatives", [{}])[0]
            .get("transcript", "")
    )

    return {"transcript": transcript}

# ----------------- CV / Image Prediction Endpoint ----------------- #
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