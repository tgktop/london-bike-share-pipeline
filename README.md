# London Bike Share Pipeline (Version 2)

## 👋 About Me & Project Overview

Hi, I'm Ayodele! I'm an aspiring Data Engineer applying to Data School. I built this project to showcase my approach to solving real-world data engineering problems—from fetching messy raw API data and structuring it into an analytical store to delivering an interactive dashboard for end users.

This pipeline tracks live cycle hire availability across London using the Transport for London (TfL) BikePoint API. It handles live data extraction, archives timestamped raw JSON snapshots for auditability, transforms nested API payloads using Python and DuckDB, and powers a custom Leaflet.js web dashboard with live system metrics.

---

## 🎯 Target Audience & What Problem This Solves

* **The Audience:** London commuters, local cyclists, and urban mobility analysts needing clear, real-time visibility into bike dock availability.
* **The Problem:** Standard transit apps often show static or isolated station data. This tool aggregates city-wide inventory into a central OLAP database, computing key metrics (total available bikes, empty docks, total active stations) alongside a visual map and searchable station directory.

---

## 📂 Repository Structure

The project follows a clean, modular structure:

* **`Version 2/`**
  * **`app/`**
    * `index.html` - Interactive web dashboard with metric cards, searchable data table, and Leaflet.js map.
    * `dashboard_data.json` - Web bridge JSON export generated directly from DuckDB.
  * **`data/raw/`**
    * Immutable, timestamped JSON snapshots collected from the TfL API.
  * **`python/`**
    * `fetch_bikes.py` - Ingestion script connecting to the live TfL REST endpoint.
  * **`sql/`**
    * `transform_bikes.py` - ETL script parsing raw JSON into structured relational tables.
    * `export_for_web.py` - Exporter script querying DuckDB to create the dashboard data payload.
  * `bikes.duckdb` - Local columnar OLAP database containing the `fact_bike_stations` table.

---

## 🚀 Pipeline Architecture & How It Works

1. **Extraction (`python/fetch_bikes.py`)**: Connects to TfL's BikePoint REST API and saves a raw timestamped JSON snapshot to `data/raw/`.
2. **Transformation (`sql/transform_bikes.py`)**: Automatically detects the latest raw snapshot, parses nested property arrays using Python and Pandas, and loads clean records into the `fact_bike_stations` table inside `bikes.duckdb`.
3. **Web Bridge Export (`sql/export_for_web.py`)**: Runs SQL queries against DuckDB to calculate overall network aggregates and exports the station-level detail to `app/dashboard_data.json`.
4. **Presentation (`app/index.html`)**: A lightweight frontend application that fetches `dashboard_data.json` asynchronously, plotting station markers on a map and filling out the interactive table.

---

## 💻 How to Run the Project Locally

### 🛠️ Prerequisites & Installation

Ensure you have Python 3.8+ installed. Install the required Python packages by running:

```powershell
pip install pandas duckdb requests
```

### 🏃 Step-by-Step Execution

Open PowerShell and run these steps in order:

1. Navigate to the project directory:
```powershell
cd "Version 2"
```

2. Fetch fresh TfL data (Optional - requires an active internet connection):
```powershell
python python/fetch_bikes.py
```

3. Parse the raw JSON into DuckDB:
```powershell
python sql/transform_bikes.py
```

4. Generate the dashboard JSON payload:
```powershell
python sql/export_for_web.py
```

5. Launch a local web server:
```powershell
python -m http.server 8000
```

6. Open your browser and go to:
👉 **`http://localhost:8000/app/index.html`**

---

## 💡 Key Technical Decisions

* **Why DuckDB?** I chose DuckDB because it offers fast, zero-config in-process analytical querying over raw JSON data, mirroring modern columnar data warehouse environments.
* **Raw Snapshot Archiving:** Storing raw JSON files in `data/raw/` ensures full idempotency and reproducibility. Anyone can clone this repository and rebuild the database locally without needing network access.
* **Decoupled Architecture:** Keeping ingestion, transformation, storage, and visualization strictly separated makes the pipeline modular, easier to debug, and simple to expand.

---

## 🔮 What I Would Explore Next

* **Historical Trend Analysis:** Use the growing archive of timestamped JSON snapshots to analyze station usage patterns across peak commuting hours.
* **Automated Orchestration:** Set up a lightweight scheduler (like GitHub Actions or a local cron job) to pull fresh TfL snapshots automatically throughout the day.
* **Enhanced Spatial Filters:** Add client-side radius or borough filtering to allow users to focus on specific London neighborhoods.

---

## 🤖 Where AI Helped

I used AI as a technical collaborator throughout this project. It helped me explore TfL API structure quirks, troubleshoot DuckDB integration syntax, and refine the decoupled pipeline design. My role focused on defining project requirements, making architectural choices, writing and verifying the Python/SQL scripts, and ensuring the final dashboard delivered clear, accurate metrics.
