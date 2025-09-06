# training_store.py
import json
from pathlib import Path
from typing import List, Dict, Any

DATA_DIR = Path(__file__).parent / "data"
TRAINING_FILE = DATA_DIR / "training.json"

def _load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

def _save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_training() -> Dict[str, Any]:
    """
    {
      "sessions": [{"id":1,"title":"Fuel System","date":"2025-09-20"}],
      "assignments": [{"user":"engineer1","session_id":1,"status":"scheduled|completed"}]
    }
    """
    return _load_json(TRAINING_FILE, {"sessions": [], "assignments": []})

def save_training(data: Dict[str, Any]):
    _save_json(TRAINING_FILE, data)

def next_session_id(data: Dict[str, Any]) -> int:
    return (max((s.get("id", 0) for s in data.get("sessions", [])), default=0) + 1)

def add_session(title: str, date_iso: str) -> Dict[str, Any]:
    data = load_training()
    sid = next_session_id(data)
    data["sessions"].append({"id": sid, "title": title, "date": date_iso})
    save_training(data)
    return {"id": sid, "title": title, "date": date_iso}

def assign_user(user: str, session_id: int) -> bool:
    data = load_training()
    if not any(s["id"] == session_id for s in data["sessions"]):
        return False
    if any(a["user"] == user and a["session_id"] == session_id for a in data["assignments"]):
        return True
    data["assignments"].append({"user": user, "session_id": session_id, "status": "scheduled"})
    save_training(data); return True

def set_assignment_status(user: str, session_id: int, status: str) -> bool:
    data = load_training()
    for a in data["assignments"]:
        if a["user"] == user and a["session_id"] == session_id:
            a["status"] = status
            save_training(data); return True
    return False
