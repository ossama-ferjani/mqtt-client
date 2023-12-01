from flask import Flask
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

# MQTT broker settings
broker_address = "test.mosquitto.org"  # Replace with your broker IP
port = 1883  # Replace with your broker's NodePort
topic = "weather/temperature"  # Replace with the desired MQTT topic

client = mqtt.Client()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(topic)

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")
    socketio.emit('mqtt_message', {'message': msg.payload.decode(), 'topic': msg.topic})

# Assign MQTT callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect(broker_address, port=port)

# Start the MQTT client loop in a separate thread
client.loop_start()

from app import routes  # Import routes after initializing the MQTT client and SocketIO
