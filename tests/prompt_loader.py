from src.prompt_engineering import assistant_instructions, filter_instructions
from src.utils.logger import Logger, logging

log = Logger(
    "assistant", log_file="data/logs/tests/prompt_loader.log", level=logging.DEBUG
)

log.info(assistant_instructions)
log.info(filter_instructions)
