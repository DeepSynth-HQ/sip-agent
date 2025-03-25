import logging
from settings.config import config
from rich.logging import RichHandler

logger = logging.getLogger(__name__)

logger.setLevel(config.LOG_LEVEL)
logger.addHandler(RichHandler())
