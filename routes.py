from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, StreamingResponse
from models import user_contexts, templates
from utils import (
    get_user_session,
    generate_patient_reminder,
    prune_context,
    is_response_consistent,
    generate_consistent_response,
    generate_patient_profile,
    generate_patient_summary,
    create_system_prompt,
    new_user_context,
)
from anthropic_client import get_anthropic_client
from anthropic import AsyncAnthropic
import json

app_routes = APIRouter()

disclaimer = "https://docs.google.com/document/d/1lDNbDQSgLv94GA7abUYuzrLegKHob4L2Ai5Y7_B09hA/view"

@app_routes.get("/", response_class=HTMLResponse)
async def get_chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app_routes.post("/new-context")
async def new_context(session: str = Depends(get_user_session)):
    user_context = await new_user_context()
    user_contexts[session] = user_context
    print(user_context['patient_profile']['name'])
    patient_profile = user_context["patient_profile"]

    return {
        "message": [
            "By continuing to use this LLM chat application, you agree to our terms and conditions.",
            "If you do not agree, please discontinue use immediately.",
            "",
            "New chat session started. Please begin the intake interview.",
            "",
            "Patient Profile:",
            f"Name: {patient_profile['name']}",
            f"Age: {patient_profile['age']} years old",
            f"Sex: {patient_profile['gender']}",
            "",
            "Note: This patient is experiencing symptoms consistent with a mental health condition. "
            "Proceed with the intake interview to gather more information."
        ],
        "disclaimer_url": disclaimer
    }

@app_routes.post("/chat")
async def chat_to_anthropic(
    message: str = Form(...),
    session: str = Depends(get_user_session),
    client: AsyncAnthropic = Depends(get_anthropic_client),
):
    context = user_contexts[session]

    # Generate patient reminder
    patient_reminder = generate_patient_reminder(context["patient_profile"])

    # Instead of injecting the reminder into the user's message, we'll use it as a system message
    system_message = f"{context['system_prompt']}\n\n{patient_reminder}"

    # Prepare the messages for the API call
    api_messages = []
    for msg in context["messages"]:
        if msg["role"] == "user":
            api_messages.append({"role": "user", "content": msg["content"]})
        elif msg["role"] == "assistant":
            api_messages.append({"role": "assistant", "content": msg["content"]})

    # Add the new user message
    api_messages.append({"role": "user", "content": message})

    async def event_generator():
        try:
            async with client.messages.stream(
                model="claude-3-sonnet-20240229",
                system=system_message,
                messages=api_messages,
                max_tokens=1000,
            ) as stream:
                full_response = ""
                async for chunk in stream:
                    if chunk.type == "content_block_delta":
                        delta_text = chunk.delta.text
                        full_response += delta_text
                        yield f"data: {json.dumps({'delta': delta_text})}\n\n"

                # Consistency check
                #if not is_response_consistent(full_response, context["patient_profile"]):
                #    correction = generate_consistent_response(context["patient_profile"])
                #    full_response = f"I apologize for any confusion. {correction}"
                #    yield f"data: {json.dumps({'delta': full_response})}\n\n"

                # Store the original message and AI's response in the context
                context["messages"].append({"role": "user", "content": message})
                context["messages"].append({"role": "assistant", "content": full_response})
                context["messages"] = prune_context(context["messages"])

                yield f"data: {json.dumps({'done': True})}\n\n"
        except Exception as e:
            print(f"Error calling Anthropic API: {str(e)}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    response = StreamingResponse(event_generator(), media_type="text/event-stream")
    response.set_cookie(key="session_id", value=session)
    return response
