import os
import argparse
from fastapi import FastAPI, Request, Form, Depends, Cookie
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from anthropic import AsyncAnthropic
from typing import Dict, List, Optional
from contextlib import asynccontextmanager
import aiohttp
import uuid
import uvicorn
import json
import asyncio

# Global variable to store the Anthropic client
anthropic_client = None

# Maximum number of messages to keep in context
MAX_CONTEXT_LENGTH = 20

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    print("Starting up...")
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if api_key:
        global anthropic_client
        anthropic_client = AsyncAnthropic(api_key=api_key)
        print("Anthropic client initialized successfully.")
    else:
        print("Warning: ANTHROPIC_API_KEY not set. The Anthropic client will not be initialized.")
    yield
    # Shutdown code
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

# Mount static files for serving CSS and JS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 template rendering
templates = Jinja2Templates(directory="templates")

# Store user contexts
user_contexts: Dict[str, List[Dict[str, str]]] = {}

# Dependency to get or create a user session
async def get_user_session(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id or session_id not in user_contexts:
        session_id = str(uuid.uuid4())
        user_contexts[session_id] = []
    return session_id

# Dependency to get the Anthropic client
async def get_anthropic_client():
    global anthropic_client
    if anthropic_client is None:
        raise RuntimeError("Anthropic client is not initialized")
    return anthropic_client

# Function to prune context if it exceeds maximum length
def prune_context(context: List[Dict[str, str]]) -> List[Dict[str, str]]:
    if len(context) > MAX_CONTEXT_LENGTH:
        return context[-MAX_CONTEXT_LENGTH:]
    return context

# Serve the chat window at "/"
@app.get("/", response_class=HTMLResponse)
async def get_chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

# Route for initializing a new chat context
@app.post("/new-context")
async def new_context(session: str = Depends(get_user_session)):
    user_contexts[session] = []
    return {"message": "New chat session started. Welcome!"}

# Route for chatting with Anthropic API (streaming)
@app.post("/chat")
async def chat_to_anthropic(
    message: str = Form(...),
    session: str = Depends(get_user_session),
    client: AsyncAnthropic = Depends(get_anthropic_client)
):
    # Add user message to context
    user_contexts[session].append({"role": "user", "content": message})
    
    # Prune context if necessary
    user_contexts[session] = prune_context(user_contexts[session])
    
    async def event_generator():
        try:
            # Call Anthropic API with streaming
            async with client.messages.stream(
                model="claude-3-sonnet-20240229",
                messages=user_contexts[session],
                max_tokens=1000,
            ) as stream:
                full_response = ""
                async for chunk in stream:
                    if chunk.type == "content_block_delta":
                        full_response += chunk.delta.text
                        yield f"data: {json.dumps({'delta': chunk.delta.text})}\n\n"
                
                # After streaming is complete, add the full response to the context
                user_contexts[session].append({"role": "assistant", "content": full_response})
                
                # Prune context again after adding assistant response
                user_contexts[session] = prune_context(user_contexts[session])
                
                yield f"data: {json.dumps({'done': True})}\n\n"
        except Exception as e:
            print(f"Error calling Anthropic API: {str(e)}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    response = StreamingResponse(event_generator(), media_type="text/event-stream")
    response.set_cookie(key="session_id", value=session)
    return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the FastAPI server with Anthropic API key")
    parser.add_argument("--api-key", required=True, help="Anthropic API key")
    args = parser.parse_args()

    # Set the API key as an environment variable
    os.environ["ANTHROPIC_API_KEY"] = args.api_key

    # Run the FastAPI app
    uvicorn.run("therabot:app", host="0.0.0.0", port=8000, reload=True)