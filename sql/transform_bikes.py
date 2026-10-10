"""
Data Transformation & Loading Script (OLAP)
- Automatically detects the latest raw JSON snapshot.
- Parses nested TfL properties in Python.
- Uses Pandas DataFrame as a bridge to load structured data into DuckDB.

Technical References:
- Pandas DataFrame Documentation: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html
- DuckDB Python API & Pandas Integration: https://duckdb.org/docs/api/python/pandas
- W3Schools Python Dictionaries: https://www.w3schools.com/python/python_dictionaries.asp
"""

import os
import glob
import json
import pandas as pd
import duckdb

def transform_data():
    raw_files = glob.glob("data/raw/bike_points_*.json")
    if not raw_files:
        print("No raw JSON files found! Run fetch_bikes.py first.")
        return
    
    latest_file = max(raw_files, key=os.path.getctime)
    print(f"Processing latest raw file: {latest_file}")
    
    with open(latest_file, "r") as f:
        data = json.load(f)
        
    stations = []
    for item in data:
        station_id = item.get("id")
        station_name = item.get("commonName")
        lat = item.get("lat")
        lon = item.get("lon")
        
        bikes_available = 0
        empty_docks = 0
        total_docks = 0
        
        for prop in item.get("additionalProperties", []):
            key = prop.get("key")
            val = prop.get("value")
            if key == "NbBikes":
                try: bikes_available = int(val)
                except: pass
            elif key == "NbEmptyDocks":
                try: empty_docks = int(val)
                except: pass
            elif key == "NbDocks":
                try: total_docks = int(val)
                except: pass
                
        stations.append({
            "station_id": station_id,
            "station_name": station_name,
            "latitude": lat,
            "longitude": lon,
            "bikes_available": bikes_available,
            "empty_docks": empty_docks,
            "total_docks": total_docks
        })
    
    # Convert list of dicts to a Pandas DataFrame (natively supported by DuckDB)
    df = pd.DataFrame(stations)
    
    con = duckdb.connect("bikes.duckdb")
    con.execute("DROP TABLE IF EXISTS fact_bike_stations;")
    
    # Create DuckDB table from the Pandas DataFrame
    con.execute("CREATE TABLE fact_bike_stations AS SELECT * FROM df;")
    
    count = con.execute("SELECT COUNT(*) FROM fact_bike_stations;").fetchone()[0]
    print(f"Transformation complete! Loaded {count} stations into DuckDB table `fact_bike_stations`.")
    con.close()

if __name__ == "__main__":
    transform_data()