from fastapi import APIRouter, UploadFile, File

router = APIRouter()

@router.get("/health")
def health():
    return {
        "status": "healthy"
    }

@router.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "prediction": "DEEPFAKE",
        "confidence_score": 87.4,
        "rir_mismatch": "HIGH",
        "breathing": "UNNATURAL"
    }