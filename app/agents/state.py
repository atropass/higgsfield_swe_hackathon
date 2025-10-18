from langgraph.graph import MessagesState


class ChatState(MessagesState):
    """
    State for the chat agent.

    Extends MessagesState which provides:
    - messages: list of messages with add_messages reducer
    - Other required fields for ReAct agent

    We add custom fields for tracking job information.
    """

    job_set_id: str | None
    job_status: str | None

