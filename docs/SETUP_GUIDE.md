# Setup Guide

This guide gets the whole system running locally: MQTT broker → Node-RED
dashboard → Python control script.

## Prerequisites

- **Node.js** (v16 or later) — https://nodejs.org
- **Python 3.8+**
- An **MQTT broker** running locally. The easiest is **Mosquitto**:
  - Windows: download the installer from https://mosquitto.org/download/
  - macOS: `brew install mosquitto`
  - Linux: `sudo apt install mosquitto mosquitto-clients`

  After installing, make sure it's running on the default port `1883`.
  - Windows: it usually installs as a service and starts automatically. If not,
    run `mosquitto` from the install directory.
  - macOS: `brew services start mosquitto`
  - Linux: `sudo systemctl start mosquitto` (often starts automatically after install)

  To sanity-check the broker is up, you can run:
  ```
  mosquitto_sub -h localhost -t test/topic
  ```
  in one terminal, and in another:
  ```
  mosquitto_pub -h localhost -t test/topic -m "hello"
  ```
  You should see "hello" appear in the first terminal.

## 1. Install and run Node-RED

```bash
npm install -g --unsafe-perm node-red
cd node-red
npm install
node-red
```

Leave this terminal running. Node-RED is now serving its editor at:
**http://127.0.0.1:1880**

> The `npm install` inside the `node-red` folder installs `node-red-dashboard`,
> which is what renders the live web dashboard (gauges, slot grid, dropdowns, etc).

## 2. Import the flow

1. Open **http://127.0.0.1:1880** in your browser.
2. Click the hamburger menu (top right) → **Import**.
3. Click **select a file to import** and choose `node-red/flows.json` from this project
   (or paste its contents into the text box).
4. Click **Import**.
5. Click the red **Deploy** button (top right).

You should now see a flow tab called **"Smart Parking System"** with nodes for
sensor data, vehicle events, gate status, and the booking dropdowns.

## 3. Open the dashboard

Go to: **http://127.0.0.1:1880/ui**

You'll see four panels:
- **Live Slot Status** — a 6-slot grid that turns red/green as cars park/leave
- **Counters** — free slots, total entries, total exits, vehicles inside
- **Gate Status** — a badge showing OPEN/CLOSED
- **Book / Exit a Slot** — dropdowns to directly book or free a slot from the web UI

It will look mostly empty until the Python script starts publishing data (next step).

## 4. Run the Python control script

In a new terminal:

```bash
cd python
pip install -r requirements.txt
python park_system.py
```

You'll see a menu:
```
1. Check slot availability
2. Park a vehicle
3. Exit a vehicle
4. Reset system (all slots free)
5. Quit
```

Pick **2** to park a vehicle into a free slot, or **3** to remove one. Watch the
Node-RED dashboard update in real time — the slot grid, gate badge, and counters
all react immediately.

## 5. (Optional) Run the auto-simulator for a hands-free demo

If you'd rather not type into the CLI while recording your video:

```bash
cd python
python auto_simulator.py
```

This generates random park/exit events every few seconds, continuously, so the
dashboard stays lively on camera. Press `Ctrl+C` to stop it.

## Where is the data stored?

- `data/slots_db.json` — current status of every slot + running totals
  (this is the local stand-in for the Cloudant database)
- `data/slot_events_log.txt` — an append-only log of every sensor event,
  written by the Node-RED "Append Slot Log" node

Both are created automatically the first time you run anything — you don't
need to create them yourself.

## Troubleshooting

- **Dashboard shows nothing / doesn't update** — make sure your MQTT broker is
  actually running (see the `mosquitto_sub`/`mosquitto_pub` test above), and
  that `park_system.py` printed "Connected." rather than retrying.
- **Node-RED import errors about missing dashboard nodes** — make sure you ran
  `npm install` inside the `node-red` folder *before* starting `node-red`, so
  `node-red-dashboard` is available.
- **Port 1880 or 1883 already in use** — stop whatever else is using that port,
  or change the broker port in `python/mqtt_client.py` and in the `broker1`
  config node inside Node-RED (double-click it to edit).
