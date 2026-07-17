from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.api.schemas import AnalyzeResponse

router = APIRouter()

ALLOWED_EXTENSIONS = {".wav", ".mp3", ".flac"}
MAX_FILE_SIZE_MB = 20
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_audio(file: UploadFile = File(...)):
    if "." not in file.filename:
        raise HTTPException(status_code=400, detail="File has no extension")

    ext = "." + file.filename.rsplit(".", 1)[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}. Allowed: {', '.join(ALLOWED_EXTENSIONS)}")

    audio_bytes = await file.read()

    if len(audio_bytes) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    if len(audio_bytes) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(status_code=413, detail=f"File exceeds {MAX_FILE_SIZE_MB}MB limit")

    # TODO: replace this stub once Dhanshree's pipeline/model are ready
    # 1. Save/pass audio_bytes to backend/pipeline/audio_loader.py
    # 2. Extract RIR + breathing features
    # 3. Run through the AST classifier in backend/models/
    return AnalyzeResponse(
        prediction="DEEPFAKE",
        confidence_score=87.4,
        rir_mismatch="HIGH",
        breathing="UNNATURAL"
    )