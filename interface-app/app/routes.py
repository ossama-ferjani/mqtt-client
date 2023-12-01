from flask import render_template, request, jsonify
from app import app, socketio
import paho.mqtt.client as mqtt

# MQTT broker settings
broker_address = "test.mosquitto.org"  # Replace with your MQTT broker address
port = 1883  # Replace with your MQTT broker's port
topic = "weather/temperature"  # Replace with the desired MQTT topic

client = mqtt.Client()

# MQTT callbacks...
# ... (on_connect, on_message, etc.)

# SocketIO event handlers
@socketio.on('connect')
def handle_connect():
    print('Client connected')
    # You can perform actions when a client connects (if needed)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
    # You can perform actions when a client disconnects (if needed)

# Route for rendering the index.html template
@app.route('/')
def index():
    return render_template('index.html')

# Route for subscribing to the MQTT topic via GET request
@app.route('/subscribe', methods=['GET'])
def subscribe():
    client.subscribe(topic)
    return jsonify({'message': 'Subscribed to topic'})

# Route for publishing a message to the MQTT topic via POST request
@app.route('/publish', methods=['POST'])
def publish():
    content = request.json
    message = content.get('message')
    client.publish(topic, message)
    return jsonify({'message': 'Published to topic'})
