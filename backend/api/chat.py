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

    history = payload.get(
        "history",
        []
    )

    if history:

        conversation = ""

        for msg in history[-6:]:

            conversation += (
                f"{msg['role']}: "
                f"{msg['content']}\n"
            )

        question = f"""
Conversation History:

{conversation}

Current Question:

{question}
"""

    answer = rag.answer_question(
        question
    )

    return {
        "response": answer
    }