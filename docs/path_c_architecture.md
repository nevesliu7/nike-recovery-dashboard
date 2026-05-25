# Path C Architecture

The project is structured as an API-backed data product:

```text
Tinybird Data Sources -> Tinybird SQL Pipe Endpoints -> Dash app -> Render URL
                                      |
                                      `-> GitHub project record
```

## Layer Responsibilities

| Layer | Tool | Role |
| --- | --- | --- |
| Data API | Tinybird | Stores/query public Nike datasets and exposes SQL Pipe endpoints. |
| App | Dash + Plotly | Provides viewer-facing filters, charts, hover details, animation, and narrative framing. |
| Runtime | Render | Runs the Python app as a web service and provides a shareable URL. |
| Record | GitHub | Holds code, README, requirements, data sample, PDF writeup, and architecture evidence. |

## Data Flow

1. Public source data is cleaned into CSV files under `data/`.
2. The same CSV files can be uploaded to Tinybird as Data Sources.
3. SQL pipes in `tinybird/pipes/` expose endpoint-ready result sets.
4. `services/data_client.py` requests the endpoints when `DATA_BACKEND=tinybird`.
5. If the API is unavailable and `REQUIRE_TINYBIRD=false`, the app falls back to local CSVs.

## Why This Is Path C

Path A would stop at a GitHub repository. Path B would add Render hosting. This project adds a separate API data layer so the app is no longer required to own all data files directly. That separation makes the data reusable, queryable, and easier to update without changing the dashboard code.
