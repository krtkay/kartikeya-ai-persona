from fastapi import APIRouter

from backend.rag.rag_engine import (
    RAGEngine
)

router = APIRouter()

rag = RAGEngine()


@router.post("/chat")
def chat(
    payload: dict
):

    question = payload["message"]

    answer = rag.answer_question(
        question
    )

    return {
        "response": answer
    }