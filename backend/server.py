from fastapi import FastAPI, Header
from pydantic import BaseModel
from typing import Optional
import time
import uuid
from src.llm.agents import Session

from fastapi.responses import StreamingResponse
import json

app = FastAPI()
sessions: dict[str, Session] = {}


class ChatRequest(BaseModel):
    message: str


@app.post("/api/chat-rest")
async def chat_endpoint_rest(
    request: ChatRequest, x_session_id: Optional[str] = Header(None)
):
    start_time = time.time()

    # 1. Session Management
    session_id = x_session_id or str(uuid.uuid4())
    if session_id not in sessions:
        sessions[session_id] = Session(x_session_id)

    session = sessions[session_id]

    try:
        # 2. Execute the Agent Loop
        # This returns (message, internal_logs) as we fixed earlier
        messages, internal_logs = session.run(request.message)

        processing_time = int((time.time() - start_time) * 1000)

        # 3. Return the exact format your TSX expects
        return {
            "success": True,
            "response": messages,
            "logs": internal_logs,
            "metadata": {
                "session_id": session_id,
                "processing_time_ms": processing_time,
                "tokens": 0,  # Replace with actual token count if available
            },
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "logs": [{"type": "error", "message": f"Fatal: {str(e)}"}],
        }


@app.post("/api/chat")
async def chat_endpoint(
    request: ChatRequest, x_session_id: Optional[str] = Header(None)
):
    session_id = x_session_id or str(uuid.uuid4())
    if session_id not in sessions:
        sessions[session_id] = Session(x_session_id)
    session = sessions[session_id]

    # Note: NOT async, so FastAPI runs it in a threadpool
    def event_generator():
        try:
            for event in session.run_stream(request.message):
                yield json.dumps(event) + "\n"
        except Exception as e:
            yield json.dumps(
                {
                    "type": "log",
                    "data": {"type": "error", "message": f"Fatal: {str(e)}"},
                }
            ) + "\n"

    return StreamingResponse(event_generator(), media_type="application/x-ndjson")
