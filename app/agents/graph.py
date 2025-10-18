from typing import Any

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent

from app.agents.prompts import SYSTEM_PROMPT
from app.agents.tools import CHAT_TOOLS
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


def create_chat_graph() -> Any:
    logger.info("creating_chat_graph", model="gemini-2.0-flash-exp", tools=len(CHAT_TOOLS))

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        google_api_key=settings.gemini_api_key,
        temperature=0.7,
        convert_system_message_to_human=True,
    )

    llm_with_prompt = llm.bind(system=SYSTEM_PROMPT)

    graph = create_react_agent(llm_with_prompt, tools=CHAT_TOOLS)

    logger.info("chat_graph_created", tools=[tool.name for tool in CHAT_TOOLS])

    return graph


_chat_graph = None


async def get_chat_graph() -> Any:
    global _chat_graph

    if _chat_graph is None:
        _chat_graph = create_chat_graph()

    return _chat_graph
