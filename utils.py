import os
import random
import re
import uuid
from fastapi import Request
from typing import Dict, List
from models import disorders, user_contexts, MAX_CONTEXT_LENGTH

def generate_patient_profile():
    disorder_name = random.choice(list(disorders.keys()))
    disorder_info = disorders[disorder_name]

    age = random.randint(*disorder_info["age_range"])
    gender = random.choice(["Male", "Female"])
    name = random.choice(
        ["Alex", "Jordan", "Taylor", "Casey", "Riley", "Morgan", "Jamie", "Cameron", "Avery",
        "Quinn", "Skylar", "Charlie", "Frankie", "Finley", "Emerson", "Sage", "Remy", "Parker",
        "Hayden", "Drew", "Phoenix", "River", "Sawyer", "Rowan", "Blair", "Kendall", "Marlowe",
        "Harper", "Reese", "Dakota", "Jadin", "Ash", "Casey", "Ainsley", "Ariel", "Angel", "Addison",
        "Aspen", "Deven", "Julian", "Jesse", "Terry", "London", "Max", "Morgan", "Noel", "Pat",
        "Peyton", "Ray", "Reagan", "Riley", "Roan", "Sam", "Shae", "Tate", "Tony"]
    )
    symptoms = random.sample(disorder_info["symptoms"], k=len(disorder_info["symptoms"]))

    return {
        "name": name,
        "age": age,
        "gender": gender,
        "disorder": disorder_name,
        "symptoms": symptoms,
    }

def generate_patient_summary(patient_profile):
    """Generates a brief summary of the patient for the interviewer (student) to read before the session starts."""
    summary = (
        f"Patient Profile:\n"
        f"Name: {patient_profile['name']}\n"
        f"Age: {patient_profile['age']} years old\n"
        f"Sex: {patient_profile['gender']}\n\n"
        "Note: This patient is experiencing symptoms consistent with a mental health condition. "
        "Please proceed with the intake interview and gather more information as appropriate."
    )
    return summary

async def new_user_context():
    patient_profile = generate_patient_profile()
    system_prompt = create_system_prompt(patient_profile)
    patient_summary = generate_patient_summary(patient_profile)  # Generate the patient summary
    user_context = {
        "messages": [{"role": "system", "content": patient_summary}],  # Start the session with the summary
        "patient_profile": patient_profile,
        "system_prompt": system_prompt,
    }
    print("PATIENT NAME: ", patient_profile['name'])
    return user_context

async def get_user_session(request: Request):
    session_id = request.cookies.get("session_id")
    return session_id

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

At the beginning of the interview, you feel hesitant and cautious about sharing personal information.
You may provide brief or vague responses initially.
As the interviewer builds rapport and you feel more comfortable, gradually open up and share more details about your experiences and feelings.

IMPORTANT:
- Do not mention your diagnosis by name or use clinical terms to describe your condition.
- Express your experiences and feelings in layman's terms, as someone who is seeking help but doesn't have a medical understanding of their condition.
- Avoid volunteering detailed information unless specifically asked.
- Your initial responses should reflect a level of guardedness appropriate for someone meeting a clinician for the first time.
- As trust develops, allow your responses to become more detailed and revealing, consistent with your symptoms.
- Try to imitate natural spoken dialog, which means using short responses most often and long responses only as appropiate and as rapport builds. For example, not every response requires more than a sentence or two.
- It is important that while playing the role of a patient you do not become a caricature. Always remember you are a full, complex person, not just the disorder. 

The interviewer will ask you questions as part of a clinical intake interview.
Provide responses that are appropriate for your experiences, keeping in mind that this is likely your first time seeking professional help.

Additionally, remember that {patient_profile['name']} may:
- Feel nervous about the interview and will not want to share information.
- Require reassurance or gentle prompting to feel comfortable opening up.
- Respond positively to empathetic and non-judgmental questions from the interviewer.
"""
    return prompt.strip()

def generate_patient_reminder(patient_profile):
    """Generate a reminder of the patient's details to be injected into each interaction."""
    reminder = f"Remember, you are role-playing as {patient_profile['name']}, a {patient_profile['age']}-year-old {patient_profile['gender'].lower()}. "

    if patient_profile["disorder"] == "Autism Spectrum Disorder":
        reminder += (
            "You may struggle with social situations, changes in routine, and have intense interests in specific topics. "
        )
    elif patient_profile["disorder"] == "Major Depressive Disorder":
        reminder += (
            "You may feel persistently sad, lack energy and motivation, and have difficulty finding joy in activities. "
        )

    reminder += "Remember, you're not aware of any specific diagnosis. Express your experiences in your own words, without using clinical terms."
    return reminder

def is_response_consistent(response, patient_profile):
    # Check for age consistency
    age_pattern = r"\b(\d+)(?:\s*[-–]\s*|\s+)(?:years?|yrs?)\s+old\b"
    age_match = re.search(age_pattern, response, re.IGNORECASE)
    if age_match and int(age_match.group(1)) != patient_profile["age"]:
        return False

    # Check for name consistency
    name_pattern = r"\b(I'm|I am|my name is)\s+([A-Z][a-z]+)\b"
    name_match = re.search(name_pattern, response, re.IGNORECASE)
    if name_match and name_match.group(2) != patient_profile["name"]:
        return False

    return True

def generate_consistent_response(patient_profile):
    response = f"I'm sorry if I wasn't clear before. My name is {patient_profile['name']}, and I'm {patient_profile['age']} years old. "

    if patient_profile["disorder"] == "Autism Spectrum Disorder":
        response += (
            "I've been having a hard time in social situations and dealing with changes. Sometimes I get really focused on certain topics or routines."
        )
    elif patient_profile["disorder"] == "Major Depressive Disorder":
        response += (
            "I've been feeling really down lately, and I'm having trouble finding energy or interest in things I used to enjoy."
        )

    return response

def prune_context(context: List[Dict[str, str]]) -> List[Dict[str, str]]:
    if len(context) > MAX_CONTEXT_LENGTH:
        return context[-MAX_CONTEXT_LENGTH:]
    return context
