from sqlalchemy.orm import Session
from backend.api.database import get_db
from backend.api.models_db import User
from backend.api.schemas_auth import UserCreate, Token
from backend.api.auth import hash_password, verify_password, create_access_token, get_current_user
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from backend.api.schemas import AnalyzeResponse

router = APIRouter()
@router.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered")
    new_user = User(username=user.username, hashed_password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    token = create_access_token({"sub": new_user.username})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = create_access_token({"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}

ALLOWED_EXTENSIONS = {".wav", ".mp3", ".flac"}
MAX_FILE_SIZE_MB = 20
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_audio(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
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