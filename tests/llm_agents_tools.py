from src.llm.agents import Session
from src.utils.logger import Logger, logging

# Initialize logger
log = Logger(
    "prompts",  # fixed typo
    log_file="data/logs/tests/llm_agents_tools.log",
    level=logging.DEBUG,
)

# Create test sessions
session = Session()

log.info(session.access_information.function("projects/assistant.md"))
