-- ========================================================
-- Ford GoBike Data Warehouse Schema (PostgreSQL)
-- Phase 1: Star Schema ERD Implementation
-- ========================================================

-- Drop tables if they exist to allow clean re-runs
DROP TABLE IF EXISTS fact_trips CASCADE;
DROP TABLE IF EXISTS dim_time CASCADE;
DROP TABLE IF EXISTS dim_station CASCADE;
DROP TABLE IF EXISTS dim_user CASCADE;

-- 1. Dimension Table: dim_time
CREATE TABLE dim_time (
    time_id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    hour INT CHECK (hour BETWEEN 0 AND 23),
    day INT CHECK (day BETWEEN 1 AND 31),
    day_of_week VARCHAR(15) NOT NULL,
    month INT CHECK (month BETWEEN 1 AND 12),
    year INT NOT NULL
);

-- 2. Dimension Table: dim_station
CREATE TABLE dim_station (
    station_id INT PRIMARY KEY,
    station_name VARCHAR(255) NOT NULL,
    latitude NUMERIC(9, 6) NOT NULL,
    longitude NUMERIC(9, 6) NOT NULL
);

-- 3. Dimension Table: dim_user
CREATE TABLE dim_user (
    user_id SERIAL PRIMARY KEY,
    birth_year INT CHECK (birth_year > 1900 AND birth_year <= 2019),
    age INT CHECK (age >= 10 AND age <= 120),
    gender VARCHAR(20) DEFAULT 'Other',
    user_type VARCHAR(50) NOT NULL CHECK (user_type IN ('Subscriber', 'Customer'))
);

-- 4. Fact Table: fact_trips
CREATE TABLE fact_trips (
    trip_id SERIAL PRIMARY KEY,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    duration_sec INT NOT NULL CHECK (duration_sec > 0),
    bike_id INT NOT NULL,
    start_station_id INT NOT NULL,
    end_station_id INT NOT NULL,
    user_id INT NOT NULL,
    time_id INT NOT NULL,
    CONSTRAINT fk_start_station FOREIGN KEY (start_station_id) REFERENCES dim_station(station_id) ON DELETE CASCADE,
    CONSTRAINT fk_end_station FOREIGN KEY (end_station_id) REFERENCES dim_station(station_id) ON DELETE CASCADE,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES dim_user(user_id) ON DELETE CASCADE,
    CONSTRAINT fk_time FOREIGN KEY (time_id) REFERENCES dim_time(time_id) ON DELETE CASCADE
);

-- Performance Indexes
CREATE INDEX idx_fact_start_time ON fact_trips(start_time);
CREATE INDEX idx_fact_start_station ON fact_trips(start_station_id);
CREATE INDEX idx_fact_end_station ON fact_trips(end_station_id);
CREATE INDEX idx_fact_user ON fact_trips(user_id);
CREATE INDEX idx_fact_time ON fact_trips(time_id);

-- ========================================================
-- Sample Data Insertion (5 rows per table as requested)
-- ========================================================

INSERT INTO dim_time (date, hour, day, day_of_week, month, year) VALUES
('2019-02-01', 8, 1, 'Friday', 2, 2019),
('2019-02-01', 9, 1, 'Friday', 2, 2019),
('2019-02-02', 14, 2, 'Saturday', 2, 2019),
('2019-02-03', 17, 3, 'Sunday', 2, 2019),
('2019-02-04', 8, 4, 'Monday', 2, 2019);

INSERT INTO dim_station (station_id, station_name, latitude, longitude) VALUES
(21, 'Montgomery St BART Station (Market St at 2nd St)', 37.789625, -122.400811),
(13, 'Commercial St at Montgomery St', 37.794231, -122.402923),
(23, 'The Embarcadero at Steuart St', 37.791464, -122.391034),
(81, 'Berry St at 4th St', 37.775880, -122.393170),
(15, 'San Francisco Ferry Building (Harry Bridges Plaza)', 37.795392, -122.394203);

INSERT INTO dim_user (birth_year, age, gender, user_type) VALUES
(1984, 35, 'Male', 'Customer'),
(1990, 29, 'Female', 'Subscriber'),
(1995, 24, 'Male', 'Subscriber'),
(1975, 44, 'Female', 'Customer'),
(1968, 51, 'Other', 'Subscriber');

INSERT INTO fact_trips (start_time, end_time, duration_sec, bike_id, start_station_id, end_station_id, user_id, time_id) VALUES
('2019-02-01 08:15:00', '2019-02-01 08:27:00', 720, 4902, 21, 13, 1, 1),
('2019-02-01 09:05:00', '2019-02-01 09:18:00', 780, 2535, 23, 81, 2, 2),
('2019-02-02 14:10:00', '2019-02-02 14:35:00', 1500, 1435, 15, 21, 3, 3),
('2019-02-03 17:20:00', '2019-02-03 17:42:00', 1320, 3120, 81, 23, 4, 4),
('2019-02-04 08:30:00', '2019-02-04 08:44:00', 840, 5211, 13, 15, 5, 5);