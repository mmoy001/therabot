from typing import Dict
from fastapi.templating import Jinja2Templates

MAX_CONTEXT_LENGTH = 20
user_contexts: Dict[str, Dict] = {}
templates = Jinja2Templates(directory="templates")

disorders = {
    # Neurodevelopmental Disorders
    "Autism Spectrum Disorder": {
        "age_range": (12, 15),
        "symptoms": [
            "difficulty with social interactions",
            "challenges in communication",
            "repetitive behaviors",
            "restricted interests",
            "resistance to changes in routine",
        ],
    },
    "Attention-Deficit/Hyperactivity Disorder (ADHD)": {
        "age_range": (12, 40),
        "symptoms": [
            "difficulty sustaining attention in tasks",
            "impulsivity and acting without thinking",
            "hyperactivity or restlessness",
            "difficulty organizing tasks and activities",
            "frequent forgetfulness in daily activities",
        ],
    },

    # Disruptive, Impulse Control, and Conduct Disorders
    "Oppositional Defiant Disorder": {
        "age_range": (12, 18),
        "symptoms": [
            "frequent temper tantrums or anger outbursts",
            "arguing with authority figures",
            "deliberately annoying others",
            "blaming others for their mistakes or misbehavior",
            "resentful or vindictive behavior",
        ],
    },
    "Antisocial Personality Disorder": {
        "age_range": (18, 65),
        "symptoms": [
            "disregard for the rights of others",
            "repeated violation of societal norms and laws",
            "impulsive and aggressive behavior",
            "lack of remorse after harming others",
            "manipulation and deceit for personal gain",
        ],
    },

    # Schizophrenia Spectrum and Other Psychotic Disorders
    "Schizophrenia with Paranoid Delusions": {
        "age_range": (18, 65),
        "symptoms": [
            "persistent delusions, particularly of persecution",
            "auditory or visual hallucinations",
            "disorganized thinking or speech",
            "social withdrawal and isolation",
            "heightened suspicion or mistrust of others",
        ],
    },

    # Bipolar and Related Disorders
    "Bipolar Disorder": {
        "age_range": (18, 65),
        "symptoms": [
            "extreme mood swings from high energy to low energy",
            "periods of elevated mood (mania) with increased activity",
            "periods of depression with low mood and energy",
            "impulsive behavior during manic episodes",
            "difficulty maintaining stable relationships",
        ],
    },

    # Depressive Disorders
    "Major Depressive Disorder": {
        "age_range": (18, 65),
        "symptoms": [
            "persistent feelings of sadness",
            "loss of interest in activities",
            "fatigue",
            "difficulty concentrating",
            "changes in sleep patterns",
        ],
    },
    "Persistent Depressive Disorder (Dysthymia)": {
        "age_range": (18, 65),
        "symptoms": [
            "long-term (2+ years) low mood",
            "lack of energy and motivation",
            "feelings of hopelessness",
            "difficulty making decisions",
            "low self-esteem",
        ],
    },

    # Anxiety Disorders
    "Generalized Anxiety Disorder (GAD)": {
        "age_range": (18, 65),
        "symptoms": [
            "excessive worry about various aspects of life",
            "restlessness or feeling on edge",
            "difficulty concentrating",
            "muscle tension",
            "sleep disturbances",
        ],
    },
    "Panic Disorder": {
        "age_range": (18, 50),
        "symptoms": [
            "unexpected panic attacks",
            "intense fear or discomfort during attacks",
            "fear of having another panic attack",
            "avoidance of situations associated with panic",
            "physical symptoms such as sweating or heart palpitations",
        ],
    },

    # Obsessive-Compulsive and Related Disorders
    "Obsessive-Compulsive Disorder (OCD)": {
        "age_range": (12, 50),
        "symptoms": [
            "recurrent, intrusive thoughts or images (obsessions)",
            "repetitive behaviors or rituals (compulsions)",
            "feelings of distress or anxiety when unable to perform compulsions",
            "excessive focus on order or cleanliness",
            "avoiding situations that trigger obsessions",
        ],
    },

    # Trauma- and Stressor-Related Disorders
    "Post-Traumatic Stress Disorder (PTSD)": {
        "age_range": (18, 65),
        "symptoms": [
            "recurrent distressing memories or flashbacks of trauma",
            "avoidance of reminders associated with the trauma",
            "heightened startle response",
            "feelings of detachment or emotional numbness",
            "difficulty sleeping or concentrating",
        ],
    },
    "Acute Stress Disorder": {
        "age_range": (18, 65),
        "symptoms": [
            "severe anxiety after a traumatic event",
            "recurrent distressing dreams or flashbacks",
            "feelings of detachment or unreality",
            "inability to concentrate or complete tasks",
            "avoidance of activities or places that remind of trauma",
        ],
    },

    # Dissociative Disorders
    "Dissociative Identity Disorder (DID)": {
        "age_range": (18, 65),
        "symptoms": [
            "presence of two or more distinct personality states",
            "gaps in memory for everyday events or personal information",
            "sense of detachment or being outside oneself",
            "difficulty remembering traumatic events",
            "sudden mood or behavior changes without clear cause",
        ],
    },
    "Dissociative Amnesia": {
        "age_range": (18, 65),
        "symptoms": [
            "inability to recall important personal information",
            "memory loss that is inconsistent with normal forgetting",
            "feeling detached from one's surroundings",
            "confusion about identity or history",
            "stress or confusion when trying to recall memories",
        ],
    },

    # Substance Abuse and Addictive Disorders
    "Substance-Induced Psychotic Disorder, Opioid Use Disorder and Violence": {
        "age_range": (18, 65),
        "symptoms": [
            "paranoia and delusions related to substance use",
            "aggressive or violent outbursts",
            "erratic behavior when under the influence",
            "intense cravings for opioids",
            "withdrawal symptoms when not using",
        ],
    },
    "Alcohol Use Disorder": {
        "age_range": (18, 65),
        "symptoms": [
            "difficulty controlling drinking behavior",
            "cravings for alcohol",
            "continued use despite negative consequences",
            "neglecting responsibilities due to alcohol use",
            "physical symptoms of withdrawal when not drinking",
        ],
    },
}

