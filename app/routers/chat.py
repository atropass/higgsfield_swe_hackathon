import json
from typing import Any, Dict

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
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


@router.post("/stream")
async def chat_stream(request: ChatRequest) -> StreamingResponse:
    logger.info(
        "chat_stream_request",
        message=request.message[:100],
        history_length=len(request.conversation_history),
    )

    graph = await get_chat_graph()
    messages = convert_to_langchain_messages(request.conversation_history)
    messages.append(HumanMessage(content=request.message))

    state: Dict[str, Any] = {"messages": messages}

    async def event_generator():
        yield "event: status\n" + "data: {\"status\": \"processing\"}\n\n"

        accumulated_text = ""
        latest_job_payload: Dict[str, Any] | None = None

        try:
            async for event in graph.astream_events(state, version="v2"):
                event_type = event.get("event")
                data = event.get("data", {})

                if event_type == "on_chat_model_stream":
                    chunk = data.get("chunk")
                    text = None
                    if hasattr(chunk, "content") and isinstance(chunk.content, str):
                        text = chunk.content
                    elif hasattr(chunk, "text") and isinstance(chunk.text, str):
                        text = chunk.text
                    elif isinstance(chunk, str):
                        text = chunk

                    if text:
                        accumulated_text += text
                        yield "event: token\n" + f"data: {{\"text\": {json.dumps(text)} }}\n\n"

                elif event_type == "on_tool_end":
                    output = data.get("output")
                    try:
                        parsed = json.loads(output) if isinstance(output, str) else output
                        if isinstance(parsed, dict) and parsed.get("_higgsfield_job"):
                            latest_job_payload = parsed
                            job_event = {
                                "job_set_id": parsed.get("job_set_id"),
                                "job_type": parsed.get("job_type"),
                                "model": parsed.get("model"),
                                "status": parsed.get("status"),
                                "parameters": parsed.get("parameters"),
                                "estimated_time": "2-5 minutes",
                            }
                            yield "event: job\n" + f"data: {json.dumps(job_event)}\n\n"
                    except Exception:
                        pass

            final_payload: Dict[str, Any] = {"message": accumulated_text or ""}

            if latest_job_payload:
                job_event = {
                    "job_set_id": latest_job_payload.get("job_set_id"),
                    "job_type": latest_job_payload.get("job_type"),
                    "model": latest_job_payload.get("model"),
                    "status": latest_job_payload.get("status"),
                    "parameters": latest_job_payload.get("parameters"),
                    "estimated_time": "2-5 minutes",
                }
                final_payload["job_details"] = job_event

            yield "event: final\n" + f"data: {json.dumps(final_payload)}\n\n"
            yield "event: done\n" + "data: {}\n\n"

        except Exception as e:
            err = {"message": "Sorry, an error occurred while streaming.", "detail": str(e)}
            yield "event: error\n" + f"data: {json.dumps(err)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
