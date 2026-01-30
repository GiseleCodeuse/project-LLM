from fastapi import APIRouter
from pydantic import BaseModel
from app.services.llm_service import get_llm_response

router = APIRouter()

class MessageRequest(BaseModel):
    message: str

@router.post("/chat")
async def chat(request: MessageRequest):
    reply = await get_llm_response(request.message)
    return {"reply": reply}