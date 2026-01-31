-- Database Setup Script for IoT Data Ingestion Pipeline
-- This script creates the necessary database, user, and tables

-- ============================================
-- STEP 1: Database and User Creation
-- ============================================
-- Run these commands as PostgreSQL superuser (e.g., postgres)

-- Create database
CREATE DATABASE iot_course;

-- Create user
CREATE USER iot_usr WITH PASSWORD 'upy_student_Admin1';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE iot_course TO iot_usr;

-- ============================================
-- STEP 2: Connect to the database
-- ============================================
-- Connect to iot_course database before running the following commands
-- \c iot_course

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO iot_usr;

-- ============================================
-- STEP 3: Create Tables
-- ============================================

-- Table for integer sensor data
CREATE TABLE lake_raw_data_int (
    id BIGSERIAL PRIMARY KEY,
    topic TEXT NOT NULL,
    payload TEXT NOT NULL,
    value BIGINT NOT NULL,
    ts TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Table for floating-point sensor data
CREATE TABLE lake_raw_data_float (
    id BIGSERIAL PRIMARY KEY,
    topic TEXT NOT NULL,
    payload TEXT NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    ts TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ============================================
-- STEP 4: Create Indexes for Better Performance
-- ============================================

-- Index on timestamp for time-based queries
CREATE INDEX idx_int_timestamp ON lake_raw_data_int(ts DESC);
CREATE INDEX idx_float_timestamp ON lake_raw_data_float(ts DESC);

-- Index on topic for topic-based filtering
CREATE INDEX idx_int_topic ON lake_raw_data_int(topic);
CREATE INDEX idx_float_topic ON lake_raw_data_float(topic);

-- ============================================
-- STEP 5: Grant Table Permissions
-- ============================================

-- Grant all privileges on tables to iot_usr
GRANT ALL PRIVILEGES ON TABLE lake_raw_data_int TO iot_usr;
GRANT ALL PRIVILEGES ON TABLE lake_raw_data_float TO iot_usr;

-- Grant sequence privileges (for BIGSERIAL)
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO iot_usr;

-- ============================================
-- STEP 6: Verification Queries
-- ============================================

-- Check tables exist
SELECT tablename FROM pg_tables WHERE schemaname = 'public';

-- Check table structure for integers
\d lake_raw_data_int

-- Check table structure for floats
\d lake_raw_data_float

-- ============================================
-- Optional: Sample Data Insertion (for testing)
-- ============================================

-- Insert sample integer data
INSERT INTO lake_raw_data_int (topic, payload, value) 
VALUES 
    ('sensor/data/int', '{"value": 42}', 42),
    ('sensor/data/int', '{"value": 100}', 100),
    ('sensor/data/int', '{"value": 255}', 255);

-- Insert sample float data
INSERT INTO lake_raw_data_float (topic, payload, value) 
VALUES 
    ('sensor/data/float', '{"value": 23.45}', 23.45),
    ('sensor/data/float', '{"value": 67.89}', 67.89),
    ('sensor/data/float', '{"value": 12.34}', 12.34);

-- ============================================
-- Verification: Count records
-- ============================================

SELECT COUNT(*) as total_int_records FROM lake_raw_data_int;
SELECT COUNT(*) as total_float_records FROM lake_raw_data_float;

-- ============================================
-- Verification: View recent data
-- ============================================

SELECT * FROM lake_raw_data_int ORDER BY ts DESC LIMIT 10;
SELECT * FROM lake_raw_data_float ORDER BY ts DESC LIMIT 10;

-- ============================================
-- Optional: Cleanup (use with caution!)
-- ============================================

-- Truncate tables (removes all data but keeps structure)
-- TRUNCATE TABLE lake_raw_data_int;
-- TRUNCATE TABLE lake_raw_data_float;

-- Drop tables (removes structure and data)
-- DROP TABLE IF EXISTS lake_raw_data_int CASCADE;
-- DROP TABLE IF EXISTS lake_raw_data_float CASCADE;
