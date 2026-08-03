from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    file: str = Field(..., description="Filename or path of the uploaded audio file")


class AnalyzeResponse(BaseModel):
    prediction: str
    confidence_score: float
    rir_mismatch: str
    breathing: str