from typing import Literal
from pydantic import BaseModel, Field, field_validator, ConfigDict

Intent= Literal[
    "greeting",
    "order_tracking",
    "payment_issue",
    "unknown",
    "current_time",
    "general_question"
]
RiskProfile= Literal["low","medium","high","unknown"]
Priority= Literal["low","medium","high"]

class IntentRequest(BaseModel):
    model_config= ConfigDict(extra= "forbid")
    message: str=Field(
        min_length= 1,
        max_length=5000,
        description= "the user's messgae",
    )
    @field_validator("message")
    @classmethod
    def message_value_not_null(cls,value:str)-> str:
        value= value.strip()
        if not value :
            raise ValueError("message can't be empty")
        return value
class TokenMetadata(BaseModel):
    estimated_input_tokens: int= Field(default=0,ge=0)
    note:str="estimated locally;may differ from provider token counts"


class IntentResult(BaseModel):
    model_config= ConfigDict(extra="forbid")
    intent: Intent
    risk_profile: RiskProfile
    priority: Priority
    requires_action: bool
    summary: str= Field(min_length=1,max_length=5000)
    token_metadata:TokenMetadata=Field(default_factory=TokenMetadata)