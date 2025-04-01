#!/usr/bin/env python3
import sys

sys.argv = ["iss_tracker.py"]

from iss_tracker import ingest_data, get_data_range, find_closest_epoch, calculate_speed

def test_ingest_data():
    '''
    Tests ingest_data() function by ensuring data is returned as a dictionary and that "ndm" is a top level-key that exists.
    '''
    data = ingest_data()
    assert isinstance(data, dict)
    assert "ndm" in data 

def test_get_data_range():
    '''
    Tests that get_data_range() function by ensuring the returned range values are strings and that the returned timestamps are valid.
    '''
    start, end = get_data_range()
    assert isinstance(start, str) and isinstance(end, str)
    assert start != "Unknown" and end != "Unknown"

def test_find_closest_epoch():
    '''
    Tests find_closest_epoch() function by ensuring returned epoch is valid and that the returned key is expected.
    '''
    closest_entry = find_closest_epoch()
    assert closest_entry is not None
    assert "EPOCH" in closest_entry

def test_calculate_speed():
    '''
    Tests calculate_speed function() by ensuring returned speeds are valid and that the instantaneous and average speed are positive.
    '''
    inst_speed, avg_speed = calculate_speed()
    assert inst_speed is not None and avg_speed is not None
    assert inst_speed > 0
    assert avg_speed > 0
