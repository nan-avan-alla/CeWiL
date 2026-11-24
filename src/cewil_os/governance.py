from pydantic import BaseModel
from typing import Literal

RiskLevel = Literal["low", "moderate", "high", "critical"]

class RiskAssessment(BaseModel):
    level: RiskLevel
    triggers: list[str]
    requires_professional_review: bool = True
    automated_clearance: bool = False
    method: str = "conservative_keyword_triage_v1"

# Conservative routing hints only. This is not a validated engineering risk model.
TRIGGERS = {
    "critical": ("collapse", "imminent failure", "building is falling", "evacuation", "life safety", "structural failure"),
    "high": ("structural design", "structural audit", "foundation design", "load bearing", "seismic", "fire safety", "permit approval", "concrete strength", "unsafe building"),
    "moderate": ("inspection", "non-conformance", "ncr", "rfi", "boq", "rate analysis", "quality control", "site execution"),
}

def assess_risk(task: str) -> RiskAssessment:
    text = task.casefold()
    matches = [(level, phrase) for level, phrases in TRIGGERS.items() for phrase in phrases if phrase in text]
    if not matches:
        return RiskAssessment(level="low", triggers=[])
    rank = {"low": 0, "moderate": 1, "high": 2, "critical": 3}
    level = max((level for level, _ in matches), key=lambda item: rank[item])
    return RiskAssessment(level=level, triggers=sorted({phrase for _, phrase in matches}))
