import logging
import sys
from pathlib import Path

# Optional: color support in terminal
try:
    from colorama import Fore, Style, init as colorama_init

    colorama_init(autoreset=True)
    COLOR_ENABLED = True
except ImportError:
    COLOR_ENABLED = False


class Logger:
    def __init__(
        self, name: str, log_file: str | Path | None = None, level=logging.INFO
    ):
        """
        Simple logger.

        Args:
            name: logger name
            log_file: optional file path to log to
            level: logging level
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.propagate = False  # avoid double logging

        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Console handler
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(level)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        # File handler
        if log_file:
            log_file = Path(log_file)
            log_file.parent.mkdir(parents=True, exist_ok=True)
            fh = logging.FileHandler(log_file, encoding="utf-8")
            fh.setLevel(level)
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)

    # Convenience methods
    def debug(self, msg: str, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg: str, *args, **kwargs):
        if COLOR_ENABLED:
            msg = f"{Fore.CYAN}{msg}{Style.RESET_ALL}"  # type: ignore
        self.logger.info(msg, *args, **kwargs)

    def warn(self, msg: str, *args, **kwargs):
        if COLOR_ENABLED:
            msg = f"{Fore.YELLOW}{msg}{Style.RESET_ALL}"  # type: ignore
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs):
        if COLOR_ENABLED:
            msg = f"{Fore.RED}{msg}{Style.RESET_ALL}"  # type: ignore
        self.logger.error(msg, *args, **kwargs)

    def exception(self, msg: str, *args, **kwargs):
        """Log an exception with traceback"""
        self.logger.exception(msg, *args, **kwargs)
