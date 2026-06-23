"""
mqtt_client.py
---------------
Thin wrapper around paho-mqtt so every script in this project connects to
the same local broker the same way. In the original IBM-Cloud version of
this project, this is the role Watson IoT Platform played -- the
mediator between the "IoT device" (our Python script) and the web app
(our Node-RED dashboard). Here, a local Mosquitto (or any MQTT) broker
plays that role, so everything runs on your machine with no cloud account.

Topics used in this project:
  parking/sensor/data    -> slot occupancy updates   {slotId, status, timestamp}
  parking/vehicle/event  -> entry/exit events         {event, timestamp}
  parking/gate/status    -> gate open/closed events   {status, timestamp}
  parking/command        -> dashboard -> backend cmds {slotId, action}
"""

import json
import time
import paho.mqtt.client as mqtt

BROKER_HOST = "localhost"
BROKER_PORT = 1883

TOPIC_SENSOR = "parking/sensor/data"
TOPIC_VEHICLE = "parking/vehicle/event"
TOPIC_GATE = "parking/gate/status"
TOPIC_COMMAND = "parking/command"


def connect(client_id, on_message=None):
    """Create and connect an MQTT client. Retries until the broker is up."""
    client = mqtt.Client(client_id=client_id)
    if on_message:
        client.on_message = on_message

    connected = False
    while not connected:
        try:
            client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
            connected = True
        except Exception as exc:
            print(f"[mqtt] Could not connect to {BROKER_HOST}:{BROKER_PORT} "
                  f"({exc}). Is your MQTT broker running? Retrying in 3s...")
            time.sleep(3)

    return client


def publish_json(client, topic, payload_dict):
    client.publish(topic, json.dumps(payload_dict))
