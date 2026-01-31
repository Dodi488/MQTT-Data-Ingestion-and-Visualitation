# Quick Start Guide - IoT MQTT Data Ingestion Pipeline

## ⚡ Fast Setup (5 minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Setup Database
```bash
# Login to PostgreSQL
sudo -u postgres psql

# Run these commands:
CREATE DATABASE iot_course;
CREATE USER iot_usr WITH PASSWORD 'upy_student_Admin1';
GRANT ALL PRIVILEGES ON DATABASE iot_course TO iot_usr;

# Connect to the database
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

# Exit
\q
```

### Step 3: Test System
```bash
python test_system.py
```

If all tests pass, proceed to Step 4.

### Step 4: Run the Pipeline

Open **3 separate terminals**:

**Terminal 1 - Start Subscriber:**
```bash
python mqtt_subscriber.py
```

**Terminal 2 - Start Publisher:**
```bash
python mqtt_publisher.py
```

**Terminal 3 - Launch Dashboard:**
```bash
streamlit run streamlit_dashboard.py
```

### Step 5: View Results

- Dashboard opens automatically at: http://localhost:8501
- Watch real-time data flowing through the system
- Check terminals for logs

---

## 🎯 What You Should See

### Subscriber Terminal:
```
[SUCCESS] Connected to MQTT Broker
[INFO] Subscribed to topic: #
[RECEIVED] Topic: sensor/data/int
[DATA] Value: 567 (Type: int)
[DB] Inserted INT: 567 into lake_raw_data_int
```

### Publisher Terminal:
```
[PUBLISH #1]
  sensor/data/int -> {"value": 567}
  sensor/data/float -> {"value": 45.6789}
```

### Dashboard:
- Real-time graphs updating every 5 seconds
- Statistics showing mean, min, max values
- Data tables with recent records

---

## 🔧 Troubleshooting

### Can't connect to database?
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Start if not running
sudo systemctl start postgresql
```

### Module not found errors?
```bash
pip install -r requirements.txt
```

### MQTT connection failed?
- Check your internet connection
- Verify credentials in the code
- The CloudAMQP broker should be accessible

### No data in dashboard?
1. Make sure subscriber is running first
2. Check subscriber terminal for "[DB] Inserted" messages
3. Verify database has records:
```bash
psql -U iot_usr -d iot_course -c "SELECT COUNT(*) FROM lake_raw_data_int;"
```

---

## 📊 Project Structure

```
iot_mqtt_project/
├── mqtt_publisher.py          # Generates and publishes data
├── mqtt_subscriber.py         # Receives data and stores in DB
├── streamlit_dashboard.py     # Visualizes data
├── database_setup.sql         # Database schema
├── test_system.py            # System tests
├── config.py                 # Configuration management
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
└── README.md                # Full documentation
```

---

## ✅ Checklist

- [ ] Python 3.8+ installed
- [ ] PostgreSQL installed and running
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Database created and configured
- [ ] System tests passed (`python test_system.py`)
- [ ] Subscriber running
- [ ] Publisher running
- [ ] Dashboard accessible

---

## 🎓 For Your Report

### Screenshots to capture:
1. **Database tables** with data:
   ```sql
   SELECT * FROM lake_raw_data_int LIMIT 10;
   SELECT * FROM lake_raw_data_float LIMIT 10;
   ```

2. **Subscriber terminal** showing data ingestion

3. **Publisher terminal** showing data publication

4. **Dashboard** showing graphs and statistics

### Architecture Diagram Components:
- MQTT Publisher (mqtt_publisher.py)
- MQTT Broker (CloudAMQP - bird.lmq.cloudamqp.com)
- MQTT Subscriber (mqtt_subscriber.py)
- PostgreSQL Database (localhost:5432)
- Streamlit Dashboard (streamlit_dashboard.py)

### Data Flow:
1. Publisher generates random int/float values
2. Values published to MQTT broker via topics
3. Subscriber receives messages from broker
4. Subscriber parses JSON and stores in PostgreSQL
5. Dashboard queries database and visualizes data

---

## 🚀 Next Steps

1. Let the system run for 5-10 minutes to collect data
2. Take screenshots for your report
3. Explore the dashboard features
4. Try different time filters
5. Review the code and understand each component

---

## 📝 Notes

- Default publish interval: 2 seconds
- Default dashboard refresh: 5 seconds
- Integer range: 0-1000
- Float range: 0.0-100.0
- QoS level: 1 (at least once delivery)

---

## 🆘 Need Help?

1. Run the test script: `python test_system.py`
2. Check the README.md for detailed documentation
3. Review error messages in terminal outputs
4. Verify all services are running

---

**Good luck with your project! 🎉**
