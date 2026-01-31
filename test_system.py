"""
Test Script for IoT Data Ingestion Pipeline
Tests database connectivity, MQTT connection, and basic functionality
"""

import sys
import psycopg2
import paho.mqtt.client as mqtt
import ssl
from datetime import datetime

# Configuration
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "iot_course",
    "user": "iot_usr",
    "password": "upy_student_Admin1"
}

MQTT_CONFIG = {
    "broker": "bird.lmq.cloudamqp.com",
    "port": 8883,
    "username": "ygvefxav:ygvefxav",
    "password": "7IP9KbugtgqrlgcgNXo4KXy65mpaRNnn"
}

def print_section(title):
    """Print formatted section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def test_database():
    """Test database connection and table existence"""
    print_section("DATABASE CONNECTIVITY TEST")
    
    try:
        # Connect to database
        print("[1/4] Attempting to connect to database...")
        conn = psycopg2.connect(**DB_CONFIG)
        print("✓ Successfully connected to database")
        
        # Create cursor
        cur = conn.cursor()
        
        # Test table existence
        print("\n[2/4] Checking if tables exist...")
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name IN ('lake_raw_data_int', 'lake_raw_data_float')
        """)
        tables = cur.fetchall()
        
        if len(tables) == 2:
            print("✓ Both tables exist:")
            for table in tables:
                print(f"  - {table[0]}")
        else:
            print("✗ Missing tables! Please run database_setup.sql")
            return False
        
        # Test table structure
        print("\n[3/4] Verifying table structure...")
        
        # Check int table
        cur.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'lake_raw_data_int'
            ORDER BY ordinal_position
        """)
        int_columns = cur.fetchall()
        print("✓ lake_raw_data_int columns:")
        for col in int_columns:
            print(f"  - {col[0]}: {col[1]}")
        
        # Check float table
        cur.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'lake_raw_data_float'
            ORDER BY ordinal_position
        """)
        float_columns = cur.fetchall()
        print("\n✓ lake_raw_data_float columns:")
        for col in float_columns:
            print(f"  - {col[0]}: {col[1]}")
        
        # Test data retrieval
        print("\n[4/4] Testing data retrieval...")
        
        cur.execute("SELECT COUNT(*) FROM lake_raw_data_int")
        int_count = cur.fetchone()[0]
        print(f"✓ Integer records: {int_count}")
        
        cur.execute("SELECT COUNT(*) FROM lake_raw_data_float")
        float_count = cur.fetchone()[0]
        print(f"✓ Float records: {float_count}")
        
        # Close connection
        cur.close()
        conn.close()
        
        print("\n✓ Database test PASSED")
        return True
        
    except psycopg2.Error as e:
        print(f"\n✗ Database test FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        return False

def test_mqtt():
    """Test MQTT broker connection"""
    print_section("MQTT CONNECTIVITY TEST")
    
    connection_success = [False]
    
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            connection_success[0] = True
            print("✓ Successfully connected to MQTT broker")
        else:
            print(f"✗ Connection failed with code: {rc}")
    
    try:
        print("[1/3] Creating MQTT client...")
        client = mqtt.Client(protocol=mqtt.MQTTv311)
        print("✓ MQTT client created")
        
        print("\n[2/3] Configuring authentication and TLS...")
        client.username_pw_set(MQTT_CONFIG["username"], MQTT_CONFIG["password"])
        client.tls_set(
            tls_version=ssl.PROTOCOL_TLSv1_2,
            cert_reqs=ssl.CERT_NONE
        )
        client.tls_insecure_set(True)
        print("✓ Authentication and TLS configured")
        
        print("\n[3/3] Connecting to broker...")
        client.on_connect = on_connect
        client.connect(MQTT_CONFIG["broker"], MQTT_CONFIG["port"], 10)
        client.loop_start()
        
        # Wait for connection
        import time
        time.sleep(3)
        
        client.loop_stop()
        client.disconnect()
        
        if connection_success[0]:
            print("\n✓ MQTT test PASSED")
            return True
        else:
            print("\n✗ MQTT test FAILED: Could not establish connection")
            return False
            
    except Exception as e:
        print(f"\n✗ MQTT test FAILED: {e}")
        return False

def test_dependencies():
    """Test if all required Python packages are installed"""
    print_section("PYTHON DEPENDENCIES TEST")
    
    required_packages = {
        "paho.mqtt": "paho-mqtt",
        "psycopg2": "psycopg2-binary",
        "pandas": "pandas",
        "streamlit": "streamlit",
        "plotly": "plotly"
    }
    
    all_installed = True
    
    for module_name, package_name in required_packages.items():
        try:
            __import__(module_name)
            print(f"✓ {package_name} is installed")
        except ImportError:
            print(f"✗ {package_name} is NOT installed")
            all_installed = False
    
    if all_installed:
        print("\n✓ Dependencies test PASSED")
        return True
    else:
        print("\n✗ Dependencies test FAILED")
        print("\nInstall missing packages with:")
        print("  pip install -r requirements.txt")
        return False

def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("  IOT DATA INGESTION PIPELINE - SYSTEM TEST")
    print("  " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 60)
    
    results = {
        "Dependencies": test_dependencies(),
        "Database": test_database(),
        "MQTT": test_mqtt()
    }
    
    # Summary
    print_section("TEST SUMMARY")
    
    all_passed = True
    for test_name, result in results.items():
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name:20s} {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("  ALL TESTS PASSED ✓")
        print("  System is ready to use!")
    else:
        print("  SOME TESTS FAILED ✗")
        print("  Please fix the issues above before proceeding.")
    print("=" * 60 + "\n")
    
    return all_passed

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
