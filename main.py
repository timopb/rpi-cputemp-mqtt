import os
import time
import datetime
import sys
import paho.mqtt.client as mqtt

from gpiozero import CPUTemperature

MQTT_SERVER = os.getenv("MQTT_SERVER")
MQTT_PORT = os.getenv("MQTT_PORT", 1883)
MQTT_TOPIC = os.getenv("MQTT_TOPIC")
INTERVAL = int(os.getenv("MQTT_INTERVAL", 10))
USERNAME = os.getenv("MQTT_USERNAME")
PASSWORD = os.getenv("MQTT_PASSWORD")

print("==== Configuration ====")
print("Server: %s:%d" % (MQTT_SERVER, MQTT_PORT))
print("Topic: %s" % MQTT_TOPIC)
print("Username: %s" % USERNAME)
print("Password: %s" % PASSWORD)
print("Interval: %d" % INTERVAL)

next_reading = time.time()

client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)

print("==== Connecting to %s ====" % MQTT_SERVER)
client.connect(MQTT_SERVER, MQTT_PORT, 60)

client.loop_start()

try:
    while True:
        now = time.time()
        temperature = CPUTemperature().temperature
        temperature = round(temperature, 2)
        st = datetime.datetime.fromtimestamp(now).strftime('%Y-%m-%d %H:%M:%S')
        print("%s Publishing %s to %s" % (st, str(temperature), MQTT_TOPIC))
        client.publish(MQTT_TOPIC, temperature, 1)
        next_reading += INTERVAL
        sleep_time = next_reading - now
        if sleep_time > 0:
            time.sleep(sleep_time)
except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()
