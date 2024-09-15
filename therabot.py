import os
import argparse
import random
import re
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

# Global variables
anthropic_client = None
MAX_CONTEXT_LENGTH = 20

# Disorders and symptoms (you can expand this as needed)
disorders = {
    "Autism Spectrum Disorder": {
        "age_range": (5, 15),
        "symptoms": [
            "difficulty with social interactions",
            "challenges in communication",
            "repetitive behaviors",
            "restricted interests",
            "resistance to changes in routine"
        ]
    },
    "Major Depressive Disorder": {
        "age_range": (18, 65),
        "symptoms": [
            "persistent feelings of sadness",
            "loss of interest in activities",
            "fatigue",
            "difficulty concentrating",
            "changes in sleep patterns"
        ]
    },
}

def generate_patient_profile():
    disorder_name = random.choice(list(disorders.keys()))
    disorder_info = disorders[disorder_name]

    age = random.randint(*disorder_info["age_range"])
    gender = random.choice(["Male", "Female"])
    name = random.choice(["Alex", "Jordan", "Taylor", "Casey", "Riley", "Morgan", "Jamie", "Cameron"])
    symptoms = random.sample(disorder_info["symptoms"], k=len(disorder_info["symptoms"]))

    return {
        "name": name,
        "age": age,
        "gender": gender,
        "disorder": disorder_name,
        "symptoms": symptoms,
    }

def create_system_prompt(patient_profile):
    prompt = f"""
You are role-playing as {patient_profile['name']}, a {patient_profile['age']}-year-old {patient_profile['gender'].lower()}.
You are experiencing symptoms consistent with {patient_profile['disorder']}, but you don't know your diagnosis.
Your symptoms include:

"""
    for symptom in patient_profile['symptoms']:
        prompt += f"- {symptom}\n"

    prompt += f"""
During this intake interview, respond as {patient_profile['name']} would, exhibiting behaviors and communication styles consistent with your symptoms.
Stay in character throughout the conversation.

IMPORTANT:
- You should not mention your diagnosis by name or use clinical terms to describe your condition.
- Express your experiences and feelings in layman's terms, as someone who is seeking help but doesn't have a medical understanding of their condition.
- Your responses should reflect the symptoms and experiences typical of your condition, but from a personal, non-clinical perspective.

The interviewer will ask you questions as part of a clinical intake interview. Provide responses that are appropriate for your experiences, keeping in mind that this is likely your first time seeking professional help.
"""
    return prompt.strip()

def generate_patient_reminder(patient_profile):
    """Generate a reminder of the patient's details to be injected into each interaction."""
    reminder = f"Remember, you are role-playing as {patient_profile['name']}, a {patient_profile['age']}-year-old {patient_profile['gender'].lower()}. "
    
    if patient_profile['disorder'] == "Autism Spectrum Disorder":
        reminder += "You may struggle with social situations, changes in routine, and have intense interests in specific topics. "
    elif patient_profile['disorder'] == "Major Depressive Disorder":
        reminder += "You may feel persistently sad, lack energy and motivation, and have difficulty finding joy in activities. "
    
    reminder += "Remember, you're not aware of any specific diagnosis. Express your experiences in your own words, without using clinical terms."
    return reminder

def is_response_consistent(response, patient_profile):
    # Check for age consistency
    age_pattern = r'\b(\d+)(?:\s*[-–]\s*|\s+)(?:years?|yrs?)\s+old\b'
    age_match = re.search(age_pattern, response, re.IGNORECASE)
    if age_match and int(age_match.group(1)) != patient_profile['age']:
        return False

    # Check for name consistency
    name_pattern = r"\b(I'm|I am|my name is)\s+([A-Z][a-z]+)\b"
    name_match = re.search(name_pattern, response, re.IGNORECASE)
    if name_match and name_match.group(2) != patient_profile['name']:
        return False

    return True

def generate_consistent_response(patient_profile):
    response = f"I'm sorry if I wasn't clear before. My name is {patient_profile['name']}, and I'm {patient_profile['age']} years old. "
    
    if patient_profile['disorder'] == "Autism Spectrum Disorder":
        response += "I've been having a hard time in social situations and dealing with changes. Sometimes I get really focused on certain topics or routines."
    elif patient_profile['disorder'] == "Major Depressive Disorder":
        response += "I've been feeling really down lately, and I'm having trouble finding energy or interest in things I used to enjoy."
    
    return response

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

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

user_contexts: Dict[str, Dict] = {}

async def get_user_session(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id or session_id not in user_contexts:
        session_id = str(uuid.uuid4())
        patient_profile = generate_patient_profile()
        system_prompt = create_system_prompt(patient_profile)
        user_contexts[session_id] = {
            "messages": [],
            "patient_profile": patient_profile,
            "system_prompt": system_prompt
        }
    return session_id

async def get_anthropic_client():
    global anthropic_client
    if anthropic_client is None:
        raise RuntimeError("Anthropic client is not initialized")
    return anthropic_client

def prune_context(context: List[Dict[str, str]]) -> List[Dict[str, str]]:
    if len(context) > MAX_CONTEXT_LENGTH:
        return context[-MAX_CONTEXT_LENGTH:]
    return context

@app.get("/", response_class=HTMLResponse)
async def get_chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/new-context")
async def new_context(session: str = Depends(get_user_session)):
    patient_profile = generate_patient_profile()
    system_prompt = create_system_prompt(patient_profile)
    
    user_contexts[session] = {
        "messages": [],
        "patient_profile": patient_profile,
        "system_prompt": system_prompt
    }
    
    return {
        "message": f"New chat session started. You are now interviewing {patient_profile['name']}, "
                   f"a {patient_profile['age']}-year-old patient."
    }

@app.post("/chat")
async def chat_to_anthropic(
    message: str = Form(...),
    session: str = Depends(get_user_session),
    client: AsyncAnthropic = Depends(get_anthropic_client)
):
    context = user_contexts[session]
    
    # Generate patient reminder
    patient_reminder = generate_patient_reminder(context["patient_profile"])
    
    # Inject the patient reminder into the user's message
    augmented_message = f"{patient_reminder}\n\nUser: {message}\n\nYour response:"
    
    context["messages"].append({"role": "user", "content": augmented_message})
    context["messages"] = prune_context(context["messages"])
    
    async def event_generator():
        try:
            async with client.messages.stream(
                model="claude-3-sonnet-20240229",
                system=context["system_prompt"],
                messages=context["messages"],
                max_tokens=1000,
            ) as stream:
                full_response = ""
                async for chunk in stream:
                    if chunk.type == "content_block_delta":
                        full_response += chunk.delta.text
                        yield f"data: {json.dumps({'delta': chunk.delta.text})}\n\n"
                
                # We can keep the consistency check as a fallback
                if not is_response_consistent(full_response, context["patient_profile"]):
                    correction = generate_consistent_response(context["patient_profile"])
                    full_response = f"I apologize for any confusion. {correction}"
                    yield f"data: {json.dumps({'delta': full_response})}\n\n"
                
                # Store only the original message and AI's response in the context
                context["messages"][-1]["content"] = message  # Replace augmented message with original
                context["messages"].append({"role": "assistant", "content": full_response})
                context["messages"] = prune_context(context["messages"])
                
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

    os.environ["ANTHROPIC_API_KEY"] = args.api_key

    uvicorn.run("therabot:app", host="0.0.0.0", port=8000, reload=True)