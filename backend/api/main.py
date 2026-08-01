from fastapi import FastAPI
from backend.api.routes import router
<<<<<<< HEAD
=======

app = FastAPI(title="AcousticSpace API")
>>>>>>> d818925c281f65671570ea526f3808d51d04b198

app = FastAPI(title="AcousticSpace API")
app.include_router(router)

@app.get("/")
def health_check():
    return {"status": "AcousticSpace API is running"}