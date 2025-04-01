#!/usr/bin/env python3
import argparse
import logging
import socket
import math
from datetime import datetime
import xmltodict
import requests

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--loglevel', type=str, required=False, default='WARNING',
                    help='set log level to DEBUG, INFO, WARNING, ERROR, or CRITICAL')
args = parser.parse_args()

format_str=f'[%(asctime)s {socket.gethostname()}] %(filename)s:%(funcName)s:%(lineno)s - %(levelname)s: %(message)s'
logging.basicConfig(level=args.loglevel, format=format_str)

ISS_URL = 'https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml'

def ingest_data():
    '''
    Ingests ISS data from the provided URL and converts it to a dictionary.

    Returns:
        dict: Parsed ISS data.
    '''
    response = requests.get(ISS_URL)
    data = xmltodict.parse(response.text)
    return data

def get_data_range():
    '''
    Extracts the data range using the first and last timestamps (EPOCH) from the ISS data.
    
    Returns:
        Tuple (start_time, end_time) if data exists, otherwise None.
    '''
    data = ingest_data()
    entries = data.get('ndm', {}).get('oem', {}).get('body', {}).get('segment', {}).get('data', {}).get('stateVector', [])

    if isinstance(entries, list) and entries:
        start_time = entries[0].get('EPOCH', 'Unknown')
        end_time = entries[-1].get('EPOCH', 'Unknown')
        print(f'Data covers the range from {start_time} to {end_time}.')
        return start_time, end_time

def find_closest_epoch():
    '''
    Finds the epoch closest to the current time.

    Returns:
        dict: The closest ISS data entry.
    '''
    data = ingest_data()
    state_vectors = data.get('ndm', {}).get('oem', {}).get('body', {}).get('segment', {}).get('data', {}).get('stateVector', [])

    if not state_vectors:
        print("No state vector data available.")
        return None

    now = datetime.utcnow()

    def parse_epoch(epoch_str):
        '''
        Tries parsing the EPOCH string in multiple formats.
        '''
        try:
            return datetime.strptime(epoch_str, '%Y-%m-%dT%H:%M:%S.%fZ')  # Standard format
        except ValueError:
            return datetime.strptime(epoch_str, '%Y-%jT%H:%M:%S.%fZ')  # DOY format

    for entry in state_vectors:
        entry['EPOCH'] = parse_epoch(entry['EPOCH'])

    closest_entry = min(state_vectors, key=lambda entry: abs(entry['EPOCH'] - now))
    print(f'Closest Epoch: {closest_entry['EPOCH'].isoformat()}Z')
    return closest_entry

def calculate_speed() -> tuple[float, float]:
    '''
    Calculates the instantaneous and average speed of the ISS data.

    Returns:
        tuple[float, float]: (instantaneous speed, average speed) or (None, None) if data is unavailable.
    '''
    data = ingest_data()
    state_vectors = data.get('ndm', {}).get('oem', {}).get('body', {}).get('segment', {}).get('data', {}).get('stateVector', [])

    if not state_vectors:
        print('No speed data available.')
        return None, None

    latest_vector = state_vectors[-1]
    try:
        x_dot = float(latest_vector.get('X_DOT', {}).get('#text', 0))
        y_dot = float(latest_vector.get('Y_DOT', {}).get('#text', 0))
        z_dot = float(latest_vector.get('Z_DOT', {}).get('#text', 0))

        instantaneous_speed = math.sqrt(x_dot**2 + y_dot**2 + z_dot**2)
    except (ValueError, AttributeError) as e:
        print(f'Error: Invalid velocity component format. {e}')
        return None, None

    speed_sum = 0
    count = 0

    for vector in state_vectors:
        try:
            x_dot = float(vector.get('X_DOT', {}).get('#text', 0))
            y_dot = float(vector.get('Y_DOT', {}).get('#text', 0))
            z_dot = float(vector.get('Z_DOT', {}).get('#text', 0))
            speed = math.sqrt(x_dot**2 + y_dot**2 + z_dot**2)
            speed_sum += speed
            count += 1
        except (ValueError, AttributeError):
            continue

    average_speed = speed_sum / count if count > 0 else None
    print(f'Instantaneous Speed: {instantaneous_speed:.3f} km/s')
    if average_speed is not None:
        print(f'Average Speed Across Entire Dataset: {average_speed:.3f} km/s')
    else:
        print('No valid data points for average speed calculation.')
    return instantaneous_speed, average_speed

def main():
    '''
    Entry point of the script. Executes main logic.
    '''
    iss_data = ingest_data()
    if not iss_data:
        print('Error: Failed to retrieve ISS data.')
        return

    data_range = get_data_range()
    if not data_range or None in data_range:
        print('Error: Failed to retrieve data range.')
        return
    print(f'Data Range: {data_range[0]} to {data_range[1]}')

    closest_epoch = find_closest_epoch()
    if not closest_epoch:
        print('Error: Failed to find the closest epoch.')
        return
    print(f'Closest Epoch to Now: {closest_epoch['EPOCH'].isoformat()}Z')

    inst_speed, avg_speed = calculate_speed()
    if inst_speed is not None:
        print(f'Instantaneous Speed: {inst_speed:.2f} km/s')
    if avg_speed is not None:
        print(f'Average Speed: {avg_speed:.2f} km/s')

if __name__ == '__main__':
    main()
