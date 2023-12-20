import paho.mqtt.client as mqtt
import models
import hashlib
import ssl

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("falls")  # Replace 'your_topic' with the desired MQTT topic

def on_message(client, userdata, msg):
    received_data = msg.payload.decode("utf-8").split(',')
    received_status, received_coordinates = received_data[0], received_data[1]
    print(received_status, received_coordinates)
    if received_status == "Faldet!":
        models.log_fall_data(received_coordinates)
        print("Data logged to the database.")

# Replace the following placeholders with your actual MQTT broker details
broker_address = "192.168.1.5"  # Example: "mqtt.example.com"
port = 8883
username = "esp_client"
password = "mqttclient123"
ca_file = "ca.crt"  # Replace with the actual path to your CA certificate file

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Set the username and password for authentication
client.username_pw_set(username, password)

# Set up SSL/TLS context
ssl_context = ssl.create_default_context(cafile=ca_file)

# Set TLS context for the client (disable certificate verification)
client.tls_set(ca_certs=ca_file, cert_reqs=ssl.CERT_NONE)


# Connect to the broker
client.connect(broker_address, port, 60)

# Start the MQTT client loop (this function runs in the background)
client.loop_forever()