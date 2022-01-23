import sys

from loguru import logger

LOGGER_FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> " \
                "| <level>{level: <8}</level> " \
                "- <level>{message}</level>"


def set_logger(level: str, log_file: str = None, **kwargs):
    logger_options = {"format": LOGGER_FORMAT, "level": level}
    logger_options.update(kwargs)

    logger.remove()
    logger.add(sys.stdout, **logger_options)

    if log_file:
        logger.add(log_file, **logger_options)
