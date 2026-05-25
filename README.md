# Nike Global Brand Recovery Dashboard

This project is a Path C API-backed data product. The Dash and Plotly interface analyzes Nike's FY2026 Q1-Q3 public performance, while the data layer can be served through Tinybird SQL Pipe endpoints or through the bundled local CSV fallback.

## Research Question

Is Nike's FY2026 recovery broad-based, or is the rebound concentrated in specific regions and channels while other parts of the brand remain under pressure?

## Dashboard Features

- Line chart for Nike's core financial trajectory with selectable metrics.
- Grouped bar chart for Wholesale, NIKE Direct, and Converse revenue with channel toggles.
- Animated regional bubble chart with hover details for revenue, prior-year revenue, and YoY change.
- Sunburst chart showing regional and product revenue hierarchy.
- Public attention chart combining GDELT news volume, GDELT average tone, and NKE stock close.
- Social platform scale view for Instagram, TikTok, and YouTube.

## Path C Architecture

```text
Tinybird API -> Dash + Plotly app -> Render web service
                         |
                         `-> GitHub project record
```

The app reads from `services/data_client.py`. By default it uses local CSV files so graders can run it immediately. For the highest-difficulty Path C deployment, set `DATA_BACKEND=tinybird` and provide a Tinybird read token in Render environment variables.

## Project Structure

```text
.
|-- app.py
|-- requirements.txt
|-- README.md
|-- render.yaml
|-- writeup.pdf
|-- writeup.md
|-- assets/
|   `-- style.css
|-- data/
|   |-- gdelt_nike_news_sentiment.csv
|   |-- nike_divisional_revenue.csv
|   |-- nike_instagram_followers.csv
|   |-- nike_quarterly_metrics.csv
|   |-- nike_social_snapshot.csv
|   `-- nke_stock_prices.csv
|-- datasources/
|   `-- Tinybird .datasource files
|-- docs/
|   `-- path_c_architecture.md
|-- pipes/
|   `-- Tinybird .pipe endpoint files
|-- services/
|   |-- __init__.py
|   `-- data_client.py
|-- scripts/
|   |-- check_api_backend.py
|   |-- make_writeup_pdf.py
|   `-- refresh_data.py
`-- tinybird/
    |-- README.md
    `-- pipes/
```

## How to Run

```bash
python3 -m pip install -r requirements.txt
python3 app.py
```

Then open the local URL printed in the terminal, usually:

```text
http://127.0.0.1:8050
```

To confirm which data layer is active:

```bash
python3 scripts/check_api_backend.py
```

## Path C Deployment

1. Upload the cleaned CSV files in `data/` to Tinybird Data Sources using the names listed in `tinybird/README.md`.
2. Create and publish the SQL Pipe endpoints listed in `tinybird/pipes/`.
3. Push this repository to GitHub.
4. Create a Render web service from the GitHub repository.
5. Use `render.yaml`, or set the Render build command to `pip install -r requirements.txt` and the start command to `gunicorn app:server`.
6. In Render environment variables, set:

```text
DATA_BACKEND=tinybird
TINYBIRD_API_BASE=https://api.us-east.tinybird.co
TINYBIRD_TOKEN=<Tinybird read token>
REQUIRE_TINYBIRD=true
```

For a classroom demo where the Tinybird token might not be available to reviewers, set `REQUIRE_TINYBIRD=false`; the dashboard will still run from the committed data sample.

## Data Sources

- Nike FY2026 Q1, Q2, and Q3 investor releases from Nike Investor Relations.
- GDELT Project DOC 2.0 API for English-language Nike news volume and average tone.
- Yahoo Finance chart API for NKE historical daily prices.
- AltIndex public Nike Instagram follower statistics.
- Social Blade public Nike TikTok profile snapshot.
- HunterTuber public Nike YouTube channel snapshot.

Financial values in `data/nike_quarterly_metrics.csv` and `data/nike_divisional_revenue.csv` are manually transcribed from Nike's official releases. Channel revenue values are rounded when the release reports rounded values in the narrative bullets.

## Refreshing Public Data

The repository already includes CSV files, so the app can run without refreshing. To refresh stock prices and GDELT public attention data:

```bash
python3 scripts/refresh_data.py
```

GDELT rate-limits requests, so the script intentionally waits between API calls.

## Collaboration Statement

We used ChatGPT/Codex to help structure the project, build the Dash app, organize public data sources, add the Path C API-backed architecture, write the README, generate the PDF writeup, and debug code. The project topic, interpretation of findings, final visual choices, and final submission decisions remain the responsibility of the group members.

Group contribution: Neves proposed the original Nike FY2026 recovery idea and helped define the dashboard direction and research questions. Mike supported dashboard structure, visualization planning, API-backed publication planning, and interpretation. Both members should review the final dashboard, verify the findings, and update this statement before submission if the division of work changes.

## Submission Note

After uploading this folder to GitHub, paste the final GitHub repository URL into `writeup.md`, regenerate `writeup.pdf`, and include that link in the submitted file or course portal response.
