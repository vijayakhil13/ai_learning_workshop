from pydantic import Field
from app.schemas.ingestion import IntentResult
class AssistantResult(IntentResult):
    session_id:str=(Field(min_length=1,description= "session_id"))
    response_markdown: str= Field(
        min_length=1,
        description= "markdown"
    )