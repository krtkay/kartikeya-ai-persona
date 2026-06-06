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

    message = payload.get(
        "message",
        ""
    )

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

        message = f"""
Conversation History:

{conversation}

Current Question:

{message}
"""

    answer = rag.answer_question(
        message
    )

    return {
        "answer": answer
    }