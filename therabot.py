import argparse
from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from anthropic import AsyncAnthropic
from typing import Dict
import aiohttp
import uuid
import uvicorn

app = FastAPI()

# Mount static files for serving CSS and JS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 template rendering
templates = Jinja2Templates(directory="templates")

# Store user contexts
user_contexts: Dict[str, list] = {}

# Global variable to store the Anthropic client
anthropic_client = None

# Dependency to get or create a user session
async def get_user_session(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id or session_id not in user_contexts:
        session_id = str(uuid.uuid4())
        user_contexts[session_id] = []
    return session_id

# Serve the chat window at "/"
@app.get("/", response_class=HTMLResponse)
async def get_chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

# Route for initializing a new chat context
@app.post("/new-context")
async def new_context(session: str = Depends(get_user_session)):
    user_contexts[session] = []
    return {"message": "New chat session started. Welcome!"}

# Route for chatting with Anthropic API
@app.post("/chat")
async def chat_to_anthropic(
    message: str = Form(...),
    session: str = Depends(get_user_session)
):
    # Add user message to context
    user_contexts[session].append({"role": "human", "content": message})
    
    # Call Anthropic API
    response = await anthropic_client.messages.create(
        model="claude-3-sonnet-20240229",
        messages=user_contexts[session],
        max_tokens=1000,
    )
    
    # Add assistant response to context
    user_contexts[session].append({"role": "assistant", "content": response.content[0].text})
    
    return {"response": response.content[0].text}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the FastAPI server with Anthropic API key")
    parser.add_argument("--api-key", required=True, help="Anthropic API key")
    args = parser.parse_args()

    # Initialize AsyncAnthropic client with the provided API key
    anthropic_client = AsyncAnthropic(api_key=args.api_key)

    # Run the FastAPI app
    uvicorn.run(app, host="0.0.0.0", port=8000)