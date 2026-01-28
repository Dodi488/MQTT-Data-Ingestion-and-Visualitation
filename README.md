# MQTT IoT Data Ingestion and Visualization

## Project Overview
This project implements a basic IoT data pipeline using the MQTT protocol.  
Simulated sensor data is published, ingested, stored in a database, and visualized in real time.

---

## Architecture
The system consists of:

- **MQTT Publisher** – generates random integer and floating-point data  
- **MQTT Broker** – routes messages between clients  
- **MQTT Subscriber** – captures messages and stores them in a database  
- **Database (PostgreSQL)** – persists sensor data  
- **Streamlit Dashboard** – visualizes data as time-series charts  

---

## Technologies Used
- Python  
- MQTT (Mosquitto, Paho MQTT)  
- PostgreSQL  
- Streamlit  
- Pandas  

---

## Database Schema
Two separate tables are used to store different data types:

- `lake_raw_data_int` – integer sensor data  
- `lake_raw_data_float` – floating-point sensor data  

Each record includes the topic, raw payload, parsed value, and timestamp.

---

## How to Run

### 1. Start the MQTT Broker
```bash
mosquitto

### 2. Start the subscriber
```bash
python subscriber.py

### 3. Start the publisher
```bash
python publisher.py

### 4. Launch the dashboard
```bash
streamlit run dashboard.py


---


## Data flow
1. The publisher generates random sensor values.
2. Data is published to MQTT topics.
3. The subscriber receives and stores messages in the database.
4. Streamlit queries the database and displays live charts.

---

## Output
- Database tables populated with real-time sensor data.
- Streamlit dashboard showing separate time-series graphs for integers and floats.
