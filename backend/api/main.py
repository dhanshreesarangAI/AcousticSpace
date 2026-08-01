from fastapi import FastAPI
from backend.api.routes import router
from backend.api.database import engine, Base
from backend.api import models_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AcousticSpace API")
app.include_router(router)

@app.get("/")
def health_check():
    return {"status": "AcousticSpace API is running"}