import os
from fastapi import FastAPI
from anthropic import AsyncAnthropic
from contextlib import asynccontextmanager

anthropic_client = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if api_key:
        global anthropic_client
        anthropic_client = AsyncAnthropic(api_key=api_key)
        print("Anthropic client initialized successfully.")
    else:
        print("Warning: ANTHROPIC_API_KEY not set. The Anthropic client will not be initialized.")
    yield
    print("Shutting down...")

async def get_anthropic_client():
    global anthropic_client
    if anthropic_client is None:
        raise RuntimeError("Anthropic client is not initialized")
    return anthropic_client
