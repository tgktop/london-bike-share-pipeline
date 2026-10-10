"""
Web Bridge Exporter Script (Version 2)
- Queries local DuckDB OLAP database.
- Computes system-wide aggregates (Total Stations, Available Bikes, Empty Docks).
- Packages row-level station data for the frontend web bridge.

Technical References:
- DuckDB Aggregate Functions: https://duckdb.org/docs/sql/aggregates
- Python JSON Module: https://docs.python.org/3/library/json.html
"""

import duckdb
import json

def export_dashboard_data():
    con = duckdb.connect("bikes.duckdb", read_only=True)
    
    # Compute system-wide aggregate metrics for Version 2 dashboard cards
    total_stations = con.execute("SELECT COUNT(*) FROM fact_bike_stations;").fetchone()[0]
    total_bikes = con.execute("SELECT SUM(bikes_available) FROM fact_bike_stations;").fetchone()[0]
    total_empty_docks = con.execute("SELECT SUM(empty_docks) FROM fact_bike_stations;").fetchone()[0]
    
    rows = con.execute("""
        SELECT station_id, station_name, latitude, longitude, bikes_available, empty_docks, total_docks 
        FROM fact_bike_stations
    """).fetchall()
    
    stations_list = []
    for r in rows:
        stations_list.append({
            "station_id": r[0],
            "station_name": r[1],
            "latitude": r[2],
            "longitude": r[3],
            "bikes_available": r[4],
            "empty_docks": r[5],
            "total_docks": r[6]
        })
        
    payload = {
        "total_stations": total_stations,
        "total_bikes": total_bikes if total_bikes else 0,
        "total_empty_docks": total_empty_docks if total_empty_docks else 0,
        "stations": stations_list
    }
    
    # Export bridge file to root and app directories
    with open("dashboard_data.json", "w") as f:
        json.dump(payload, f, indent=4)
        
    with open("app/dashboard_data.json", "w") as f:
        json.dump(payload, f, indent=4)
        
    print(f"Exported Version 2 payload ({total_stations} stations) to web bridge JSON files!")
    con.close()

if __name__ == "__main__":
    export_dashboard_data()