from pydantic import BaseModel


class AnalyzeResponse(BaseModel):
    prediction: str
    confidence_score: float
    rir_mismatch: str
    breathing: str