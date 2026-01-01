from pathlib import Path

ROOT = Path(__file__).parent


def load_prompt(filename: str) -> str:
    path = ROOT / filename
    return path.read_text(encoding="utf-8")


# optional convenience variables
assistant_instructions = load_prompt("assistant_instructions.md")
filter_instructions = load_prompt("filter_instructions.md")
