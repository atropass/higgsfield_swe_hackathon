from app.agents.tools.t2i import generate_text_to_image
from app.agents.tools.t2v import generate_text_to_video
from app.agents.tools.i2v import generate_image_to_video

CHAT_TOOLS = [
    generate_text_to_image,
    generate_text_to_video,
    generate_image_to_video,
]

__all__ = [
    "CHAT_TOOLS",
    "generate_text_to_image",
    "generate_text_to_video",
    "generate_image_to_video",
]

