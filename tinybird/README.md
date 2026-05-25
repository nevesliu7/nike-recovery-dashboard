# Tinybird Data API Layer

This folder documents the Path C data layer for the Nike dashboard.

The Dash app can run in two modes:

- `DATA_BACKEND=local`: reads the CSV files in `data/`. This is the default so graders can run the app without credentials.
- `DATA_BACKEND=tinybird`: reads the same logical tables from Tinybird SQL Pipe API endpoints.

## Expected Data Sources

Create Tinybird Data Sources with these names:

| Data Source | Local CSV |
| --- | --- |
| `nike_quarterly_metrics` | `data/nike_quarterly_metrics.csv` |
| `nike_divisional_revenue` | `data/nike_divisional_revenue.csv` |
| `nike_news_sentiment` | `data/gdelt_nike_news_sentiment.csv` |
| `nke_stock_prices` | `data/nke_stock_prices.csv` |
| `nike_social_snapshot` | `data/nike_social_snapshot.csv` |
| `nike_instagram_followers` | `data/nike_instagram_followers.csv` |

## Expected Pipe Endpoints

Create the SQL Pipes in `tinybird/pipes/` and publish each final node as an endpoint:

| Pipe | App env var |
| --- | --- |
| `nike_quarterly_metrics_api` | `TINYBIRD_PIPE_QUARTERLY` |
| `nike_divisional_revenue_api` | `TINYBIRD_PIPE_DIVISIONAL` |
| `nike_news_sentiment_api` | `TINYBIRD_PIPE_SENTIMENT` |
| `nke_stock_prices_api` | `TINYBIRD_PIPE_STOCK` |
| `nike_social_snapshot_api` | `TINYBIRD_PIPE_SOCIAL` |
| `nike_instagram_followers_api` | `TINYBIRD_PIPE_INSTAGRAM` |

## Render Environment Variables

Use these values for a full Path C deployment:

```text
DATA_BACKEND=tinybird
TINYBIRD_API_BASE=https://api.us-east.tinybird.co
TINYBIRD_TOKEN=<read token for published pipes>
REQUIRE_TINYBIRD=true
```

For a safer classroom demo, keep `REQUIRE_TINYBIRD=false`; the app will fall back to local CSVs if the API token is missing or expired.
