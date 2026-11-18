from app.prompt_builder import build_user_message
from app.validator import validate_response
import pytest
from pydantic import ValidationError

def test_build_user_message():
    result = build_user_message("  I have a headache  ")

    assert result == "Patient description:\nI have a headache"

from app.prompt_builder import SYSTEM_PROMPT

def test_system_prompt_contains_triage_levels():
    assert "low" in SYSTEM_PROMPT
    assert "moderate" in SYSTEM_PROMPT
    assert "high" in SYSTEM_PROMPT

def test_validate_response_with_valid_data():
    raw = {
        "chief_complaint": "Persistent headache",
        "onset": "4 days ago",
        "duration": "4 days",
        "severity": 7,
        "red_flags": [],
        "triage_level": "moderate"
    }

    result = validate_response(raw)

    assert result.chief_complaint == "Persistent headache"
    assert result.severity == 7
    assert result.triage_level == "moderate"

def test_validate_response_rejects_invalid_severity():
    raw = {
        "chief_complaint": "Persistent headache",
        "onset": "4 days ago",
        "duration": "4 days",
        "severity": 15,
        "red_flags": [],
        "triage_level": "moderate"
    }

    with pytest.raises(ValidationError):
        validate_response(raw)

def test_validate_response_rejects_invalid_triage():
    raw = {
        "chief_complaint": "Persistent headache",
        "onset": "4 days ago",
        "duration": "4 days",
        "severity": 7,
        "red_flags": [],
        "triage_level": "urgent"
    }

    with pytest.raises(ValidationError):
        validate_response(raw)

def test_validate_response_rejects_missing_required_field():
    raw = {
        "onset": "4 days ago",
        "duration": "4 days",
        "severity": 7,
        "red_flags": [],
        "triage_level": "moderate"
    }

    with pytest.raises(ValidationError):
        validate_response(raw)

def test_validate_response_accepts_missing_optional_fields():
    raw = {
        "chief_complaint": "Mild headache",
        "triage_level": "low"
    }

    result = validate_response(raw)

    assert result.chief_complaint == "Mild headache"
    assert result.onset is None
    assert result.duration is None
    assert result.severity is None

def test_validate_response_defaults_red_flags_to_empty_list():
    raw = {
        "chief_complaint": "Mild headache",
        "triage_level": "low"
    }

    result = validate_response(raw)

    assert result.red_flags == []

def test_validate_response_accepts_minimum_severity():
    raw = {
        "chief_complaint": "Mild headache",
        "severity": 1,
        "triage_level": "low"
    }

    result = validate_response(raw)

    assert result.severity == 1

def test_validate_response_accepts_maximum_severity():
    raw = {
        "chief_complaint": "Severe headache",
        "severity": 10,
        "triage_level": "high"
    }

    result = validate_response(raw)

    assert result.severity == 10
