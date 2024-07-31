from logging_activity.logging_module import logging
from apps.constants import LOG_SWITCH


def log_info(message):
    """
    Logs an informational message.

    :param message: Message to log.
    :return: None
    """
    if LOG_SWITCH:
        logging.info(message)


def log_error(message):
    """
    Logs an error message.

    :param message: Message to log.
    :return: None
    """
    if LOG_SWITCH:
        logging.error(message)


def log_debug(message):
    """
    Logs a debug message.

    :param message: Message to log.
    :return: None
    """
    if LOG_SWITCH:
        logging.debug(message)
