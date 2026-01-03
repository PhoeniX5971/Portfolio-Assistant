import os
from pathlib import Path
from datetime import datetime, timezone
from uuid import uuid4

from synaptic import Model, UserMem, autotool
from config import models as config
from src.prompt_engineering import assistant_instructions, filter_instructions
from src.utils.logger import Logger

INFO_ROOT = Path(__file__).resolve().parent / "info"
SESSIONS_ROOT = Path("data/sessions")


class Session:
    def __init__(self, session_id: str | None = None) -> None:
        self.rerun = False
        self.rerun_reason = ""

        # ---- Session ID ----
        self.session_id = session_id or str(uuid4())

        # ---- Session directory ----
        self.session_dir = SESSIONS_ROOT / self.session_id
        self.session_dir.mkdir(parents=True, exist_ok=True)

        # ---- Logger ----
        self.logger = Logger(
            name=f"Session[{self.session_id}]",
            log_file=self.session_dir / "session.log",
        )
        self.logger.info("Session initialized.")

        # ---- Main Assistant ----
        self.assistant = Model(
            provider=config.provider,
            model=config.model,
            api_key=os.getenv("GEMINI_API"),  # type: ignore
            automem=True,
            autorun=True,
            instructions=assistant_instructions,
        )
        self.logger.info("Assistant model initialized.")

        # ---- Allowed files ----
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

        # ---- Tools ----
        self.assistant.bind_tools(
            [
                self.request_rerun,
                self.access_information,
            ]
        )
        self.logger.info("Tools bound to assistant.")

        # ---- Filter Agent (Fix: Renamed from self.assistant) ----
        self.filter = Model(
            provider=config.provider,
            model=config.model,  # You can use a lighter/faster model here if desired
            api_key=os.getenv("GEMINI_API"),  # type: ignore
            automem=False,  # Filter is stateless; doesn't need chat history
            autorun=True,
            instructions=filter_instructions,
        )
        self.logger.info("Filter agent initialized.")

    # ------------------------------------------------------------------

    @autotool(
        description="Request a rerun with instructions for the next step.",
        param_descriptions={
            "needed": "True if an additional execution turn is required.",
            "reason": "Instruction for the next run.",
        },
        autobind=False,
    )
    def request_rerun(self, needed: bool, reason: str):
        self.logger.info(f"Tool call: request_rerun(needed={needed}, reason={reason})")
        self.rerun = needed
        self.rerun_reason = reason

        result = f"Rerun scheduled: {reason}" if needed else "Final turn confirmed."
        self.logger.debug(f"Tool result: {result}")
        return result

    # ------------------------------------------------------------------

    @autotool(
        description="Read allowed project files.",
        param_descriptions={"section": "The relative path of the file to read."},
        autobind=False,
    )
    def access_information(self, section: str) -> str:
        self.logger.info(f"Tool call: access_information(section={section})")

        if section not in self.ALLOWED_FILES:
            msg = f"❌ File not allowed: {section}"
            self.logger.warn(msg)
            return msg

        target_path = (INFO_ROOT / section).resolve()
        if not str(target_path).startswith(str(INFO_ROOT)):
            msg = "❌ Access denied."
            self.logger.warn(msg)
            return msg

        try:
            content = target_path.read_text(encoding="utf-8")
            self.logger.debug(f"File read successfully: {section}")
            return content
        except Exception as e:
            msg = f"❌ Error reading file {section}: {e}"
            self.logger.error(msg)
            return msg

    # ------------------------------------------------------------------

    def wrap_to_mem(self, message: str) -> UserMem:
        mem = UserMem(
            message=message,
            role="User",
            created=datetime.now(tz=timezone.utc),
        )
        self.logger.debug(f"Wrapped message into UserMem")
        return mem

    # ------------------------------------------------------------------

    def run(self, prompt: str):
        self.logger.info(f"User input: {prompt}")

        self.rerun = True
        current_input = prompt

        internal_logs = [{"type": "info", "message": "🚀 Starting task sequence..."}]
        all_messages = []

        while self.rerun:
            self.rerun = False

            response = self.assistant.invoke(current_input)

            # --- FILTER INTEGRATION ---
            # If this is the final output (no rerun scheduled), run the filter.
            if not self.rerun and response.message:
                self.logger.info("Passing output to Filter Agent...")
                filtered_response = self.filter.invoke(response.message)

                # Check if filter returned valid text, otherwise keep original
                if filtered_response.message:
                    self.logger.info("Output sanitized.")
                    response.message = filtered_response.message
                else:
                    self.logger.warn("Filter returned empty; using raw output.")
            # --------------------------

            if response.message:
                self.logger.info(f"ResponseMem: {response.message}")
                all_messages.append(response.message)

            if getattr(response, "tool_calls", None):
                for call in response.tool_calls:
                    self.logger.debug(f"Tool call in response: {call}")

            if self.rerun:
                msg = f"🔄 Rerunning: {self.rerun_reason}"
                internal_logs.append({"type": "warning", "message": msg})
                self.logger.warn(msg)
                current_input = f"INSTRUCTION: {self.rerun_reason}"
            else:
                msg = "✅ Task completed."
                internal_logs.append({"type": "success", "message": msg})
                self.logger.info(msg)

        return all_messages, internal_logs

    # ------------------------------------------------------------------

    def run_stream(self, prompt: str):
        self.logger.info(f"User input (stream): {prompt}")

        self.rerun = True
        current_input = prompt

        yield {
            "type": "log",
            "data": {"type": "info", "message": "🚀 Starting task sequence..."},
        }

        while self.rerun:
            self.rerun = False

            response = self.assistant.invoke(current_input)

            # --- FILTER INTEGRATION (STREAM) ---
            if not self.rerun and response.message:
                self.logger.info("Passing output to Filter Agent...")
                prompt = (
                    "The following is the user's promprt:\n\n"
                    + current_input
                    + "\n\nThe following is the output of the agentic system:\n\n"
                    + response.message
                    + "\n\nAnything and everything you say here will be directly transmitted to the user. Please be very careful and act as instructed."
                )
                filtered_response = self.filter.invoke(prompt=prompt)

                if filtered_response.message:
                    response.message = filtered_response.message
            # -----------------------------------

            if response.message:
                self.logger.info(f"ResponseMem (stream): {response.message}")
                yield {"type": "message", "data": response.message}

            if getattr(response, "tool_calls", None):
                for call in response.tool_calls:
                    self.logger.debug(f"Tool call in response (stream): {call}")

            if self.rerun:
                msg = f"🔄 Rerunning: {self.rerun_reason}"
                self.logger.warn(msg)
                yield {"type": "log", "data": {"type": "warning", "message": msg}}
                current_input = f"INSTRUCTION: {self.rerun_reason}"
            else:
                msg = "✅ Task completed."
                self.logger.info(msg)
                yield {"type": "log", "data": {"type": "success", "message": msg}}
