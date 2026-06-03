import logging
import queue
import sys
from logging.handlers import QueueHandler, QueueListener
from typing import Optional


class ColoredFormatter(logging.Formatter):
    RESET = "\033[0m"
    COLORS = {
        logging.DEBUG: "\033[90m",     # gray
        logging.INFO: "\033[32m",      # green
        logging.WARNING: "\033[33m",   # yellow
        logging.ERROR: "\033[31m",     # red
        logging.CRITICAL: "\033[35m",  # magenta
    }

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelno, self.RESET)

        original_levelname = record.levelname
        record.levelname = f"{color}{record.levelname}{self.RESET}"

        try:
            return super().format(record)
        finally:
            record.levelname = original_levelname

# Module-level globals so they live for the whole process lifetime
_log_queue: Optional[queue.Queue] = None
_listener: Optional[QueueListener] = None
_is_configured: bool = False
_global_log_level: Optional[int] = None


def set_global_log_level(log_level: str) -> None:
    """
    Set the log level for the root logger.
    """
    effective_log_level = getattr(logging, log_level.upper(), None)
    if not isinstance(effective_log_level, int):
        raise ValueError(f'Invalid log level: {log_level}')
    logging.getLogger().setLevel(effective_log_level)
    global _global_log_level
    _global_log_level = effective_log_level

def get_logger(
    logger_name: str = "app",
    fmt: str = "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
) -> logging.Logger:
    """
    Configure asynchronous, non-blocking logging using a queue and background listener.

    Calling this multiple times is safe: the queue & listener are created only once.
    You just get a logger with the given name back.
    """
    global _log_queue, _listener, _is_configured

    if not _is_configured:
        # Queue for log records
        _log_queue = queue.Queue()

        # Handler that puts records into the queue (used by your loggers)
        queue_handler = QueueHandler(_log_queue)

        # "Real" handler that actually writes to stdout
        console_handler = logging.StreamHandler(sys.stdout)
        formatter = ColoredFormatter(fmt, datefmt="%Y-%m-%d %H:%M:%S")
        console_handler.setFormatter(formatter)

        # Listener running in a background thread, reading from the queue
        _listener = QueueListener(_log_queue, console_handler)
        _listener.start()

        # attach handler to the root logger so all loggers go through the queue
        root_logger = logging.getLogger()
        root_logger.addHandler(queue_handler)

        global _global_log_level
        if _global_log_level is None:
            _global_log_level = logging.INFO
        root_logger.setLevel(_global_log_level)

        # Silence noisy dependency logs unless explicitly debugging them
        dependency_log_level = logging.WARNING if _global_log_level > logging.DEBUG else logging.DEBUG
        logging.getLogger("httpx").setLevel(dependency_log_level)
        logging.getLogger("httpcore").setLevel(dependency_log_level)
        logging.getLogger("google_genai.models").setLevel(dependency_log_level)

        _is_configured = True

    # Return a named logger for the caller
    return logging.getLogger(logger_name)


def shutdown_logging() -> None:
    """
    Stop the global QueueListener cleanly. Call this at application shutdown if you want
    to flush remaining logs.
    """
    global _listener
    if _listener is not None:
        _listener.stop()
        _listener = None
