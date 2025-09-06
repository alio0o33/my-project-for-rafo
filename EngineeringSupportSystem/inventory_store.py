# inventory_store.py
import json
from pathlib import Path
from typing import List, Dict, Any

DATA_DIR = Path(__file__).parent / "data"
STOCK_FILE = DATA_DIR / "stock.json"

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

def load_stock() -> List[Dict[str, Any]]:
    return _load_json(STOCK_FILE, [])

def save_stock(items: List[Dict[str, Any]]):
    _save_json(STOCK_FILE, items)

def upsert_item(part_no: str, name: str, qty: int, min_qty: int) -> None:
    items = load_stock()
    for it in items:
        if it["part_no"] == part_no:
            it.update({"name": name, "qty": qty, "min_qty": min_qty})
            save_stock(items); return
    items.append({"part_no": part_no, "name": name, "qty": qty, "min_qty": min_qty})
    save_stock(items)

def adjust_qty(part_no: str, delta: int) -> bool:
    items = load_stock()
    for it in items:
        if it["part_no"] == part_no:
            it["qty"] = max(0, int(it.get("qty", 0)) + int(delta))
            save_stock(items); return True
    return False

def delete_item(part_no: str) -> bool:
    items = load_stock()
    new_items = [x for x in items if x["part_no"] != part_no]
    if len(new_items) == len(items):
        return False
    save_stock(new_items); return True

def low_stock() -> List[Dict[str, Any]]:
    return [x for x in load_stock() if x.get("qty", 0) < x.get("min_qty", 0)]
