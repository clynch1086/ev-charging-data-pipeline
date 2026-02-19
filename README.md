# EV Charging Data Pipeline

Production-ready ETL pipeline for analyzing electric vehicle (EV) charging session data using Python and MySQL.

---

## Project Overview

This project implements a production-style ETL pipeline that ingests electric vehicle charging session data from a CSV dataset, loads it into a MySQL database, performs SQL-based transformations, and generates analytical dashboards.

The pipeline demonstrates:

- Incremental data ingestion
- Persistent storage in MySQL
- SQL transformations
- Monitoring via metadata tracking
- Reproducible deployment from GitHub

The final outputs include aggregated tables and visual dashboards showing:

- Total charging sessions by location
- Average energy consumed
- Energy demand by day of week
- Cost and efficiency metrics
- Charger type distribution

---

## Repository Structure

ev-charging-data-pipeline/
│
├── data/
│ └── raw/ # Raw EV charging dataset (CSV)
│
├── sql/
│ └── transform_data.sql # SQL transformation logic
│
├── src/
│ ├── main.py # Pipeline entry point
│ ├── load_raw_data.py # Incremental ingestion logic
│ ├── dashboard.py # Visualization logic
│ └── db.py # Database connection utility
│
├── requirements.txt # Python dependencies
└── README.md

---

## Architecture Overview

**Source**  
CSV file containing EV charging sessions.

**Ingestion Stage**

- Loads raw data into MySQL table `raw_data`
- Implements incremental loading using:
   - `pipeline_metadata` table
   - `last_loaded_start_time` tracking

**Transformation Stage**

- SQL transformations executed in MySQL
- Aggregated analytical tables generated

**Output Stage**

- Dashboards rendered using Matplotlib
- Aggregated tables available for reporting

**Persistent Data Store**

- MySQL 8.0 database

---

## Deployment Instructions (Fully Reproducible Setup)

### 1. Clone the Repository

```bash
git clone https://github.com/clynch1086/ev-charging-data-pipeline.git
cd ev-charging-data-pipeline

```

### 2. Install python dependencies

```bash
pip install -r requirements.txt

```

### 3. Install and Configure MySQL

Install MySQL 8.0

Create a database:

    CREATE DATABASE ev_pipeline;

### 4. Run the pipeline

python src/main.py

---

## Incremental Loading Logic

The pipeline uses a metadata table:

    pipeline_metadata

Columns:
dataset_name
last_loaded_start_time
last_run timestamp

On each execution:
If no previous load exists → full dataset is loaded
If a previous load exists → only new records (based on timestamp) are appended

---

## Monitoring

Monitoring is implemented through:

### Metadata Tracking

    pipeline_metadata records last load time
    Prevents duplicate ingestion

### Console Logging

    Records loaded
    Transformation completion
    Dashboard launch confirmation

### Data Validation

    Null timestamp handling
    Timestamp parsing
    Controlled append logic

### SQL Transformations

    Aggregate session counts
    Compute average energy consumption
    Calculate charging cost metrics
    Generate energy demand summaries

### Manual Processes

The following manual steps are required:

    Install MySQL
    Create the target database
    Configure database credentials
    Install Python dependencies

All manual steps are fully documented above.
