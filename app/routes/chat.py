from fastapi import APIRouter

from app.ai.graph import student_graph
from app.schemas.chat import ChatRequest, ChatResponse


router = APIRouter(
    prefix="/chat",
    tags=["🤖 AI Chatbot"]
)


@router.post(
    "/",
    response_model=ChatResponse,
    summary="🤖 Ask Student Database AI",
    description="Ask questions about students using the LangGraph AI system."
)
def chat(request: ChatRequest):
    result = student_graph.invoke(
        {
            "message": request.message,
            "response": ""
        }
    )

    return {
        "response": result["response"]
    }