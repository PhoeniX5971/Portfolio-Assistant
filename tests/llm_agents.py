from src.llm.agents import Session
from src.utils.logger import Logger, logging

# Initialize logger
log = Logger(
    "prompts",  # fixed typo
    log_file="data/logs/tests/llm_agents.log",
    level=logging.DEBUG,
)

# Create test sessions
testsession = Session()
memory_test_session_one = Session()
memory_test_session_two = Session()

# Extract tool declarations
tool_declarations = [tool.declaration for tool in testsession.assistant.tools]
log.info("Tool Declarations:", tool_declarations)

# log.info memory addresses for debugging
log.info("\n=== History One Address ===")
log.info(
    f"{memory_test_session_one.assistant.history} @ {hex(id(memory_test_session_one.assistant.history))}"
)

log.info("\n=== Memory List One Address ===")
log.info(
    f"{memory_test_session_one.assistant.history.MemoryList} @ {hex(id(memory_test_session_one.assistant.history.MemoryList))}"
)

log.info("\n=== History Two Address ===")
log.info(
    f"{memory_test_session_two.assistant.history} @ {hex(id(memory_test_session_two.assistant.history))}"
)

log.info("\n=== Memory List Two Address ===")
log.info(
    f"{memory_test_session_two.assistant.history.MemoryList} @ {hex(id(memory_test_session_two.assistant.history.MemoryList))}"
)
