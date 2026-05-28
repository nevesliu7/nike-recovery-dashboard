# Nike Global Brand Recovery Dashboard

This project is a data product we built using Dash and Plotly to analyze Nike's FY2026 Q1-Q3 public performance. The data layer can be served through Tinybird SQL Pipe endpoints, or through the bundled local CSV fallback so users can run it immediately. The research question we want to answer is: is Nike's FY2026 recovery broad-based, or is the rebound concentrated in specific regions and channels while other parts of the brand remain under pressure?

Live Render app: https://nike-recovery-dashboard.onrender.com

## Dashboard Features

- Line chart for Nike's core financial trajectory with selectable metrics.
- Grouped bar chart for Wholesale, NIKE Direct, and Converse revenue with channel toggles.
- Animated regional bubble chart with hover details for revenue, prior-year revenue, and YoY change.
- Sunburst chart showing regional and product revenue hierarchy.
- Public attention chart combining GDELT news volume, GDELT average tone, and NKE stock close.
- Social platform scale view for Instagram, TikTok, and YouTube.

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

## Refreshing Public Data

The repository already includes CSV files, so the app can run without refreshing. To refresh stock prices and GDELT public attention data:

```bash
python3 scripts/refresh_data.py
```

GDELT rate-limits requests, so the script intentionally waits between API calls.

## Data Sources

- Nike FY2026 Q1, Q2, and Q3 investor releases from Nike Investor Relations.
- GDELT Project DOC 2.0 API for English-language Nike news volume and average tone.
- Yahoo Finance chart API for NKE historical daily prices.
- AltIndex public Nike Instagram follower statistics.
- Social Blade public Nike TikTok profile snapshot.
- HunterTuber public Nike YouTube channel snapshot.

## Collaboration Statement

- Mike: used Claude to research the Tinybird and GDELT integration, and wrote the README. 
- Neves: used ChatGPT to research the Render deployment and the Yahoo Finance API integration, and defined the research questions.

As a co-effort, we spent one day drawing the layout of the dashboard, deciding on what charts we were going to use, and researching other data sources (GDELT, Yahoo Finance API) that can make this dashboard more insightful. We then spent another day coding together, using Codex as the debugging agent, with a tuned MD to stop it from moving on automatically without our permission, so we could actually learn from the session instead of just accepting the output.
