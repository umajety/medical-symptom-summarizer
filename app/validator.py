"""validator.py — Pydantic schema for GPT output validation"""

from __future__ import annotations
from typing import List, Literal, Optional
from pydantic import BaseModel, field_validator
class SymptomSummary(BaseModel):
    chief_complaint: str
    onset: Optional[str] = None
    duration: Optional[str] = None
    severity: Optional[int] = None
    red_flags: List[str] = []
    triage_level: Literal["low", "moderate", "high"]
        
    @field_validator("severity")
    @classmethod
    def severity_range(cls, v):
        """Custom validation: if severity is given, it must be 1-10."""
        if v is not None and not (1 <= v <= 10):
            raise ValueError("Severity must be between 1 and 10")
        return v

def validate_response(raw: dict) -> SymptomSummary:
    """Parse and validate the LLM JSON response. Raises ValidationError if invalid."""
    return SymptomSummary(**raw)