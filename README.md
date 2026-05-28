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
|-- .env.example
|-- .gitignore
|-- app.py
|-- requirements.txt
|-- README.md
|-- render.yaml
|-- writeup.pdf
|-- writeup.md
|-- assets/
|   `-- style.css
|-- data/
|   |-- raw/
|   |-- gdelt_nike_news_sentiment.csv
|   |-- nike_divisional_revenue.csv
|   |-- nike_instagram_followers.csv
|   |-- nike_quarterly_metrics.csv
|   |-- nike_social_snapshot.csv
|   `-- nke_stock_prices.csv
|-- datasources/
|   |-- nike_divisional_revenue.datasource
|   |-- nike_instagram_followers.datasource
|   |-- nike_news_sentiment.datasource
|   |-- nike_quarterly_metrics.datasource
|   |-- nike_social_snapshot.datasource
|   `-- nke_stock_prices.datasource
|-- docs/
|-- pipes/
|   |-- nike_divisional_revenue_api.pipe
|   |-- nike_instagram_followers_api.pipe
|   |-- nike_news_sentiment_api.pipe
|   |-- nike_quarterly_metrics_api.pipe
|   |-- nike_social_snapshot_api.pipe
|   `-- nke_stock_prices_api.pipe
|-- services/
|   |-- __init__.py
|   `-- data_client.py
|-- scripts/
|   |-- check_api_backend.py
|   `-- refresh_data.py
`-- tinybird/
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
- Public Nike-related business, consumer, and social media research from Google, TikTok, and Instagram, used to help frame the research question and interpret Nike's recent recovery more cautiously.
