from uuid import UUID,uuid4
import traceback
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel,Field,ValidationError
from app.schemas.ingestion import IntentRequest,IntentResult
from app.services.llmservices import analyse_user_message
from app.utils.token_counter import estimate_token
from app.schemas.assistant import AssistantResult
from app.services.response import generate_response
from app.services.db import(initialize_database,ensure_conversation,add_chat_message,get_chat_history,list_conversations,get_conversation_messages)
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
@app.on_event("startup")
def startup():
    initialize_database()
@app.get("/health")
def health_check():
    return{"status":"ok", "message":"ingestion app is running"}
@app.get("/api/conversations")
def conversations():
    return {"items": list_conversations()}
        
@app.get("/api/conversations/{session_id}/messages")
def conversations_messages(session_id:str):
    try: UUID(session_id)
    except ValueError: raise HTTPException(status_code=400, detail="Invalid conversation ID.")
    return {"session_id": session_id, "items": get_conversation_messages(session_id)}

""""
@app.post("/api/analyze",response_model=IntentResult)
def analyze(request: IntentRequest):
    message= request.message.strip()
    if not message:
        raise HTTPException(status_code=422, detail="message is empty")
    try:
        result= analyse_user_message(message)
        result.token_metadata.estimated_input_tokens = estimate_token(message)
        response_markdown=generate_response(result)
        return AssistantResult(**result.model_dump(),response_markdown=response_markdown,)
        
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
        print(f"REAL BACKEND EXCEPTION: {exc}")
        print("="*50 + "\n")
        
        # Keep the response simple; avoid exposing secrets or internal details.
        raise HTTPException(
            status_code=502,
            detail="LLM request failed. Check the API key, model name, network, and provider limits.",
        ) from exc """
@app.post("/api/analyze", response_model=AssistantResult)
def analyze(request: IntentRequest):
    message = request.message.strip()
    if not message: raise HTTPException(status_code=422, detail="Message cannot be empty.")
    session_id = request.session_id or str(uuid4())
    try: UUID(session_id)
    except ValueError: raise HTTPException(status_code=422, detail="session_id must be a valid UUID.")
    try:
        ensure_conversation(session_id, message[:70])
        result = analyse_user_message(message)
        result.token_metadata.estimated_input_tokens = estimate_token(message)
        history = get_chat_history(session_id)
        response_markdown = generate_response(result, history=history, current_message=message)
        add_chat_message(session_id, "user", message)
        add_chat_message(session_id, "assistant", response_markdown)
        return AssistantResult(**result.model_dump(), session_id=session_id, response_markdown=response_markdown)
    except ValidationError as exc:
        raise HTTPException(status_code=502, detail={"error":"The model response did not pass schema validation.", "validation_errors":exc.errors()}) from exc
    except Exception as exc:
        print(f"\n{'='*50}")
        print(f"REQUEST FAILED FOR SESSION: {session_id}")
        print(f"ERROR: {exc}")
        print("FULL TRACEBACK:")
        traceback.print_exc()  # This will print the exact file name and line number!
        print(f"{'='*50}\n")
        
        raise HTTPException(
            status_code=502, 
            detail="The AI request failed. Check backend/.env, your network, database connection, model name, and provider limits."
        ) from exc    