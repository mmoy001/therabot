from typing import Dict
from fastapi.templating import Jinja2Templates

MAX_CONTEXT_LENGTH = 20
user_contexts: Dict[str, Dict] = {}
templates = Jinja2Templates(directory="templates")

disorders = {
    "ADHD": {
        "age_range": (4, 65),
        "symptoms": [
            "fails to give close attention to details or makes careless mistakes",
            "difficulty sustaining attention in tasks or play activities",
            "does not seem to listen when spoken to directly",
            "often fidgets with or taps hands or feet",
            "difficulty organizing tasks and activities",
            "often interrupts or intrudes on others",
        ],
    },
    "Oppositional Defiant Disorder": {
        "age_range": (5, 17),
        "symptoms": [
            "often loses temper",
            "is often touchy or easily annoyed",
            "is often angry and resentful",
            "often argues with authority figures or adults",
            "often actively defies or refuses to comply with requests",
            "often deliberately annoys others",
            "often blames others for their mistakes or misbehavior",
            "has been spiteful or vindictive at least twice in the past six months",
        ],
    },
    "Antisocial Personality Disorder": {
        "age_range": (18, 65),
        "symptoms": [
            "failure to conform to social norms with respect to lawful behaviors",
            "deceitfulness, as indicated by repeated lying or conning others",
            "impulsivity or failure to plan ahead",
            "irritability and aggressiveness, often leading to physical fights",
            "reckless disregard for safety of self or others",
            "consistent irresponsibility",
            "lack of remorse after harming others",
        ],
    },
    "Schizophrenia": {
        "age_range": (16, 65),
        "symptoms": [
            "delusions (e.g., persecutory or grandiose delusions)",
            "hallucinations",
            "disorganized speech",
            "grossly disorganized or catatonic behavior",
            "negative symptoms (e.g., diminished emotional expression)",
        ],
    },
    "Substance-Induced Psychotic Disorder": {
        "age_range": (15, 65),
        "symptoms": [
            "presence of hallucinations or delusions",
            "symptoms developed during or soon after substance intoxication or withdrawal",
            "the substance used is capable of producing such symptoms",
            "psychotic symptoms not exclusive to delirium",
            "impairment in social or occupational functioning",
        ],
    },
    "Opioid Use Disorder": {
        "age_range": (18, 65),
        "symptoms": [
            "opioids taken in larger amounts or over a longer period than intended",
            "persistent desire or unsuccessful efforts to cut down or control use",
            "great deal of time spent obtaining, using, or recovering from opioids",
            "craving or strong desire to use opioids",
            "recurrent use resulting in failure to fulfill major role obligations",
            "continued use despite social or interpersonal problems",
            "important activities given up or reduced because of use",
            "tolerance and withdrawal symptoms",
        ],
    },
    "Autism Spectrum Disorder": {
        "age_range": (2, 15),
        "symptoms": [
            "deficits in social-emotional reciprocity",
            "deficits in nonverbal communicative behaviors",
            "deficits in developing and maintaining relationships",
            "restricted, repetitive patterns of behavior or speech",
            "highly restricted, fixated interests",
            "hyper- or hyporeactivity to sensory input",
        ],
    },
    "Major Depressive Disorder": {
        "age_range": (18, 65),
        "symptoms": [
            "depressed mood most of the day, nearly every day",
            "markedly diminished interest or pleasure in all activities",
            "significant weight loss when not dieting or weight gain",
            "insomnia or hypersomnia nearly every day",
            "psychomotor agitation or retardation",
            "fatigue or loss of energy nearly every day",
            "feelings of worthlessness or excessive guilt",
            "diminished ability to think or concentrate",
            "recurrent thoughts of death or suicidal ideation",
        ],
    },
}
