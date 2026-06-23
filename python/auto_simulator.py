"""
auto_simulator.py
-------------------
Optional helper script that randomly parks/exits vehicles at a fixed
interval, so you have continuously changing live data on the Node-RED
dashboard while recording your demo video -- without having to type
into park_system.py the whole time.

This corresponds to the assignment's mention of "sending random car
availability slot values... to the IoT platform" for the dashboard to
display.

Usage:
    python auto_simulator.py
    (Ctrl+C to stop)
"""

import random
import time
from datetime import datetime, timezone

import slots_db
from mqtt_client import connect, publish_json, TOPIC_SENSOR, TOPIC_VEHICLE, TOPIC_GATE

CLIENT_ID = "smart-parking-auto-simulator"
INTERVAL_SECONDS = 4


def now():
    return datetime.now(timezone.utc).isoformat()


def step(client):
    free = slots_db.get_free_slots()
    occupied = slots_db.get_occupied_slots()

    # Randomly decide whether to park or exit a vehicle, weighted by
    # what's actually available so it always produces a valid action.
    can_park = len(free) > 0
    can_exit = len(occupied) > 0

    if can_park and (not can_exit or random.random() < 0.55):
        slot = random.choice(free)
        slots_db.set_slot_status(slot, "occupied")
        slots_db.record_entry()
        publish_json(client, TOPIC_SENSOR, {"slotId": slot, "status": "occupied", "timestamp": now()})
        publish_json(client, TOPIC_VEHICLE, {"event": "entry", "slotId": slot, "timestamp": now()})
        publish_json(client, TOPIC_GATE, {"status": "open", "timestamp": now()})
        print(f"[simulator] Vehicle entered -> slot {slot} occupied")
    elif can_exit:
        slot = random.choice(occupied)
        slots_db.set_slot_status(slot, "free")
        slots_db.record_exit()
        publish_json(client, TOPIC_SENSOR, {"slotId": slot, "status": "free", "timestamp": now()})
        publish_json(client, TOPIC_VEHICLE, {"event": "exit", "slotId": slot, "timestamp": now()})
        publish_json(client, TOPIC_GATE, {"status": "open", "timestamp": now()})
        print(f"[simulator] Vehicle exited <- slot {slot} freed")

    time.sleep(0.8)
    publish_json(client, TOPIC_GATE, {"status": "closed", "timestamp": now()})


def main():
    print("Connecting to local MQTT broker...")
    client = connect(CLIENT_ID)
    client.loop_start()
    print(f"Connected. Generating random parking activity every {INTERVAL_SECONDS}s. Ctrl+C to stop.")
    try:
        while True:
            step(client)
            time.sleep(INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print("\nStopping simulator.")
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
