# London Bike Share Pipeline (Version 2)

A production-grade, end-to-end data engineering portfolio project built for Data School applications. This pipeline extracts live urban mobility data from the Transport for London (TfL) BikePoint API, archives raw snapshots for data lineage, transforms the nested payload using Python and DuckDB (OLAP storage), and exports a high-performance web bridge JSON to power an interactive Leaflet.js web dashboard with real-time system metrics.

---

## 📂 Project Directory Structure

The project is organized into a clean, modular structure under the root directory:

* **`Version 2/`**
  * **`app/`**
    * `index.html` - Interactive frontend dashboard featuring system-wide metric cards, live table inventory, and Leaflet.js mapping.
    * `dashboard_data.json` - Web bridge payload exported from the OLAP database.
  * **`data/raw/`**
    * Timestamped raw JSON snapshots ensuring full data reproducibility and auditability.
  * **`python/`**
    * `fetch_bikes.py` - Data extraction script connecting to the live TfL REST API.
  * **`sql/`**
    * `transform_bikes.py` - ETL script processing raw JSON into a structured table.
    * `export_for_web.py` - Exporter script querying DuckDB to generate the web bridge JSON payload.
  * `bikes.duckdb` - Local columnar OLAP database store housing the `fact_bike_stations` table.

---

## 🚀 Pipeline Architecture & Workflow

1. **Extraction (`python/fetch_bikes.py`)**: Connects to the live TfL BikePoint API endpoint, serializes the response, and saves a timestamped raw snapshot inside `data/raw/`.
2. **Transformation & Loading (`sql/transform_bikes.py`)**: Automatically detects the latest raw snapshot, parses nested API properties via Python and Pandas, and loads clean tabular data into a `fact_bike_stations` table inside the local `bikes.duckdb` OLAP database.
3. **Web Bridge Export (`sql/export_for_web.py`)**: Queries DuckDB to compute system-wide aggregations (Total Stations, Available Bikes, Empty Docks) and packages row-level inventory into `dashboard_data.json`.
4. **Visualization (`app/index.html`)**: Asynchronously consumes the JSON payload via the Fetch API, plotting interactive markers on a Leaflet.js map and populating a searchable station directory table.

---

## 💻 How to Run the Project & View Locally

To execute this data pipeline and launch the dashboard on your local machine, open your **PowerShell** terminal and follow these steps sequentially:

1. Navigate into your project directory:
```powershell
cd "Version 2"
```

2. Execute the Data Extraction Script:
*(Connects to the live TfL API and saves a raw timestamped JSON snapshot)*
```powershell
python python/fetch_bikes.py
```

3. Run the Transformation Script:
*(Parses the raw JSON and loads clean tabular records into your DuckDB database)*
```powershell
python sql/transform_bikes.py
```

4. Export the Web Bridge Data:
*(Queries DuckDB to compute system aggregates and generate the frontend JSON payload)*
```powershell
python sql/export_for_web.py
```

5. Start the Local Web Server:
```powershell
python -m http.server 8000
```

6. Open the Local Run Link:
Once the server is running, open your web browser and navigate to:
👉 **`http://localhost:8000/app/index.html`**

---

## 💡 Key Design Decisions & Learnings

* **Why DuckDB?** Chosen for zero-configuration, lightning-fast in-process analytical querying over raw data payloads, mirroring modern columnar data warehouse patterns.
* **Decoupled Architecture:** Separating the ingestion layer (`python/`), OLAP storage (`bikes.duckdb`), and presentation layer (`app/`) ensures modularity, scalability, and clean separation of concerns.
* **Real-World Relevance:** Using live TfL transit data grounds technical data engineering in a tangible, commercial smart-city context.

---

## Where AI helped

AI served as a co-pilot throughout the build process. AI assisted with researching API payload structures, designing the decoupled ingestion-to-OLAP-to-frontend workflow, and troubleshooting Python/DuckDB integration syntax. Human oversight focused on system design choices, defining core project requirements, reviewing code, verifying pipeline outputs, and validating the final dashboard functionality.
