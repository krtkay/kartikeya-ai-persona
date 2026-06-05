from fastapi import FastAPI

from backend.db.database import engine
from backend.db.database import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Persona Backend"
)


@app.get("/")
def root():

    return {
        "status": "running"
    }