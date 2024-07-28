import logging

__all__ = ["logger"]

logger = logging.getLogger("publisher")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)d | %(name)s | %(levelname)s | %(message)s",
)
