from pydantic import Field
from app.schemas.ingestion import IntentResult
class AssistantResult(IntentResult):
    markdown_result: str= Field(
        min_length=1,
        description= "markdown"
    )