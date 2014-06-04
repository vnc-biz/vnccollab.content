import sys
import logging


MYLOGGER = logging.getLogger('vnccollab.content')


def log_exception(msg, context=None, logger=MYLOGGER):
    """Log helper function."""
    logger.exception(msg)
    if context is not None:
        error_log = getattr(context, 'error_log', None)
        if error_log is not None:
            error_log.raising(sys.exc_info())
