from typing import Dict
from fastapi.templating import Jinja2Templates

MAX_CONTEXT_LENGTH = 20
user_contexts: Dict[str, Dict] = {}
templates = Jinja2Templates(directory="templates")

disorders = {
    "Autism Spectrum Disorder": {
        "age_range": (5, 15),
        "symptoms": [
            "difficulty with social interactions",
            "challenges in communication",
            "repetitive behaviors",
            "restricted interests",
            "resistance to changes in routine",
        ],
    },
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
}
