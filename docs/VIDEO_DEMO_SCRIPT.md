# Video Demo Script

A suggested shot list that demonstrates every scenario named in the
assignment brief. Aim for 3–5 minutes total.

## 0. Intro (15–20s)
"This is my Smart Parking System for Smart Cities project. It uses an IoT-style
pipeline — a Python script simulating the parking sensors and entry/exit
detection, an MQTT broker as the messaging layer, and a Node-RED web
dashboard that drivers and operators would actually use."

*(Briefly show the architecture diagram from the README.)*

## 1. Show the empty dashboard (15s)
- Open `http://127.0.0.1:1880/ui`
- Point out: the 6-slot grid (all green/FREE), the gate badge (CLOSED), and
  the counters all at zero.

## 2. Scenario: Driver enters during rush hour (45s)
- Switch to the terminal running `park_system.py`.
- Choose **1** (Check availability) — narrate: "the driver's app checks for a
  free spot, just like the assignment scenario describes."
- Choose **2** (Park a vehicle), pick a free slot, e.g. `S2`.
- Switch back to the dashboard: show `S2` turn red/OCCUPIED, the gate badge
  flip to OPEN then back to CLOSED, and "Total Entries" increment.
- Narrate: "the app guided the driver to the nearest open spot, and the
  gate opened automatically on detection — no manual ticket."

## 3. Scenario: Commuter checks availability near home (30s)
- Back in the CLI, choose **1** again to show updated availability.
- Narrate: "a different driver checking the app would now see this updated,
  real-time availability before heading out — reducing wasted trips."

## 4. Scenario: Automatic payment & exit (45s)
- In the CLI, choose **3** (Exit a vehicle), select the slot you just parked in.
- Show the dashboard: slot turns green again, gate cycles open/closed,
  "Total Exits" increments, "Vehicles Inside" updates.
- Narrate: "on exit, payment is processed automatically and the barrier
  lifts immediately — no cash, no manual validation."

## 5. Booking directly from the web dashboard (30s)
- On the dashboard, use the **Book / Exit a Slot** dropdowns to book a
  different slot directly from the web UI (not the CLI).
- Show the success toast notification, and the slot grid updating.
- Narrate: "operators or future kiosk integrations could also book or
  release a slot straight from the web app."

## 6. (Optional) Continuous live traffic (20s)
- Run `python auto_simulator.py` in a terminal and let it run for ~15
  seconds while the camera stays on the dashboard, to show sustained,
  real-time activity rather than a single staged event.

## 7. Wrap-up (15s)
- Briefly show the Node-RED flow editor (`http://127.0.0.1:1880`) and
  mention: "all of this is built on an MQTT publish/subscribe pipeline —
  the same pattern used by the IBM Watson IoT Platform in the original
  cloud-hosted version of this assignment, just running locally so it's
  fully self-contained and reproducible from the GitHub repo."

## Checklist before you record
- [ ] MQTT broker running
- [ ] Node-RED running, flow deployed
- [ ] Dashboard open in browser, sized so the panels are clearly visible
- [ ] Terminal font large enough to read on screen
- [ ] `data/slots_db.json` reset (`python park_system.py` → option 4) so you start from a clean, empty lot
