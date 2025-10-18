
import asyncio
import random
from typing import Any, Callable

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

async def retry_with_backoff(
    func: Callable[..., Any],
    *args: Any,
    max_retries: int | None = None,
    backoff_factor: float | None = None,
    **kwargs: Any,
) -> Any:
    if max_retries is None:
        max_retries = settings.max_retries
    if backoff_factor is None:
        backoff_factor = settings.retry_backoff_factor

    last_exception = None

    for attempt in range(max_retries + 1):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            last_exception = e

            if attempt == max_retries:
                logger.error(
                    "max_retries_reached",
                    func=func.__name__,
                    attempt=attempt + 1,
                    error=str(e),
                )
                break

            backoff = (backoff_factor**attempt) + random.uniform(0, 1)
            logger.warning(
                "retry_attempt",
                func=func.__name__,
                attempt=attempt + 1,
                max_retries=max_retries,
                backoff_seconds=backoff,
                error=str(e),
            )

            await asyncio.sleep(backoff)

    if last_exception:
        raise last_exception
    raise RuntimeError("Retry failed without exception")

