from fastapi import FastAPI
from backend.api.routes import router

app = FastAPI(title="AcousticSpace API")

app.include_router(router)

@app.get("/")
def health_check():
    return {"status": "AcousticSpace API is running"}