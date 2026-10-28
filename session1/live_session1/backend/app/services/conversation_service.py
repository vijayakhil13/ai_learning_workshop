from threading import RLock
from collections import defaultdict,deque
from typing import Any
MAX_MESSAGES=12
_history= dict[str,deque[dict[str,str]]]= defaultdict(
    lambda: deque(maxlen=MAX_MESSAGES))
lock=RLock()
def get_history(session_id:str)-> list[dict[str,str]]:
    with lock:
        return list(_history[session_id])
def add_message(session_id:str,role:str,content:str)-> None:
    if role not in {"user","assistant"}:
        raise ValueError("message not found")
    with lock:
        _history[session_id].append({"role":role,"content":content}) 
def remove_session(session_id:str) -> None:
    with lock:
        _history.pop(session_id,None)
def remove_all_sessions()-> None:
    with lock:
        _history.clear()