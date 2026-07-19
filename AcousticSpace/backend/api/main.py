from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import sys
sys.path.append('../pipeline')
from predict import predict_audio

# Initialize FastAPI app
app = FastAPI(
    title="AcousticSpace API",
    description="Deepfake audio detection using RIR analysis",
    version="1.0.0"
)

# Allow React frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/health")
def health_check():
    """
    Check if server is running
    """
    return {
        "status": "running",
        "message": "AcousticSpace API is live!"
    }

@app.post("/analyze")
async def analyze_audio(file: UploadFile = File(...)):
    """
    Receive audio file and return prediction
    """
    # Save uploaded file temporarily
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run prediction pipeline
    result = predict_audio(temp_path)

    # Delete temporary file
    os.remove(temp_path)

    return result