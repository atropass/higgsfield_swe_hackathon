from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent

from app.agents.prompts import SYSTEM_PROMPT
from app.agents.tools import CHAT_TOOLS
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


def create_chat_graph() -> any:
    print("\n" + "="*80)
    print("CREATING LANGGRAPH AGENT")
    print("="*80)

    logger.info("Creating chat graph with Gemini")

    print("Initializing Gemini 2.0 Flash...")
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        google_api_key=settings.gemini_api_key,
        temperature=0.7,
        convert_system_message_to_human=True,
    )
    print("Model initialized\n")

    print(f"Registering {len(CHAT_TOOLS)} generation tools:")
    for i, tool in enumerate(CHAT_TOOLS, 1):
        print(f"   {i}. {tool.name}")
    print("Note: Status checking handled by frontend, not agent\n")

    llm_with_prompt = llm.bind(system=SYSTEM_PROMPT)

    print("Building ReAct agent graph...")
    graph = create_react_agent(
        llm_with_prompt,
        tools=CHAT_TOOLS,
    )
    print(" Graph compiled successfully\n")

    print("The agent can now:")
    print("  • Generate images from text (T2I)")
    print("  • Generate videos from text (T2V)")
    print("  • Animate images (I2V)")
    print("\nStatus checking: Handled automatically by frontend")
    print("="*80 + "\n")

    logger.info("Chat graph created successfully")

    return graph


_chat_graph = None


async def get_chat_graph() -> any:
    global _chat_graph

    if _chat_graph is None:
        _chat_graph = create_chat_graph()

    return _chat_graph
