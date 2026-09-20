-- =====================================================================
-- Ford GoBike Data Warehouse — PostgreSQL Schema (Star Schema)
-- Part 1 of the Data Analysis Final Project
-- Fact table: fact_trips
-- Dimension tables: dim_time, dim_station, dim_user
-- =====================================================================

DROP TABLE IF EXISTS fact_trips CASCADE;
DROP TABLE IF EXISTS dim_time CASCADE;
DROP TABLE IF EXISTS dim_station CASCADE;
DROP TABLE IF EXISTS dim_user CASCADE;

-- ---------------------------------------------------------------------
-- Dimension: dim_time
-- ---------------------------------------------------------------------
CREATE TABLE dim_time (
    time_id     SERIAL PRIMARY KEY,
    date        DATE        NOT NULL,
    hour        SMALLINT    NOT NULL CHECK (hour BETWEEN 0 AND 23),
    day         SMALLINT    NOT NULL CHECK (day BETWEEN 1 AND 31),
    day_of_week VARCHAR(10) NOT NULL CHECK (day_of_week IN
                    ('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')),
    month       SMALLINT    NOT NULL CHECK (month BETWEEN 1 AND 12),
    year        SMALLINT    NOT NULL,
    UNIQUE (date, hour)
);

-- ---------------------------------------------------------------------
-- Dimension: dim_station
-- ---------------------------------------------------------------------
CREATE TABLE dim_station (
    station_id   SERIAL PRIMARY KEY,
    station_name VARCHAR(150) NOT NULL,
    latitude     NUMERIC(9,6) NOT NULL,
    longitude    NUMERIC(9,6) NOT NULL,
    UNIQUE (station_name)
);

-- ---------------------------------------------------------------------
-- Dimension: dim_user
-- ---------------------------------------------------------------------
CREATE TABLE dim_user (
    user_id    SERIAL PRIMARY KEY,
    birth_year SMALLINT CHECK (birth_year BETWEEN 1900 AND 2020),
    age        SMALLINT CHECK (age BETWEEN 0 AND 120),
    gender     VARCHAR(10) NOT NULL CHECK (gender IN ('Male','Female','Other')),
    user_type  VARCHAR(12) NOT NULL CHECK (user_type IN ('Subscriber','Customer'))
);

-- ---------------------------------------------------------------------
-- Fact: fact_trips
-- ---------------------------------------------------------------------
CREATE TABLE fact_trips (
    trip_id          SERIAL PRIMARY KEY,
    start_time       TIMESTAMP NOT NULL,
    end_time         TIMESTAMP NOT NULL,
    duration_sec     INTEGER   NOT NULL CHECK (duration_sec > 0),
    bike_id          INTEGER   NOT NULL,
    start_station_id INTEGER   NOT NULL REFERENCES dim_station(station_id),
    end_station_id   INTEGER   NOT NULL REFERENCES dim_station(station_id),
    user_id          INTEGER   NOT NULL REFERENCES dim_user(user_id),
    time_id          INTEGER   NOT NULL REFERENCES dim_time(time_id),
    CHECK (end_time > start_time)
);

CREATE INDEX idx_fact_trips_time    ON fact_trips(time_id);
CREATE INDEX idx_fact_trips_user    ON fact_trips(user_id);
CREATE INDEX idx_fact_trips_start   ON fact_trips(start_station_id);
CREATE INDEX idx_fact_trips_end     ON fact_trips(end_station_id);

-- =====================================================================
-- Sample data — 5 rows per dimension, 5 fact rows referencing them
-- =====================================================================

INSERT INTO dim_time (date, hour, day, day_of_week, month, year) VALUES
('2019-02-01', 8,  1, 'Friday',    2, 2019),
('2019-02-02', 17, 2, 'Saturday',  2, 2019),
('2019-02-04', 9,  4, 'Monday',    2, 2019),
('2019-02-06', 18, 6, 'Wednesday', 2, 2019),
('2019-02-08', 12, 8, 'Friday',    2, 2019);

INSERT INTO dim_station (station_name, latitude, longitude) VALUES
('Montgomery St BART Station (Market St at 2nd St)', 37.789625, -122.400811),
('The Embarcadero at Steuart St',                      37.791464, -122.391034),
('Market St at Dolores St',                             37.769305, -122.426826),
('Powell St BART Station (Market St at 4th St)',        37.786375, -122.404904),
('Berry St at 4th St',                                  37.775880, -122.393170);

INSERT INTO dim_user (birth_year, age, gender, user_type) VALUES
(1984, 35, 'Male',   'Customer'),
(1990, 29, 'Female', 'Subscriber'),
(1972, 47, 'Male',   'Subscriber'),
(1995, 24, 'Other',  'Customer'),
(1988, 31, 'Female', 'Subscriber');

INSERT INTO fact_trips (start_time, end_time, duration_sec, bike_id,
                         start_station_id, end_station_id, user_id, time_id) VALUES
('2019-02-01 08:00:00', '2019-02-01 08:14:30', 870,  4902, 1, 5, 1, 1),
('2019-02-02 17:00:00', '2019-02-02 17:22:15', 1335, 2535, 2, 5, 2, 2),
('2019-02-04 09:00:00', '2019-02-04 09:10:20', 620,  5905, 3, 4, 3, 3),
('2019-02-06 18:00:00', '2019-02-06 18:07:45', 465,  1234, 4, 1, 4, 4),
('2019-02-08 12:00:00', '2019-02-08 12:31:00', 1860, 5678, 2, 3, 5, 5);

-- =====================================================================
-- Quick sanity-check queries
-- =====================================================================
-- SELECT * FROM fact_trips f
--   JOIN dim_time t ON f.time_id = t.time_id
--   JOIN dim_user u ON f.user_id = u.user_id
--   JOIN dim_station s1 ON f.start_station_id = s1.station_id
--   JOIN dim_station s2 ON f.end_station_id = s2.station_id;
