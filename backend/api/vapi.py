from fastapi import APIRouter

router = APIRouter()


@router.post("/vapi")
def vapi_webhook(
    payload: dict
):

    return {
        "message": "vapi webhook"
    }