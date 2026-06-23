"""
park_system.py
---------------
This is the core Python deliverable for the assignment:

    "Develop a python code for taking the user input to check the
    availability of slots in the parking area. And based on the
    availability a person can park the vehicle in that area otherwise
    he can make an exit from that parking area. When entry or exit of
    the vehicle is detected the data along with slot no will be sent
    to the cloud and processing would be done in the Cloud."

Run this script, choose an action from the menu, and it will:
  1. Check slot availability locally (our JSON "DB", standing in for Cloudant)
  2. Park or remove a vehicle accordingly
  3. Publish the event over MQTT to the local broker (standing in for
     Watson IoT Platform), which the Node-RED dashboard is subscribed to
     and will update live.

Usage:
    python park_system.py
"""

import sys
import time
from datetime import datetime, timezone

import slots_db
from mqtt_client import (
    connect,
    publish_json,
    TOPIC_SENSOR,
    TOPIC_VEHICLE,
    TOPIC_GATE,
)

CLIENT_ID = "smart-parking-python-controller"


def now():
    return datetime.now(timezone.utc).isoformat()


def print_slots():
    slots = slots_db.get_slots()
    print("\nCurrent Parking Status")
    print("-----------------------")
    for slot_id in sorted(slots.keys()):
        info = slots[slot_id]
        marker = "OCCUPIED" if info["status"] == "occupied" else "FREE"
        print(f"  {slot_id}: {marker}")
    free = slots_db.get_free_slots()
    print(f"\nFree slots: {len(free)} / {len(slots)}")
    totals = slots_db.get_totals()
    print(f"Total entries so far: {totals['entries']}  |  "
          f"Total exits so far: {totals['exits']}")


def open_gate_and_pause(client):
    publish_json(client, TOPIC_GATE, {"status": "open", "timestamp": now()})
    slots_db.set_gate("open")
    print("[gate] Barrier opening...")
    time.sleep(1.5)
    publish_json(client, TOPIC_GATE, {"status": "closed", "timestamp": now()})
    slots_db.set_gate("closed")
    print("[gate] Barrier closed.")


def handle_park(client):
    free = slots_db.get_free_slots()
    if not free:
        print("\nSorry, the parking area is FULL. No free slots available.")
        print("Vehicle cannot park. Please try again later or check nearby lots.")
        return

    print(f"\nAvailable slots: {', '.join(sorted(free))}")
    chosen = input("Enter the slot number you want to park in (e.g. S1): ").strip().upper()
    if chosen not in free:
        print("Invalid or already-occupied slot. Please choose one from the list above.")
        return

    slots_db.set_slot_status(chosen, "occupied")
    slots_db.record_entry()

    publish_json(client, TOPIC_SENSOR, {
        "slotId": chosen, "status": "occupied", "timestamp": now(),
    })
    publish_json(client, TOPIC_VEHICLE, {"event": "entry", "slotId": chosen, "timestamp": now()})

    open_gate_and_pause(client)
    print(f"\nVehicle parked successfully in slot {chosen}. Payment processed automatically.")


def handle_exit(client):
    occupied = slots_db.get_occupied_slots()
    if not occupied:
        print("\nNo vehicles are currently parked.")
        return

    print(f"\nOccupied slots: {', '.join(sorted(occupied))}")
    chosen = input("Enter the slot number the vehicle is leaving from (e.g. S1): ").strip().upper()
    if chosen not in occupied:
        print("Invalid or already-free slot. Please choose one from the list above.")
        return

    slots_db.set_slot_status(chosen, "free")
    slots_db.record_exit()

    publish_json(client, TOPIC_SENSOR, {
        "slotId": chosen, "status": "free", "timestamp": now(),
    })
    publish_json(client, TOPIC_VEHICLE, {"event": "exit", "slotId": chosen, "timestamp": now()})

    open_gate_and_pause(client)
    print(f"\nVehicle exited slot {chosen} successfully. Barrier lifted, no manual ticket needed.")


def menu():
    print("\n=========================================")
    print(" Smart Parking System -- Control Console")
    print("=========================================")
    print(" 1. Check slot availability")
    print(" 2. Park a vehicle")
    print(" 3. Exit a vehicle")
    print(" 4. Reset system (all slots free)")
    print(" 5. Quit")
    return input("Choose an option (1-5): ").strip()


def main():
    print("Connecting to local MQTT broker (this is the stand-in for Watson IoT Platform)...")
    client = connect(CLIENT_ID)
    client.loop_start()
    print("Connected. Make sure Node-RED is running and the flow is deployed to see live updates.")

    while True:
        choice = menu()
        if choice == "1":
            print_slots()
        elif choice == "2":
            handle_park(client)
        elif choice == "3":
            handle_exit(client)
        elif choice == "4":
            slots_db.reset()
            print("All slots reset to FREE.")
        elif choice == "5":
            print("Goodbye!")
            client.loop_stop()
            client.disconnect()
            sys.exit(0)
        else:
            print("Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
