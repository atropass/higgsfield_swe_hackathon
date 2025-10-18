import json
from typing import Any, Dict

from fastapi import APIRouter
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

from app.agents import get_chat_graph
from app.core.logging import get_logger
from app.schemas.chat import ChatMessage, ChatRequest, ChatResponse, JobDetails

router = APIRouter(prefix="/v1/chat", tags=["chat"])
logger = get_logger(__name__)


def convert_to_langchain_messages(messages: list[ChatMessage]) -> list:
    lc_messages = []

    for msg in messages:
        if msg.role == "user":
            lc_messages.append(HumanMessage(content=msg.content))
        elif msg.role == "assistant":
            lc_messages.append(AIMessage(content=msg.content))

    return lc_messages


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    print("\n" + "="*80)
    print("CHAT REQUEST RECEIVED")
    print("="*80)
    print(f"User Message: {request.message}")
    print(f"History Length: {len(request.conversation_history)} messages")
    print("="*80 + "\n")

    logger.info(
        "chat_request",
        message_length=len(request.message),
        history_length=len(request.conversation_history),
    )

    print("Initializing LangGraph agent...\n")
    graph = await get_chat_graph()

    messages = convert_to_langchain_messages(request.conversation_history)
    messages.append(HumanMessage(content=request.message))

    print(f"Total messages in context: {len(messages)}\n")

    state: Dict[str, Any] = {
        "messages": messages,
    }

    print("Running agent with Gemini...\n")
    result = await graph.ainvoke(state)

    ai_messages = [msg for msg in result["messages"] if isinstance(msg, AIMessage)]
    response_text = ai_messages[-1].content if ai_messages else "I apologize, but I couldn't process your request."

    print("="*80)
    print("AGENT RESPONSE")
    print("="*80)
    print(f"{response_text[:200]}{'...' if len(response_text) > 200 else ''}")
    print("="*80 + "\n")

    job_details = None
    action_performed = None
    tool_messages = [msg for msg in result["messages"] if isinstance(msg, ToolMessage)]

    for tool_msg in reversed(tool_messages):
        try:
            tool_result = json.loads(tool_msg.content)
            if tool_result.get("_higgsfield_job"):
                job_type = tool_result.get("job_type", "")

                if "image-to-video" in job_type:
                    action_performed = "generate_video_from_image"
                elif "text-to-video" in job_type:
                    action_performed = "generate_video"
                elif "text-to-image" in job_type:
                    action_performed = "generate_image"

                job_details = JobDetails(
                    job_set_id=tool_result["job_set_id"],
                    status=tool_result["status"],
                    job_type=job_type,
                    model=tool_result["model"],
                    parameters=tool_result["parameters"],
                    estimated_time="2-5 minutes",
                )

                response_text = tool_result.get("user_message", response_text)

                print(f"Job created: {job_details.job_set_id} ({job_type} with {job_details.model})\n")
                break
        except (json.JSONDecodeError, KeyError):
            continue

    logger.info(
        "chat_response",
        response_length=len(response_text),
        has_job=job_details is not None,
        action=action_performed,
    )

    return ChatResponse(
        message=response_text,
        job_details=job_details,
        action_performed=action_performed,
    )

