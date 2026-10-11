from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel,Field,ValidationError
from app.schemas.ingestion import IntentRequest,IntentResult
from app.services.llmservices import analyse_user_message
from app.utils.token_counter import estimate_token
app= FastAPI(
    title= "Testing the ingestion firewall at prompt level",
    description= "Testing the ingestion firewall at prompt level",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/health")
def health_check():
    return{"status":"ok", "message":"ingestion app is running"}
@app.post("/api/analyze",response_model=IntentResult)
def analyze(request: IntentRequest):
    message= request.message.strip()
    if not message:
        raise HTTPException(status_code=422, detail="message is empty")
    try:
        result= analyse_user_message(message)
        result.token_metadata.estimated_input_tokens = estimate_token(message)
        return result
    except ValidationError as exc:
        raise HTTPException(
            status_code=502,
            detail={
                "error": "The model response did not pass schema validation.",
                "validation_errors": exc.errors(),
            },
        ) from exc
    except Exception as exc:
        # ADD THIS PRINT STATEMENT TO LOG THE REAL BUG TO YOUR TERMINAL
        print("\n" + "="*50)
        print(f"🚨 REAL BACKEND EXCEPTION: {exc}")
        print("="*50 + "\n")
        
        # Keep the response simple; avoid exposing secrets or internal details.
        raise HTTPException(
            status_code=502,
            detail="LLM request failed. Check the API key, model name, network, and provider limits.",
        ) from exc