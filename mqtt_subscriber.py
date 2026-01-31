"""
MQTT Subscriber with Database Integration
Subscribes to MQTT topics and stores data in PostgreSQL database
"""

import ssl
import json
import paho.mqtt.client as mqtt
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

# MQTT Broker Configuration
BROKER = "bird.lmq.cloudamqp.com"
PORT = 8883
USERNAME = "ygvefxav:ygvefxav"
PASSWORD = "7IP9KbugtgqrlgcgNXo4KXy65mpaRNnn"
TOPIC = "#"  # Subscribe to all topics

# Database Configuration
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "iot_course",
    "user": "iot_usr",
    "password": "upy_student_Admin1"
}

def get_db_connection():
    """Create and return database connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        print(f"[ERROR] Database connection failed: {e}")
        return None

def insert_int(topic: str, payload: dict, value: int):
    """Insert integer data into database"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO lake_raw_data_int (topic, payload, value)
            VALUES (%s, %s, %s)
            """,
            (topic, json.dumps(payload), value)
        )
        conn.commit()
        cur.close()
        conn.close()
        print(f"[DB] Inserted INT: {value} into lake_raw_data_int")
        return True
    except psycopg2.Error as e:
        print(f"[ERROR] Failed to insert int data: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False

def insert_float(topic: str, payload: dict, value: float):
    """Insert float data into database"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO lake_raw_data_float (topic, payload, value)
            VALUES (%s, %s, %s)
            """,
            (topic, json.dumps(payload), value)
        )
        conn.commit()
        cur.close()
        conn.close()
        print(f"[DB] Inserted FLOAT: {value} into lake_raw_data_float")
        return True
    except psycopg2.Error as e:
        print(f"[ERROR] Failed to insert float data: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False

def on_connect(client, userdata, flags, rc):
    """Callback when client connects to broker"""
    if rc == 0:
        print("[SUCCESS] Connected to MQTT Broker")
        client.subscribe(TOPIC)
        print(f"[INFO] Subscribed to topic: {TOPIC}")
    else:
        print(f"[ERROR] Connection failed with code {rc}")

def on_message(client, userdata, msg):
    """Callback when message is received"""
    print(f"\n[RECEIVED] Topic: {msg.topic}")
    
    try:
        # Decode payload
        payload_str = msg.payload.decode("utf-8")
        payload_json = json.loads(payload_str)
        
        # Extract value
        value = payload_json.get("value")
        
        if value is None:
            print("[WARNING] No 'value' field in payload")
            return
        
        print(f"[DATA] Value: {value} (Type: {type(value).__name__})")
        
        # Determine data type and insert into appropriate table
        if isinstance(value, int) and not isinstance(value, bool):
            insert_int(msg.topic, payload_json, value)
        elif isinstance(value, float):
            insert_float(msg.topic, payload_json, value)
        else:
            print(f"[WARNING] Unsupported data type: {type(value).__name__}")
        
    except (UnicodeDecodeError, json.JSONDecodeError, KeyError) as e:
        print(f"[ERROR] Invalid payload: {e}")
        print(f"[RAW] {msg.payload}")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
    
    print("-" * 60)

def on_log(client, userdata, level, buf):
    """Callback for logging (optional)"""
    # Uncomment to see detailed logs
    # print(f"[LOG] {buf}")
    pass

def main():
    """Main subscriber loop"""
    # Test database connection
    print("[INFO] Testing database connection...")
    conn = get_db_connection()
    if conn:
        print("[SUCCESS] Database connection successful")
        conn.close()
    else:
        print("[ERROR] Database connection failed. Please check configuration.")
        return
    
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
    client.on_message = on_message
    client.on_log = on_log
    
    # Connect to broker
    print(f"[INFO] Connecting to broker {BROKER}:{PORT}...")
    client.connect(BROKER, PORT, keepalive=60)
    
    # Start listening
    print("[INFO] Listening for messages. Press Ctrl+C to stop.")
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n[STOP] Subscriber stopped by user")
    finally:
        client.disconnect()
        print("[INFO] Disconnected from broker")

if __name__ == "__main__":
    main()
