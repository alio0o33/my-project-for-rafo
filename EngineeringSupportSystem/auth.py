# auth.py
from typing import Optional, Dict, Any
from data_store import load_users

def authenticate(username: str, password: str) -> Optional[Dict[str, Any]]:
    users = load_users()
    for u in users:
        if u.get("username") == username and u.get("password") == password:
            return u
    return None
