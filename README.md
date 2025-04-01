# ISS Trajectory Analysis  

## Overview  

This project provides a containerized Flask application that ingests, processes, and analyzes International Space Station (ISS) orbital trajectory data through the utilization of a Python3 script found within the same container. The Python3 script extracts state vectors from the **Orbital Ephemeris Message (OEM)** dataset, calculates key statistics such as the range of available data, the closest state vector to the current time, and the average and instantaneous speed of the ISS. The Flask application employs these methods in various routes with the same or a similar function.

The project follows best practices in Python development, including **unit testing, logging, error handling, and proper documentation**. The README and script structure were built ultilizing **ChatGPT**, which helped to fill in knowledge gaps and aid in the clarity of the project documentation.  

## Dataset  

The ISS trajectory data can be obtained from the official NASA website: https://spotthestation.nasa.gov/trajectory_data.cfm

Two formats are available:  
- **Plain text (OEM format):** https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.txt

- **XML format:** https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml  

Both contain **15 days of state vector data**, including position, velocity, and timestamps in the J2000 reference frame. **The XML format is utilized for this project.** The dataset is **not included** in this repository and should be downloaded manually.  

## Python3 Functions (iss_tracker.py)  
- **Data ingestion:** Fetches the latest ISS trajectory data from a URL.  
- **Range calculation:** Determines the first and last available timestamps.  
- **Current state vector retrieval:** Finds the state vector closest to execution time.  
- **Speed calculations:** Computes both **average speed over all epochs** and **instantaneous speed closest to execution time**.  
- **Logging and error handling:** Includes debug, warning, and error messages for better traceability.  
- **Unit tests:** Ensures reliability with pytest-based testing.

## Flask App Routes (app.py)
- **`/epochs`** – Returns the entire data set.  
- **`/epochs?limit=int&offset=int`** – Returns a modified list of EPOCHs based on query parameters.  
- **`/epochs/<epoch>`** – Returns state vectors for a specific EPOCH from the data set.  
- **`/epochs/<epoch>/speed`** – Returns the instantaneous speed for a specific EPOCH.  
- **`/now`** – Returns state vectors and instantaneous speed for the EPOCH closest to the current time.

## Setup Instructions  

### Prerequisites  
- **Flask** (for web application development)
- **Docker** (for containerized execution)  
- **Python 3.0** (for local execution)  
- **pip** (for package installation)  

## Build the Docker Image 

```bash
docker build -t homework05:1.0 .
```

## Run the Containerized Flask App  

**First, start Flask app in the foreground:**
```bash
docker run --rm homework05:1.0 app.py
```
**then, in a new terminal, begin running routes:**

```bash
curl http://127.0.0.1:5000/epochs
```
Returns the entire data set in a list-of-dictionaries format.

```bash
curl http://127.0.0.1:5000/epochs?limit=<int>&offset=<int> 
```
Returns a modified list of EPOCHs based on query parameters. For example, ```/epochs?limit=2&offset=10``` displays two EPOCHs after skipping the first 10 EPOCHs within the dataset.

```bash
curl http://127.0.0.1:5000/epochs/<epoch> 
```
Returns state vectors for a specific EPOCH from the data set. An example input would be ```/epochs/2025-100T11:59:56.000Z```

```bash
curl http://127.0.0.1:5000/epochs/<epoch>/speed 
```
Returns the instantaneous speed for a specific EPOCH.
    
```bash
curl http://127.0.0.1:5000/now 
```
Returns state vectors and instantaneous speed for the EPOCH closest to the current time.

### Running Tests  

### Run the Containerized Unit Test

```bash
docker run --rm homework05:1.0 pytest
```

## Code Structure  
```
📂 homework05
 ├── 📄 iss_tracker.py         # Main script for fetching and processing ISS data
 ├── 📄 test_iss_tracker.py    # Function unit tests
 ├── 📄 app.py                 # Flask app for routing ISS data
 ├── 📄 Dockerfile             # Docker configuration
 ├── 🖼️ diagram.png            # Syotwared diagram
 ├── 📄 README.md              # Project documentation
```

## Notes  

- The script **does not store the dataset**; it fetches the latest available data dynamically.  
- To modify the source URL, update `iss_tracker.py`.  
- Logging and error handling ensure robustness against missing or malformed data.  

---

This project strives to adhere to **best practices in software design and documentation**, with guidance from ChatGPT to structure the README and refine Python implementation.