# Smart Parking System for Smart Cities

A full, working implementation of the SmartInternz Smart Parking System
project — built to run entirely on your own laptop, with no IBM Cloud
account required, while still using the exact technologies the
assignment asks for: **Python**, **MQTT-based IoT messaging**, and a
**Node-RED dashboard web application**.

## How this maps to the original IBM Cloud architecture

The original brief asks for IBM Watson IoT Platform + Node-RED + Cloudant DB.
Those are commercial cloud services that need a registered account, API
keys, and ongoing provisioning — not something that can be packaged into
a downloadable project. So this build swaps in local, open-source
equivalents that do the *same job*, wired together the same way:

| Original (IBM Cloud)         | This project (local)                          |
|-------------------------------|------------------------------------------------|
| IBM Watson IoT Platform       | A local MQTT broker (e.g. Mosquitto)          |
| Node-RED service (IBM Cloud)  | Node-RED running locally (`npm install -g node-red`) |
| Cloudant DB                   | A local JSON file (`data/slots_db.json`) + event log |
| IoT device                    | `python/park_system.py` (and `auto_simulator.py`) |
| Web Application                | Node-RED Dashboard (`node-red-dashboard`)     |

Everything else — the data flow, the dashboard features, the gate
logic, the slot booking/cancellation — works exactly as specified in
the assignment. You get a real, demoable, end-to-end IoT pipeline.

```
 ┌────────────────────┐        MQTT         ┌─────────────────┐
 │ python/             │ ───────────────────▶│ Local MQTT       │
 │ park_system.py      │  parking/sensor/*   │ Broker           │
 │ (interactive CLI)   │  parking/vehicle/*  │ (Mosquitto)      │
 └────────────────────┘  parking/gate/*      └────────┬─────────┘
                                                        │
                                              subscribe/publish
                                                        │
                                              ┌─────────▼─────────┐
                                              │ Node-RED            │
                                              │ flows.json          │
                                              │  - parses messages  │
                                              │  - updates state    │
                                              │  - logs to data/     │
                                              │  - drives dashboard │
                                              └─────────┬─────────┘
                                                        │
                                              ┌─────────▼─────────┐
                                              │ Node-RED Dashboard │
                                              │ (browser web app)  │
                                              │  - slot grid        │
                                              │  - gate status       │
                                              │  - counters          │
                                              │  - book/exit slot     │
                                              └────────────────────┘
```

## Features implemented (matches the assignment's "Features" list)

- ✅ Automated gate simulation on entry/exit (auto-opens, auto-closes after a delay)
- ✅ Detection of empty / filled parking slots (6 slots, live state)
- ✅ "Display at the gate" — the Node-RED dashboard's slot grid + gate badge
- ✅ Vehicle entry/exit counting (gauges for total entries, exits, vehicles inside)
- ✅ Booking / cancelling a slot directly from the web dashboard
- ✅ Python script that takes user input to check availability, park, or exit
- ✅ All events flow through an IoT-style publish/subscribe pipeline, exactly like the cloud version

## Project structure

```
smart-parking-system/
├── python/
│   ├── park_system.py      <- main interactive CLI (the core deliverable)
│   ├── auto_simulator.py   <- optional: generates random traffic for video demos
│   ├── slots_db.py         <- local JSON "DB" (Cloudant stand-in)
│   ├── mqtt_client.py      <- shared MQTT connection helper
│   └── requirements.txt
├── node-red/
│   ├── flows.json          <- import this into Node-RED
│   └── package.json
├── data/                   <- created automatically: slots_db.json, log file
├── docs/
│   ├── SETUP_GUIDE.md      <- step-by-step install & run instructions
│   └── VIDEO_DEMO_SCRIPT.md<- a ready-made script for your demo video
└── README.md
```

## Quick start

See **`docs/SETUP_GUIDE.md`** for full step-by-step instructions (installing
Node-RED, the MQTT broker, importing the flow, and running the Python
script). In short:

1. Install and start a local MQTT broker (Mosquitto).
2. `npm install -g node-red` then `cd node-red && npm install` then `node-red`
3. Open `http://127.0.0.1:1880`, import `node-red/flows.json`, click **Deploy**.
4. Open the dashboard at `http://127.0.0.1:1880/ui`.
5. In another terminal: `cd python && pip install -r requirements.txt && python park_system.py`
6. Park/exit vehicles from the CLI (or run `auto_simulator.py`) and watch the dashboard update live.

## Submitting to SmartInternz

1. Push this whole folder to a public GitHub repository.
2. Record your demo video following `docs/VIDEO_DEMO_SCRIPT.md` — it walks
   through every required scenario (entry, real-time slot display, automatic
   gate/payment-style exit, and booking/cancelling from the web UI).
3. Submit the GitHub repo link + video link on the portal.
