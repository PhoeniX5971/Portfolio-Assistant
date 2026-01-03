import sys
from collections.abc import Iterable
from src.llm.agents import Session


def print_logs(logs: list[dict]):
    for log in logs:
        level = log.get("type", "info").upper()
        message = log.get("message", "")
        print(f"[{level}] {message}")


def normalize_messages(messages):
    """
    Defensive normalization:
    - ensures messages is a list of full strings
    - auto-joins character-split outputs
    """
    if not messages:
        return []

    # Case: accidentally got a list of single characters
    if all(isinstance(m, str) and len(m) == 1 for m in messages):
        return ["".join(messages)]

    normalized = []
    for msg in messages:
        if isinstance(msg, str):
            normalized.append(msg)
        elif isinstance(msg, Iterable):
            normalized.append("".join(map(str, msg)))
        else:
            normalized.append(str(msg))

    return normalized


def print_messages(messages):
    messages = normalize_messages(messages)

    for msg in messages:
        print("\n--- AI Assistant ---")
        print(msg)
        print("--------------------")


def main():
    session = Session()

    # One-shot mode
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
        messages, logs = session.run(prompt=prompt)

        print_logs(logs)
        print_messages(messages)
        return

    # Interactive mode
    print("--- Phoenix Assistant Terminal (Type 'exit' to quit) ---")
    while True:
        try:
            user_input = input("visitor@portfolio:~$ ")
            if user_input.lower() in ("exit", "quit"):
                break
            if not user_input.strip():
                continue

            messages, logs = session.run(prompt=user_input)

            print_logs(logs)
            print_messages(messages)

        except KeyboardInterrupt:
            print("\nExiting.")
            break


if __name__ == "__main__":
    main()
