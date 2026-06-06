from fastapi import APIRouter

from backend.rag.rag_engine import (
    RAGEngine
)

router = APIRouter()

rag = RAGEngine()


@router.post("/vapi")
def vapi_webhook(
    payload: dict
):

    question = payload.get(
        "message",
        ""
    )

    answer = rag.answer_question(
        question
    )

    return {
        "answer": answer
    }