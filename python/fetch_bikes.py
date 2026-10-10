"""
Data Extraction Script
- Connects to the live Transport for London (TfL) BikePoint API.
- Archives raw JSON snapshots locally for complete auditability.

Technical References:
- Python Requests Library: https://requests.readthedocs.io/
- Python File I/O Tutorial: https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files
"""

import os
import requests
import json
from datetime import datetime

def fetch_tfl_data():
    url = "https://api.tfl.gov.uk/BikePoint"
    print("Connecting to TfL API...")
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        os.makedirs("data/raw", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = f"data/raw/bike_points_{timestamp}.json"
        
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Success! Raw data saved to {filepath}")
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")

if __name__ == "__main__":
    fetch_tfl_data()