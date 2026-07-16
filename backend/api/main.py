from fastapi import FastAPI
from routes import router

app = FastAPI(
    title="AcousticSpace API",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
def home():
    return {
        "message": "AcousticSpace Backend is Running 🚀"
    }