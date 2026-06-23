"""
slots_db.py
------------
A tiny local JSON "database" that stands in for the Cloudant DB used in the
original IBM-Cloud version of this project. It stores the current status
of every parking slot plus running totals for vehicles entered / exited.

Using a plain JSON file keeps the project fully runnable on a laptop with
no cloud account, while still giving Node-RED and the Python script a
shared, persistent place to read/write parking data -- exactly the role
Cloudant played in the original architecture.
"""

import json
import os
import threading
from datetime import datetime, timezone

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "slots_db.json")
DB_PATH = os.path.abspath(DB_PATH)

_lock = threading.Lock()

DEFAULT_SLOT_COUNT = 6


def _default_state():
    return {
        "slots": {
            f"S{i}": {"status": "free", "updated_at": None}
            for i in range(1, DEFAULT_SLOT_COUNT + 1)
        },
        "totals": {"entries": 0, "exits": 0},
        "gate": {"status": "closed", "updated_at": None},
    }


def _ensure_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, "w") as f:
            json.dump(_default_state(), f, indent=2)


def load():
    _ensure_db()
    with _lock:
        with open(DB_PATH, "r") as f:
            return json.load(f)


def save(state):
    _ensure_db()
    with _lock:
        with open(DB_PATH, "w") as f:
            json.dump(state, f, indent=2)


def get_slots():
    return load()["slots"]


def set_slot_status(slot_id, status):
    state = load()
    if slot_id not in state["slots"]:
        raise KeyError(f"Unknown slot: {slot_id}")
    state["slots"][slot_id] = {
        "status": status,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    save(state)
    return state["slots"][slot_id]


def get_free_slots():
    slots = get_slots()
    return [sid for sid, s in slots.items() if s["status"] == "free"]


def get_occupied_slots():
    slots = get_slots()
    return [sid for sid, s in slots.items() if s["status"] == "occupied"]


def record_entry():
    state = load()
    state["totals"]["entries"] += 1
    save(state)
    return state["totals"]


def record_exit():
    state = load()
    state["totals"]["exits"] += 1
    save(state)
    return state["totals"]


def set_gate(status):
    state = load()
    state["gate"] = {
        "status": status,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    save(state)
    return state["gate"]


def get_totals():
    return load()["totals"]


def reset():
    save(_default_state())
