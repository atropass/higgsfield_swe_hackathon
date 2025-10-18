import json
from typing import Any, Dict

from fastapi import APIRouter
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

from app.agents import get_chat_graph
from app.core.logging import get_logger
from app.schemas.chat import ChatMessage, ChatRequest, ChatResponse, JobDetails
from app.schemas.enums import ActionType, JobType

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
    logger.info(
        "chat_request",
        message=request.message[:100],
        history_length=len(request.conversation_history),
    )

    graph = await get_chat_graph()
    messages = convert_to_langchain_messages(request.conversation_history)
    messages.append(HumanMessage(content=request.message))

    state: Dict[str, Any] = {"messages": messages}

    try:
        result = await graph.ainvoke(state)
    except Exception as e:
        logger.error("agent_error", error=str(e))
        return ChatResponse(
            message="Sorry, I encountered an error. Please try again!",
            job_details=None,
            action_performed=None,
        )

    ai_messages = [msg for msg in result["messages"] if isinstance(msg, AIMessage)]
    response_text = ai_messages[-1].content if ai_messages else "I apologize, but I couldn't process your request."

    job_details = None
    action_performed = None

    ACTION_MAP = {
        JobType.IMAGE_TO_VIDEO.value: ActionType.GENERATE_VIDEO_FROM_IMAGE.value,
        JobType.TEXT_TO_VIDEO.value: ActionType.GENERATE_VIDEO.value,
        JobType.TEXT_TO_IMAGE.value: ActionType.GENERATE_IMAGE.value,
    }

    tool_messages = [msg for msg in result["messages"] if isinstance(msg, ToolMessage)]

    for tool_msg in reversed(tool_messages):
        try:
            tool_result = json.loads(tool_msg.content)
            if tool_result.get("_higgsfield_job"):
                job_type = tool_result["job_type"]
                action_performed = ACTION_MAP.get(job_type)

                job_details = JobDetails(
                    job_set_id=tool_result["job_set_id"],
                    status=tool_result["status"],
                    job_type=job_type,
                    model=tool_result["model"],
                    parameters=tool_result["parameters"],
                    estimated_time="2-5 minutes",
                )

                logger.info("job_created", job_id=job_details.job_set_id, job_type=job_type)
                break
        except (json.JSONDecodeError, KeyError):
            continue

    return ChatResponse(
        message=response_text,
        job_details=job_details,
        action_performed=action_performed,
    )

