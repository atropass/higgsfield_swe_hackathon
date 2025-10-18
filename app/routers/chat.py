"""Chat endpoint with LangGraph and Gemini."""

import json
import re
from typing import Any, Dict

from fastapi import APIRouter
from langchain_core.messages import AIMessage, HumanMessage

from app.agents import get_chat_graph
from app.core.logging import get_logger
from app.schemas.chat import ChatMessage, ChatRequest, ChatResponse, JobDetails

router = APIRouter(prefix="/v1/chat", tags=["chat"])
logger = get_logger(__name__)


def convert_to_langchain_messages(messages: list[ChatMessage]) -> list:
    """Convert API messages to LangChain messages."""
    lc_messages = []

    for msg in messages:
        if msg.role == "user":
            lc_messages.append(HumanMessage(content=msg.content))
        elif msg.role == "assistant":
            lc_messages.append(AIMessage(content=msg.content))

    return lc_messages


def extract_tool_result(response_text: str) -> tuple[str, Dict[str, Any] | None]:
    """
    Extract TOOL_RESULT JSON from the response text.

    Returns:
        Tuple of (cleaned_text, tool_result_dict or None)
    """
    pattern = r'TOOL_RESULT:\s*(\{.*?\})'
    match = re.search(pattern, response_text, re.DOTALL)

    if match:
        try:
            tool_result_json = match.group(1)
            tool_result = json.loads(tool_result_json)
            cleaned_text = re.sub(pattern, '', response_text, flags=re.DOTALL).strip()
            return cleaned_text, tool_result
        except json.JSONDecodeError:
            pass

    return response_text, None


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Chat with AI agent that can generate images/videos.

    The agent uses Gemini with function calling to orchestrate
    calls to Higgsfield's generation APIs based on user requests.
    """
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

    # Get the graph
    print("Initializing LangGraph agent...\n")
    graph = await get_chat_graph()

    # Convert conversation history
    messages = convert_to_langchain_messages(request.conversation_history)
    messages.append(HumanMessage(content=request.message))

    print(f"Total messages in context: {len(messages)}\n")

    # Run the graph
    state: Dict[str, Any] = {
        "messages": messages,
    }

    print("Running agent with Gemini...\n")
    result = await graph.ainvoke(state)

    # Extract the last AI message
    ai_messages = [msg for msg in result["messages"] if isinstance(msg, AIMessage)]

    if not ai_messages:
        response_text = "I apologize, but I couldn't process your request. Please try again."
        print("No AI response generated\n")
    else:
        response_text = ai_messages[-1].content
        print("="*80)
        print("AGENT RESPONSE GENERATED")
        print("="*80)
        print(f"Response: {response_text[:200]}{'...' if len(response_text) > 200 else ''}")
        print("="*80 + "\n")

    # Extract tool result if present
    cleaned_text, tool_result = extract_tool_result(response_text)

    # Build job details if tool was called
    job_details = None
    action_performed = None

    if tool_result:
        action_performed = tool_result.get("action")

        # Build JobDetails for generation actions
        if "job_set_id" in tool_result:
            job_details = JobDetails(
                job_set_id=tool_result["job_set_id"],
                status=tool_result["status"],
                job_type=tool_result["job_type"],
                model=tool_result["model"],
                parameters=tool_result.get("parameters", {}),
                estimated_time=tool_result.get("estimated_time", "2-5 minutes"),
            )

            print("="*80)
            print("JOB CREATED - STRUCTURED DATA")
            print("="*80)
            print(f"Job Set ID: {job_details.job_set_id}")
            print(f"Type: {job_details.job_type}")
            print(f"Model: {job_details.model}")
            print(f"Parameters: {json.dumps(job_details.parameters, indent=2)}")
            print(f"Estimated Time: {job_details.estimated_time}")
            print("="*80 + "\n")

    logger.info(
        "chat_response",
        response_length=len(cleaned_text),
        has_job=job_details is not None,
        action=action_performed,
    )

    return ChatResponse(
        message=cleaned_text,
        job_details=job_details,
        action_performed=action_performed,
    )

