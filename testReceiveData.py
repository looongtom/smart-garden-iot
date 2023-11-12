from flask import Flask, jsonify
import paho.mqtt.client as mqtt

app = Flask(__name__)

mqtt_broker = "192.168.1.10"
mqtt_port = 1883
mqtt_topic = "iot"

data = {}

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    global data
    payload = msg.payload.decode()
    print(f"Received message on topic {msg.topic}: {payload}")
    # Update data dictionary with received JSON
    data = payload

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_broker, mqtt_port, 60)

# Start MQTT loop in a separate thread
client.loop_start()

@app.route('/get_data', methods=['GET'])
def get_data():
    global data
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
