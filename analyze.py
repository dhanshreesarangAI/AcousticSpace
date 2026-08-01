from fastapi import APIRouter, UploadFile, File, HTTPException
from app.utils.ml_pipeline import DeepfakeDetector
import librosa
import io

router = APIRouter()
detector = DeepfakeDetector("backend/models/saved_model/ast_model.pt")

@router.post("/analyze")
async def analyze_audio(file: UploadFile = File(...)):
    if not file.filename.endswith(".wav"):
        raise HTTPException(status_code=400, detail="Only WAV files supported")

    audio_bytes = await file.read()
    buf = io.BytesIO(audio_bytes)
    y, sr = librosa.load(buf, sr=22050)

    prob = detector.predict(y, sr)
    return {"deepfake_probability": prob}

from fastapi import FastAPI
from app.routes import analyze

app = FastAPI()

app.include_router(analyze.router)
