from fastapi import APIRouter

from backend.rag.rag_engine import (
    RAGEngine
)

router = APIRouter()

rag = RAGEngine()


@router.post("/voice-query")
def voice_query(
    payload: dict
):

    question = payload.get(
        "question",
        ""
    )

    answer = rag.answer_question(
        question
    )

    return {
        "answer": answer
    }