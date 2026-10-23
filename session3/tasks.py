from groq import Groq
import json
client=Groq()
chat_sessions={}
def chat_session(session_id:str,user_message:str)->str:
    if session_id not in chat_sessions:
        chat_sessions[session_id]=[{
            "role":"system",
            "content":"You are a helpfull concise assistant"
        }]
        chat_sessions[session_id].append({"role":"user","content":user_message})
        response=client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=chat_sessions[session_id],
            max_tokens=1024,
            temperature=0.7,
        )
        assistant_reply=response.choices[0].message.content
        chat_sessions[session_id].append({"role":"assistant","content":assistant_reply})
        return assistant_reply

if __name__=="__main__":
    session1="session1"
    session2="session2"
    print(chat_session(session1,"hi there"))
    print(chat_session(session2,"whats rag pipeline"))
    print(json.dumps(chat_sessions, indent=4))