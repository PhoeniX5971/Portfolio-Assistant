import os
from pathlib import Path
from synaptic import Model, UserMem, autotool
from synaptic.core.base import memory
from config import models as config
from src.prompt_engineering import assistant_instructions, filter_instructions
from datetime import datetime, timezone

INFO_ROOT = Path(__file__).resolve().parent / "info"


class Session:
    def __init__(self) -> None:
        self.rerun = False
        self.rerun_reason = ""

        self.assistant = Model(
            provider=config.provider,
            model=config.model,
            api_key=os.getenv("GEMINI_API"),  # type:ignore
            automem=True,
            autorun=True,
            instructions=assistant_instructions,
        )

        self.ALLOWED_FILES = {
            "cv/about.md",
            "cv/contact.md",
            "cv/resume.md",
            "projects/attack-copilot.md",
            "projects/synaptic.md",
            "projects/assistant.md",
            "skills.md",
            "technologies.md",
        }

        # Bind tools using the instance methods directly
        self.assistant.bind_tools([self.request_rerun, self.access_information])

    @autotool(
        description="Request a rerun with instructions for the next step.",
        param_descriptions={
            "needed": "True if an additional execution turn is required.",
            "reason": "Instruction for the next run (e.g., 'Now summarize the file').",
        },
        autobind=False,
    )
    def request_rerun(self, needed: bool, reason: str):
        self.rerun = needed
        self.rerun_reason = reason
        return f"Rerun scheduled: {reason}" if needed else "Final turn confirmed."

    def wrap_to_mem(self, message):
        return UserMem(
            message=message,
            role="User",
            created=datetime.now().astimezone(timezone.utc),
        )

    @autotool(
        description="Read allowed project files.",
        param_descriptions={"section": "The relative path of the file to read."},
        autobind=False,
    )
    def access_information(self, section: str) -> str:
        if section not in self.ALLOWED_FILES:
            return f"❌ File not allowed: {section}"
        target_path = (INFO_ROOT / section).resolve()
        if not str(target_path).startswith(str(INFO_ROOT)):
            return "❌ Access denied."
        try:
            return target_path.read_text(encoding="utf-8")
        except Exception as e:
            return f"❌ Error: {e}"

    def run(self, prompt: str):
        self.rerun = True
        current_input = prompt
        internal_logs = []
        start_log = {"type": "info", "message": "🚀 Starting task sequence..."}
        if start_log not in internal_logs:
            internal_logs.append(start_log)
        all_messages = []  # 1. Create a list to store messages
        while self.rerun:
            self.rerun = False  # Reset
            response = self.assistant.invoke(current_input)

            # 2. Append the message to the list
            if response.message:
                all_messages.append(response.message)
            if self.rerun:
                internal_logs.append(
                    {"type": "warning", "message": f"🔄 Rerunning: {self.rerun_reason}"}
                )
                current_input = f"INSTRUCTION: {self.rerun_reason}"
            else:
                internal_logs.append(
                    {"type": "success", "message": "✅ Task completed."}
                )
        return all_messages, internal_logs  # 3. Return the list

    def run_stream(self, prompt: str):
        self.rerun = True
        current_input = prompt

        # Initial Log
        yield {
            "type": "log",
            "data": {"type": "info", "message": "🚀 Starting task sequence..."},
        }
        while self.rerun:
            self.rerun = False  # Reset
            response = self.assistant.invoke(current_input)
            # Yield message if present
            if response.message:
                yield {"type": "message", "data": response.message}
            if self.rerun:
                yield {
                    "type": "log",
                    "data": {
                        "type": "warning",
                        "message": f"🔄 Rerunning: {self.rerun_reason}",
                    },
                }
                current_input = f"INSTRUCTION: {self.rerun_reason}"
            else:
                yield {
                    "type": "log",
                    "data": {"type": "success", "message": "✅ Task completed."},
                }
