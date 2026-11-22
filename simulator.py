import json, time, random
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc, props):
    print("DEVICE connected:", rc)
    client.subscribe("devices/pump-001/commands", qos=1)

def on_message(client, userdata, msg):
    print("COMMAND RECEIVED:", msg.payload.decode())

c = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="pump-001")
c.tls_set(ca_certs="certs/ca.crt", certfile="certs/pump-001.crt", keyfile="certs/pump-001.key")
c.on_connect = on_connect
c.on_message = on_message
c.connect("127.0.0.1", 8883, 60)
c.loop_start()

while True:
    m = {"moisture": round(random.uniform(18, 32), 1),
         "current": round(random.uniform(3.0, 4.0), 2),
         "eto": 4.0, "rain_mm": 0.0, "stage": "mid"}
    c.publish("devices/pump-001/sensors", json.dumps(m))
    print("SENT:", m)
    time.sleep(5)
