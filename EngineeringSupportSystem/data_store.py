# data_store.py
import json
from pathlib import Path
from typing import Dict, Any, List

DATA_DIR = Path(__file__).parent / "data"
USERS_FILE = DATA_DIR / "users.json"
TASKS_FILE = DATA_DIR / "tasks.json"

def load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default
    except json.JSONDecodeError:
        return default

def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_users():
    return load_json(USERS_FILE, [])

def save_users(users):
    save_json(USERS_FILE, users)

def load_tasks():
    return load_json(TASKS_FILE, [])

def save_tasks(tasks):
    save_json(TASKS_FILE, tasks)
    
def next_task_id() -> int:
    tasks = load_tasks()
    return (max((t.get("id", 0) for t in tasks), default=0) + 1)

def add_task(task: Dict[str, Any]) -> Dict[str, Any]:
    tasks = load_tasks()
    task["id"] = next_task_id()
    tasks.append(task)
    save_tasks(tasks)
    return task

def update_task(task_id: int, updates: Dict[str, Any]) -> bool:
    tasks = load_tasks()
    for t in tasks:
        if t.get("id") == task_id:
            t.update(updates)
            save_tasks(tasks)
            return True
    return False

def get_usernames_by_role(role: str) -> List[str]:
    return [u["username"] for u in load_users() if u.get("role") == role]

def list_usernames() -> List[str]:
    return [u["username"] for u in load_users()]

def add_user(username: str, password: str, role: str) -> bool:
    users = load_users()
    if any(u["username"] == username for u in users):
        return False
    users.append({"username": username, "password": password, "role": role})
    save_users(users)
    return True

def delete_user(username: str) -> bool:
    users = load_users()
    new_users = [u for u in users if u["username"] != username]
    if len(new_users) == len(users):
        return False
    save_users(new_users)
    return True

def filter_tasks(base_id: str = None, aircraft_tail: str = None):
    tasks = load_tasks()
    if base_id:
        tasks = [t for t in tasks if t.get("base_id") == base_id]
    if aircraft_tail:
        tasks = [t for t in tasks if t.get("aircraft_tail") == aircraft_tail]
    return tasks
