"""
Configuration file for IoT Data Ingestion Pipeline
Centralized configuration for all components
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# ============================================
# MQTT Broker Configuration
# ============================================
MQTT_CONFIG = {
    "broker": os.getenv("MQTT_BROKER", "bird.lmq.cloudamqp.com"),
    "port": int(os.getenv("MQTT_PORT", "8883")),
    "username": os.getenv("MQTT_USERNAME", "ygvefxav:ygvefxav"),
    "password": os.getenv("MQTT_PASSWORD", "7IP9KbugtgqrlgcgNXo4KXy65mpaRNnn"),
    "use_tls": os.getenv("MQTT_USE_TLS", "True").lower() == "true",
    "keepalive": int(os.getenv("MQTT_KEEPALIVE", "60")),
    "qos": int(os.getenv("MQTT_QOS", "1"))
}

# MQTT Topics
TOPICS = {
    "int": os.getenv("TOPIC_INT", "sensor/data/int"),
    "float": os.getenv("TOPIC_FLOAT", "sensor/data/float"),
    "subscribe_all": os.getenv("TOPIC_SUBSCRIBE", "#")
}

# ============================================
# Database Configuration
# ============================================
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "dbname": os.getenv("DB_NAME", "iot_course"),
    "user": os.getenv("DB_USER", "iot_usr"),
    "password": os.getenv("DB_PASSWORD", "upy_student_Admin1")
}

# Database Tables
DB_TABLES = {
    "int": "lake_raw_data_int",
    "float": "lake_raw_data_float"
}

# ============================================
# Publisher Configuration
# ============================================
PUBLISHER_CONFIG = {
    "publish_interval": float(os.getenv("PUBLISH_INTERVAL", "2")),  # seconds
    "int_min": int(os.getenv("INT_MIN", "0")),
    "int_max": int(os.getenv("INT_MAX", "1000")),
    "float_min": float(os.getenv("FLOAT_MIN", "0.0")),
    "float_max": float(os.getenv("FLOAT_MAX", "100.0")),
    "float_precision": int(os.getenv("FLOAT_PRECISION", "4"))
}

# ============================================
# Dashboard Configuration
# ============================================
DASHBOARD_CONFIG = {
    "refresh_interval": int(os.getenv("DASHBOARD_REFRESH", "5")),  # seconds
    "default_data_limit": int(os.getenv("DASHBOARD_DATA_LIMIT", "100")),
    "page_title": "IoT Data Ingestion Dashboard",
    "page_icon": "📊"
}

# ============================================
# Logging Configuration
# ============================================
LOGGING_CONFIG = {
    "level": os.getenv("LOG_LEVEL", "INFO"),
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
}

# ============================================
# Validation
# ============================================
def validate_config():
    """Validate configuration settings"""
    errors = []
    
    # Validate MQTT configuration
    if not MQTT_CONFIG["broker"]:
        errors.append("MQTT broker is not configured")
    
    if not MQTT_CONFIG["username"] or not MQTT_CONFIG["password"]:
        errors.append("MQTT credentials are not configured")
    
    # Validate database configuration
    if not DB_CONFIG["host"]:
        errors.append("Database host is not configured")
    
    if not DB_CONFIG["dbname"]:
        errors.append("Database name is not configured")
    
    if not DB_CONFIG["user"] or not DB_CONFIG["password"]:
        errors.append("Database credentials are not configured")
    
    return errors

# ============================================
# Display Configuration (for debugging)
# ============================================
def display_config(hide_secrets=True):
    """Display current configuration"""
    print("=" * 60)
    print("CONFIGURATION")
    print("=" * 60)
    
    print("\nMQTT Broker:")
    print(f"  Broker: {MQTT_CONFIG['broker']}:{MQTT_CONFIG['port']}")
    print(f"  Username: {MQTT_CONFIG['username']}")
    if hide_secrets:
        print(f"  Password: {'*' * 10}")
    else:
        print(f"  Password: {MQTT_CONFIG['password']}")
    print(f"  Use TLS: {MQTT_CONFIG['use_tls']}")
    
    print("\nMQTT Topics:")
    print(f"  Integer: {TOPICS['int']}")
    print(f"  Float: {TOPICS['float']}")
    print(f"  Subscribe: {TOPICS['subscribe_all']}")
    
    print("\nDatabase:")
    print(f"  Host: {DB_CONFIG['host']}:{DB_CONFIG['port']}")
    print(f"  Database: {DB_CONFIG['dbname']}")
    print(f"  User: {DB_CONFIG['user']}")
    if hide_secrets:
        print(f"  Password: {'*' * 10}")
    else:
        print(f"  Password: {DB_CONFIG['password']}")
    
    print("\nPublisher:")
    print(f"  Interval: {PUBLISHER_CONFIG['publish_interval']}s")
    print(f"  Int Range: {PUBLISHER_CONFIG['int_min']} - {PUBLISHER_CONFIG['int_max']}")
    print(f"  Float Range: {PUBLISHER_CONFIG['float_min']} - {PUBLISHER_CONFIG['float_max']}")
    
    print("=" * 60)

if __name__ == "__main__":
    # Validate configuration
    errors = validate_config()
    
    if errors:
        print("Configuration Errors:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("Configuration is valid!")
        display_config()
