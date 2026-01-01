from synaptic import Model
from config import models as config
from src.prompt_engineering import (
    assistant_instructions,
    filter_instructions,
)

assistant = Model(
    provider=config.provider,
    model=config.model,
    api_key=".",
    automem=True,
    autorun=True,
    instructions=assistant_instructions,
)

filter = Model(
    provider=config.provider,
    model=config.model,
    api_key=".",
    automem=False,
    autorun=False,
    instructions=filter_instructions,
)
