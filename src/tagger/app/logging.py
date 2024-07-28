import logging

__all__ = ["logger"]

logger = logging.getLogger("tagger")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)d | %(name)s | %(levelname)s | %(message)s",
)
