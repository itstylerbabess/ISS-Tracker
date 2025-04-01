#!/usr/bin/env python3
import redis
import argparse
import logging
import socket
import math
from datetime import datetime
import xmltodict
import requests
import json
from flask import Flask, jsonify, request
from iss_tracker import ingest_data, find_closest_epoch, calculate_speed 

app = Flask(__name__)
rd = redis.Redis(host='redis-db', port=6379, decode_responses=True)

def load_data_into_redis():
    data = ingest_data()['ndm']['oem']['body']['segment']['data']['stateVector']
    for entry in data:
        epoch = entry['EPOCH']
        sv = json.dumps(entry)
        rd.set(epoch, sv)
        
@app.route('/epochs', methods=['GET'])
def epochs():
    '''
    Retrieves a list of state vectors with optional limits and offset.
    '''
    data = []
    for key in rd.keys():
        data.append(json.loads(rd.get(key)))
    limit = request.args.get('limit', default=len(data), type=int)
    offset = request.args.get('offset', default=0, type=int)
    return jsonify(data[offset:offset+limit])

@app.route('/epochs/<epoch>', methods=['GET'])
def epoch(epoch):
    '''
    Retrieves the state vector for a specific epoch.
    '''
#TYLER I LEFT OFF HERE ! THERE IS SOMETHING EXTRA!

    data = []
    for key in rd.keys():
        data.append(json.loads(rd.get(key)))
        if entry['EPOCH'] == epoch:
            return json.loads(entry)
    return json.loads({'error': 'Epoch not found'}), 404

@app.route('/epochs/<epoch>/speed', methods=['GET'])
def epoch_speed(epoch):
    '''
    Calculates and returns the speed of the object at a specific epoch.
    '''
    data = ingest_data()['ndm']['oem']['body']['segment']['data']['stateVector']
    for entry in data:
        if entry['EPOCH'] == epoch:
            x_dot = float(entry["X_DOT"]["#text"])
            y_dot = float(entry["Y_DOT"]["#text"])
            z_dot = float(entry["Z_DOT"]["#text"])
            speed = (x_dot**2 + y_dot**2 + z_dot**2) ** 0.5
            return jsonify({'EPOCH': epoch, 'Speed': speed})
    return jsonify({'error': 'Epoch not found'}), 404

@app.route('/now', methods=['GET'])
def now():
    '''
    Retrieves the closest epoch's state vector and calculate its speed.
    '''
    closest_epoch = find_closest_epoch()
    if closest_epoch:
        x_dot = float(closest_epoch['X_DOT']['#text'])
        y_dot = float(closest_epoch['Y_DOT']['#text'])
        z_dot = float(closest_epoch['Z_DOT']['#text'])
        speed = (x_dot**2 + y_dot**2 + z_dot**2) ** 0.5
        return jsonify({'EPOCH': closest_epoch['EPOCH'], 'state_vector': closest_epoch, 'Speed': speed})
    return jsonify({'error': 'No data available'}), 404

if __name__ == '__main__':
    if len(rd.keys()) == 0:
        load_data_into_redis()
    app.run(debug=True, host='0.0.0.0')
