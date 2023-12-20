import paho.mqtt.client as mqtt
import models
import hashlib
import ssl

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("BPM")

def on_message(client, userdata, msg):
    received_data = msg.payload.decode("utf-8").split(',')
    received_bpm, received_bpm_hash = received_data[0], received_data[1]

    calculated_hash = hashlib.sha256(str(received_bpm).encode()).hexdigest()

    if received_bpm_hash == calculated_hash:
        models.log_heart_data(received_bpm)
        print("Data logged to the database.")
    else:
        print("Hash mismatch. Data not logged.")

broker_address = "192.168.1.5"
port = 8883
username = "esp_client"
password = "mqttclient123"
ca_file = "ca.crt"

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(username, password)

ssl_context = ssl.create_default_context(cafile=ca_file)

client.tls_set(ca_certs=ca_file, cert_reqs=ssl.CERT_NONE)

client.connect(broker_address, port, 60)

client.loop_forever()
