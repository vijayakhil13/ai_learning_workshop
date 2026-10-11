import pytest
from pydantic import ValidationError
from app.schemas.ingestion import IntentResult,IntentRequest
def test_requests_trims_message():
    request=IntentRequest(message=" hello")
    assert request.message=="hello"

def test_request_rejects_black_message():
    with pytest.raises(ValidationError):
        IntentRequest(message=" ")
def test_result_invalid_intent():
    with pytest.raises(ValidationError):
        IntentResult(
            intent="shopping",
            risk_profile= "low",
            priority="low",
            requires_action=False,
            summary=" A test",
        )
def test_result_accepts_valid_data():
    result= IntentResult(
        intent="greeting",
        risk_profile="low",
        priority="low",
        requires_action=False,
        summary="The user greeted the assistant."
    )
    assert result.intent=="greeting"
    assert result.token_metadata.estimated_input_token==0