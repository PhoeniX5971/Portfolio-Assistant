from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
import time
import uuid
from src.llm.agents import Session
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import backend.security as security

app = FastAPI()
sessions: dict[str, Session] = {}

# Only allow your frontend to make browser requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://phoenix5971-portfolio.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


def verify_auth(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    token = auth_header.split(" ")[1]
    if not security.verify_token(token):
        raise HTTPException(status_code=401, detail="Invalid Authentication Token")


@app.post("/api/chat-rest")
async def chat_endpoint_rest(
    request: ChatRequest,
    request_obj: Request,
    x_session_id: Optional[str] = Header(None),
):
    # 1. Verify JWT
    verify_auth(request_obj)

    start_time = time.time()

    # 2. Session Management
    session_id = x_session_id or str(uuid.uuid4())
    if session_id not in sessions:
        sessions[session_id] = Session(session_id)

    session = sessions[session_id]

    try:
        # 3. Execute the Agent Loop (synchronous)
        messages, internal_logs = session.run(request.message)

        processing_time = int((time.time() - start_time) * 1000)

        return {
            "success": True,
            "response": messages,
            "logs": internal_logs,
            "metadata": {
                "session_id": session_id,
                "processing_time_ms": processing_time,
                "tokens": 0,  # replace with actual token count if available
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
    request: ChatRequest,
    request_obj: Request,
    x_session_id: Optional[str] = Header(None),
):
    # 1. Verify JWT
    verify_auth(request_obj)

    # 2. Session Management
    session_id = x_session_id or str(uuid.uuid4())
    if session_id not in sessions:
        sessions[session_id] = Session(session_id)

    session = sessions[session_id]

    # 3. Streaming response generator
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
