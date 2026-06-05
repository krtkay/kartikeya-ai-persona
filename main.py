from fastapi import FastAPI

from backend.api.chat import router as chat_router
from backend.api.scheduling import router as scheduling_router
from backend.api.vapi import router as vapi_router

app = FastAPI(
    title="Kartikeya AI Persona"
)

app.include_router(chat_router)
app.include_router(scheduling_router)
app.include_router(vapi_router)


@app.get("/")
def home():

    return {
        "status": "running",
        "message": "Kartikeya AI Persona Backend"
    }