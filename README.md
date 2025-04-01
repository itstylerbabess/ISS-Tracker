# ISS Tracker Application with Redis and Docker Compose

## Overview

This project provides a containerized Flask application that ingests, processes, and analyzes International Space Station (ISS) orbital trajectory data. The application retrieves data from the ISS website and stores it in a Redis database container for persistence. It allows querying of the ISS data via several Flask routes and uses Docker Compose to manage both the Flask app and Redis container.

The project also calculates key statistics like speed and position for the ISS based on its orbital trajectory data, while also providing real-time geographical information (latitude, longitude, altitude, and geoposition) for a specific epoch and the nearest epoch to the current time.

## Dataset

The ISS trajectory data can be obtained from the official NASA website: [ISS Trajectory Data](https://spotthestation.nasa.gov/trajectory_data.cfm)

Two formats are available:
- **Plain text (OEM format):** [ISS OEM Text](https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.txt)
- **XML format:** [ISS OEM XML](https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml)

Both contain **15 days of state vector data**, including position, velocity, and timestamps in the J2000 reference frame. **The XML format is used for this project.** The dataset is **not included** in this repository and should be downloaded manually.

## Python3 Functions (iss_tracker.py)

- **Data ingestion:** Fetches the latest ISS trajectory data from a URL.
- **Range calculation:** Determines the first and last available timestamps.
- **Current state vector retrieval:** Finds the state vector closest to execution time.
- **Speed calculations:** Computes both **average speed over all epochs** and **instantaneous speed closest to execution time**.
- **Location calculations:** Uses latitude and longitude data to calculate geoposition for specific epochs.
- **Logging and error handling:** Includes debug, warning, and error messages for better traceability.
- **Unit tests:** Ensures reliability with pytest-based testing.

## Flask App Routes (app.py)

- **`/epochs`** – Returns the entire data set.
- **`/epochs?limit=<int>&offset=<int>`** – Returns a modified list of Epochs based on query parameters.
- **`/epochs/<epoch>`** – Returns state vectors for a specific Epoch.
- **`/epochs/<epoch>/speed`** – Returns the instantaneous speed for a specific Epoch.
- **`/epochs/<epoch>/location`** – Returns the latitude, longitude, altitude, and geoposition for a specific Epoch.
- **`/now`** – Returns instantaneous speed, latitude, longitude, altitude, and geoposition for the Epoch closest to the current time.

## Setup Instructions

### Prerequisites
- **Flask** (for web application development)
- **Docker** (for containerized execution and redis image execution)
- **Python 3.0** (for local execution)
- **pip** (for package installation)

## Starting the Services

```bash
docker compose up --build
```

## Running the Routes
```bash
curl http://127.0.0.1:5000/epochs
```
Returns the entire data set in a list-of-dictionaries format.

```bash
curl http://127.0.0.1:5000/epochs?limit=<int>&offset=<int>
```
Returns a modified list of Epochs based on query parameters. For example, ```/epochs?limit=2&offset=10``` displays two Epochs after skipping the first 10 Epochs

```bash
curl http://127.0.0.1:5000/epochs/<epoch>
```
Returns state vectors for a specific Epoch. An example input would be ```/epochs/2025-100T11:59:56.000Z.```

```bash
curl http://127.0.0.1:5000/epochs/<epoch>/speed
```
Returns the instantaneous speed for a specific Epoch.

```bash
curl http://127.0.0.1:5000/epochs/<epoch>/location
```
Returns latitude, longitude, altitude, and geoposition for a specific Epoch.

```bash
curl http://127.0.0.1:5000/now
```
Returns instantaneous speed, latitude, longitude, altitude, and geoposition for the Epoch closest to the current time.

## Notes
The script does not store the dataset; it fetches the latest available data dynamically from the ISS website.

To modify the source URL, update iss_tracker.py.

Logging and error handling ensure robustness against missing or malformed data.

The Redis container stores data backups in the ./data directory. The backups should not be committed to your Git repository.

This project follows best practices in software design and documentation and is designed to be scalable and flexible with Docker Compose for orchestration and Redis for persistence.

This project strives to adhere to best practices in software design and documentation, with guidance from ChatGPT to structure the README and refine Python implementation.