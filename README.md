# IoT Data Ingestion Pipeline with MQTT

## Project Overview

This project implements a complete IoT data ingestion pipeline using MQTT protocol. It simulates sensor data by publishing random integer and floating-point values, stores them in a PostgreSQL database, and visualizes the data using a Streamlit dashboard.

## Architecture

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Publisher │ ──────> │ MQTT Broker  │ ──────> │ Subscriber  │
│ (Simulator) │         │  (CloudAMQP) │         │ (Receiver)  │
└─────────────┘         └──────────────┘         └─────────────┘
                                                         │
                                                         ▼
                                                  ┌─────────────┐
                                                  │ PostgreSQL  │
                                                  │  Database   │
                                                  └─────────────┘
                                                         │
                                                         ▼
                                                  ┌─────────────┐
                                                  │  Streamlit  │
                                                  │  Dashboard  │
                                                  └─────────────┘
```

## Components

1. **MQTT Publisher** (`mqtt_publisher.py`)
   - Generates random sensor data
   - Publishes integer values to `sensor/data/int`
   - Publishes float values to `sensor/data/float`
   - Uses secure TLS connection to CloudAMQP broker

2. **MQTT Subscriber** (`mqtt_subscriber.py`)
   - Subscribes to all MQTT topics
   - Processes incoming messages
   - Stores data in PostgreSQL database
   - Separates int and float data into different tables

3. **Streamlit Dashboard** (`streamlit_dashboard.py`)
   - Real-time data visualization
   - Time-series graphs for both data types
   - Statistical analysis
   - Distribution histograms
   - Auto-refresh capability

4. **Database Schema** (`database_setup.sql`)
   - Two tables: `lake_raw_data_int` and `lake_raw_data_float`
   - Timestamps for temporal analysis
   - Indexes for query optimization

## Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- Internet connection (for MQTT broker)

## Installation

### 1. Clone or Download the Project

```bash
# Create project directory
mkdir iot_mqtt_project
cd iot_mqtt_project
```

### 2. Install Python Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Install and Configure PostgreSQL

#### On Ubuntu/Debian:
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

#### On macOS:
```bash
brew install postgresql
brew services start postgresql
```

#### On Windows:
Download and install from: https://www.postgresql.org/download/windows/

### 4. Setup Database

```bash
# Switch to postgres user (Linux)
sudo -u postgres psql

# Or connect directly (if configured)
psql -U postgres

# Run the setup script
\i database_setup.sql

# Or manually execute:
CREATE DATABASE iot_course;
CREATE USER iot_usr WITH PASSWORD 'upy_student_Admin1';
GRANT ALL PRIVILEGES ON DATABASE iot_course TO iot_usr;

# Connect to database
\c iot_course

# Create tables
CREATE TABLE lake_raw_data_int (
    id BIGSERIAL PRIMARY KEY,
    topic TEXT NOT NULL,
    payload TEXT NOT NULL,
    value BIGINT NOT NULL,
    ts TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE lake_raw_data_float (
    id BIGSERIAL PRIMARY KEY,
    topic TEXT NOT NULL,
    payload TEXT NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    ts TIMESTAMPTZ NOT NULL DEFAULT now()
);

# Grant permissions
GRANT ALL PRIVILEGES ON TABLE lake_raw_data_int TO iot_usr;
GRANT ALL PRIVILEGES ON TABLE lake_raw_data_float TO iot_usr;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO iot_usr;
```

## Configuration

### Database Configuration

Edit the `DB_CONFIG` dictionary in both `mqtt_subscriber.py` and `streamlit_dashboard.py`:

```python
DB_CONFIG = {
    "host": "localhost",      # Database host
    "port": 5432,             # Database port
    "dbname": "iot_course",   # Database name
    "user": "iot_usr",        # Database user
    "password": "upy_student_Admin1"  # Database password
}
```

### MQTT Configuration

The MQTT broker credentials are pre-configured for CloudAMQP. If you want to use your own broker, update these variables in `mqtt_publisher.py` and `mqtt_subscriber.py`:

```python
BROKER = "your-broker-address.com"
PORT = 8883  # or 1883 for non-TLS
USERNAME = "your-username"
PASSWORD = "your-password"
```

## Usage

### Step 1: Start the Subscriber

Open a terminal and run:

```bash
python mqtt_subscriber.py
```

You should see:
```
[INFO] Testing database connection...
[SUCCESS] Database connection successful
[INFO] Connecting to broker bird.lmq.cloudamqp.com:8883...
[SUCCESS] Connected to MQTT Broker
[INFO] Subscribed to topic: #
[INFO] Listening for messages. Press Ctrl+C to stop.
```

### Step 2: Start the Publisher

Open a **new terminal** and run:

```bash
python mqtt_publisher.py
```

You should see:
```
[INFO] Connecting to broker bird.lmq.cloudamqp.com:8883...
[SUCCESS] Connected to MQTT Broker
[INFO] Starting data publication. Press Ctrl+C to stop.

[PUBLISH #1]
  sensor/data/int -> {"value": 567}
  sensor/data/float -> {"value": 45.6789}
```

### Step 3: Launch the Dashboard

Open a **third terminal** and run:

```bash
streamlit run streamlit_dashboard.py
```

The dashboard will open in your browser at `http://localhost:8501`

## Dashboard Features

- **Real-time Metrics**: Total records and latest values
- **Time Series Graphs**: Separate charts for int and float data
- **Combined Comparison**: Dual-axis chart comparing both streams
- **Distribution Analysis**: Histograms showing value distribution
- **Statistics**: Mean, min, max, and standard deviation
- **Recent Records**: Table showing latest data entries
- **Auto-refresh**: Configurable refresh interval
- **Time Filtering**: View data from last 1, 6, 12, or 24 hours

## Verification

### Check Database Data

```bash
# Connect to database
psql -U iot_usr -d iot_course

# View integer data
SELECT * FROM lake_raw_data_int ORDER BY ts DESC LIMIT 10;

# View float data
SELECT * FROM lake_raw_data_float ORDER BY ts DESC LIMIT 10;

# Count records
SELECT COUNT(*) FROM lake_raw_data_int;
SELECT COUNT(*) FROM lake_raw_data_float;
```

### Expected Output

After running for a few minutes:
- Subscriber terminal shows incoming messages and database inserts
- Publisher terminal shows outgoing messages every 2 seconds
- Dashboard displays real-time graphs with increasing data points
- Database contains records with timestamps

## Troubleshooting

### Database Connection Error

**Error**: `Database connection failed: connection to server at "localhost" failed`

**Solution**:
1. Check PostgreSQL is running: `sudo systemctl status postgresql`
2. Verify credentials in `DB_CONFIG`
3. Ensure database and user exist
4. Check firewall settings

### MQTT Connection Error

**Error**: `Connection failed with code 5` (Authentication failed)

**Solution**:
1. Verify broker credentials
2. Check internet connection
3. Ensure TLS configuration is correct

### No Data in Dashboard

**Solution**:
1. Ensure subscriber is running and receiving data
2. Check database has records: `SELECT COUNT(*) FROM lake_raw_data_int;`
3. Verify database configuration in dashboard matches subscriber
4. Refresh the dashboard

### Module Not Found Error

**Error**: `ModuleNotFoundError: No module named 'paho'`

**Solution**:
```bash
pip install -r requirements.txt
```

## Project Structure

```
iot_mqtt_project/
│
├── mqtt_publisher.py          # MQTT data publisher
├── mqtt_subscriber.py         # MQTT subscriber with DB integration
├── streamlit_dashboard.py     # Streamlit visualization dashboard
├── database_setup.sql         # Database schema and setup
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Data Flow

1. **Publisher** generates random values every 2 seconds
2. **MQTT Broker** (CloudAMQP) receives and routes messages
3. **Subscriber** receives messages and validates JSON payload
4. **Database** stores values in appropriate tables (int or float)
5. **Dashboard** queries database and displays real-time visualizations

## Database Schema

### lake_raw_data_int
| Column  | Type         | Description                    |
|---------|--------------|--------------------------------|
| id      | BIGSERIAL    | Primary key (auto-increment)   |
| topic   | TEXT         | MQTT topic name                |
| payload | TEXT         | Full JSON payload              |
| value   | BIGINT       | Extracted integer value        |
| ts      | TIMESTAMPTZ  | Timestamp (auto-generated)     |

### lake_raw_data_float
| Column  | Type              | Description                    |
|---------|-------------------|--------------------------------|
| id      | BIGSERIAL         | Primary key (auto-increment)   |
| topic   | TEXT              | MQTT topic name                |
| payload | TEXT              | Full JSON payload              |
| value   | DOUBLE PRECISION  | Extracted float value          |
| ts      | TIMESTAMPTZ       | Timestamp (auto-generated)     |

## Technologies Used

- **Python 3.x**: Programming language
- **Paho MQTT**: MQTT client library
- **PostgreSQL**: Relational database
- **psycopg2**: PostgreSQL adapter for Python
- **Streamlit**: Web dashboard framework
- **Plotly**: Interactive visualization library
- **Pandas**: Data manipulation and analysis
- **CloudAMQP**: Cloud-based MQTT broker

## Security Considerations

⚠️ **Important**: The credentials in this code are for educational purposes only.

For production deployment:
1. Use environment variables for sensitive data
2. Implement proper authentication and authorization
3. Use SSL/TLS certificates for database connections
4. Rotate credentials regularly
5. Implement rate limiting and input validation
