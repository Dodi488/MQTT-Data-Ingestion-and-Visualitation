"""
MQTT Publisher for IoT Data Ingestion Pipeline
Publishes random integer and float values to separate MQTT topics
"""

import json
import random
import ssl
import time
import paho.mqtt.client as mqtt

# MQTT Broker Configuration
BROKER = "bird.lmq.cloudamqp.com"
PORT = 8883
USERNAME = "ygvefxav:ygvefxav"
PASSWORD = "7IP9KbugtgqrlgcgNXo4KXy65mpaRNnn"

# Topics for different data types
TOPIC_INT = "sensor/data/int"
TOPIC_FLOAT = "sensor/data/float"

def on_connect(client, userdata, flags, rc):
    """Callback when client connects to broker"""
    if rc == 0:
        print("[SUCCESS] Connected to MQTT Broker")
    else:
        print(f"[ERROR] Connection failed with code {rc}")

def on_publish(client, userdata, mid):
    """Callback when message is published"""
    print(f"[INFO] Message {mid} published")

def main():
    """Main publisher loop"""
    # Create MQTT client
    client = mqtt.Client(protocol=mqtt.MQTTv311)
    
    # Set credentials
    client.username_pw_set(USERNAME, PASSWORD)
    
    # Configure TLS
    client.tls_set(
        tls_version=ssl.PROTOCOL_TLSv1_2,
        cert_reqs=ssl.CERT_NONE
    )
    client.tls_insecure_set(True)
    
    # Set callbacks
    client.on_connect = on_connect
    client.on_publish = on_publish
    
    # Connect to broker
    print(f"[INFO] Connecting to broker {BROKER}:{PORT}...")
    client.connect(BROKER, PORT, 60)
    client.loop_start()
    
    try:
        print("[INFO] Starting data publication. Press Ctrl+C to stop.")
        message_count = 0
        
        while True:
            # Generate random sensor values
            int_value = random.randint(0, 1000)
            float_value = round(random.uniform(0.0, 100.0), 4)
            
            # Create JSON payloads
            payload_int = json.dumps({"value": int_value})
            payload_float = json.dumps({"value": float_value})
            
            # Publish messages
            result_int = client.publish(TOPIC_INT, payload_int, qos=1)
            result_float = client.publish(TOPIC_FLOAT, payload_float, qos=1)
            
            # Log publications
            message_count += 1
            print(f"\n[PUBLISH #{message_count}]")
            print(f"  {TOPIC_INT} -> {payload_int}")
            print(f"  {TOPIC_FLOAT} -> {payload_float}")
            
            # Wait before next publication
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n[STOP] Publisher stopped by user")
    
    finally:
        client.loop_stop()
        client.disconnect()
        print("[INFO] Disconnected from broker")

if __name__ == "__main__":
    main()
