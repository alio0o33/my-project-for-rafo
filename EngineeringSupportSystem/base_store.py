# base_store.py
import json
from pathlib import Path
from typing import List, Dict, Any, Optional

DATA_DIR = Path(__file__).parent / "data"
BASES_FILE = DATA_DIR / "airbases.json"
AIRCRAFT_FILE = DATA_DIR / "aircraft.json"

def _load(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

def load_bases() -> List[Dict[str, Any]]:
    return _load(BASES_FILE, [])

def load_aircraft() -> List[Dict[str, Any]]:
    return _load(AIRCRAFT_FILE, [])

def list_base_ids() -> List[str]:
    return [b["id"] for b in load_bases()]

def base_name(base_id: str) -> str:
    for b in load_bases():
        if b["id"] == base_id:
            return b.get("name", base_id)
    return base_id

def aircraft_by_base(base_id: str) -> List[Dict[str, Any]]:
    return [a for a in load_aircraft() if a.get("base_id") == base_id]

def tails_by_base(base_id: str) -> List[str]:
    return [a["tail"] for a in aircraft_by_base(base_id)]

def find_aircraft(tail: str) -> Optional[Dict[str, Any]]:
    for a in load_aircraft():
        if a.get("tail") == tail:
            return a
    return None
