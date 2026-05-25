from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


def write_financial_data() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    quarterly = pd.DataFrame(
        [
            {
                "quarter": "FY26 Q1",
                "period_end": "2025-08-31",
                "release_date": "2025-09-30",
                "total_revenue_m": 11720,
                "reported_revenue_change_pct": 1,
                "currency_neutral_revenue_change_pct": -1,
                "nike_brand_revenue_m": 11362,
                "nike_brand_reported_change_pct": 2,
                "nike_brand_cn_change_pct": 0,
                "wholesale_revenue_m": 6800,
                "wholesale_reported_change_pct": 7,
                "wholesale_cn_change_pct": 5,
                "direct_revenue_m": 4500,
                "direct_reported_change_pct": -4,
                "direct_cn_change_pct": -5,
                "converse_revenue_m": 366,
                "converse_reported_change_pct": -27,
                "converse_cn_change_pct": -28,
                "gross_margin_pct": 42.2,
                "gross_margin_change_bps": -320,
                "net_income_m": 727,
                "net_income_change_pct": -31,
                "diluted_eps": 0.49,
                "eps_change_pct": -30,
                "inventories_m": 8114,
                "inventory_change_pct": -2,
                "cash_and_short_investments_m": 8575,
            },
            {
                "quarter": "FY26 Q2",
                "period_end": "2025-11-30",
                "release_date": "2025-12-18",
                "total_revenue_m": 12427,
                "reported_revenue_change_pct": 1,
                "currency_neutral_revenue_change_pct": 0,
                "nike_brand_revenue_m": 12124,
                "nike_brand_reported_change_pct": 1,
                "nike_brand_cn_change_pct": 1,
                "wholesale_revenue_m": 7500,
                "wholesale_reported_change_pct": 8,
                "wholesale_cn_change_pct": 8,
                "direct_revenue_m": 4600,
                "direct_reported_change_pct": -8,
                "direct_cn_change_pct": -9,
                "converse_revenue_m": 300,
                "converse_reported_change_pct": -30,
                "converse_cn_change_pct": -31,
                "gross_margin_pct": 40.6,
                "gross_margin_change_bps": -300,
                "net_income_m": 792,
                "net_income_change_pct": -32,
                "diluted_eps": 0.53,
                "eps_change_pct": -32,
                "inventories_m": 7726,
                "inventory_change_pct": -3,
                "cash_and_short_investments_m": 8345,
            },
            {
                "quarter": "FY26 Q3",
                "period_end": "2026-02-28",
                "release_date": "2026-03-31",
                "total_revenue_m": 11279,
                "reported_revenue_change_pct": 0,
                "currency_neutral_revenue_change_pct": -3,
                "nike_brand_revenue_m": 11012,
                "nike_brand_reported_change_pct": 1,
                "nike_brand_cn_change_pct": -2,
                "wholesale_revenue_m": 6500,
                "wholesale_reported_change_pct": 5,
                "wholesale_cn_change_pct": 1,
                "direct_revenue_m": 4500,
                "direct_reported_change_pct": -4,
                "direct_cn_change_pct": -7,
                "converse_revenue_m": 264,
                "converse_reported_change_pct": -35,
                "converse_cn_change_pct": -37,
                "gross_margin_pct": 40.2,
                "gross_margin_change_bps": -130,
                "net_income_m": 520,
                "net_income_change_pct": -35,
                "diluted_eps": 0.35,
                "eps_change_pct": -35,
                "inventories_m": 7487,
                "inventory_change_pct": -1,
                "cash_and_short_investments_m": 8057,
            },
        ]
    )
    quarterly.to_csv(DATA_DIR / "nike_quarterly_metrics.csv", index=False)

    rows = []

    def add(quarter, region, product, revenue, prior, change, cn_change):
        rows.append(
            {
                "quarter": quarter,
                "region": region,
                "product": product,
                "revenue_m": revenue,
                "prior_year_revenue_m": prior,
                "reported_change_pct": change,
                "currency_neutral_change_pct": cn_change,
            }
        )

    # FY26 Q1 divisional revenues from NIKE official investor release.
    add("FY26 Q1", "North America", "Footwear", 3219, 3212, 0, 0)
    add("FY26 Q1", "North America", "Apparel", 1474, 1331, 11, 11)
    add("FY26 Q1", "North America", "Equipment", 327, 283, 16, 16)
    add("FY26 Q1", "North America", "Total", 5020, 4826, 4, 4)
    add("FY26 Q1", "Europe, Middle East & Africa", "Footwear", 2021, 1952, 4, -2)
    add("FY26 Q1", "Europe, Middle East & Africa", "Apparel", 1106, 993, 11, 6)
    add("FY26 Q1", "Europe, Middle East & Africa", "Equipment", 204, 198, 3, -2)
    add("FY26 Q1", "Europe, Middle East & Africa", "Total", 3331, 3143, 6, 1)
    add("FY26 Q1", "Greater China", "Footwear", 1109, 1246, -11, -12)
    add("FY26 Q1", "Greater China", "Apparel", 362, 360, 1, 0)
    add("FY26 Q1", "Greater China", "Equipment", 41, 60, -32, -33)
    add("FY26 Q1", "Greater China", "Total", 1512, 1666, -9, -10)
    add("FY26 Q1", "Asia Pacific & Latin America", "Footwear", 1061, 1052, 1, 0)
    add("FY26 Q1", "Asia Pacific & Latin America", "Apparel", 371, 348, 7, 5)
    add("FY26 Q1", "Asia Pacific & Latin America", "Equipment", 58, 62, -6, -7)
    add("FY26 Q1", "Asia Pacific & Latin America", "Total", 1490, 1462, 2, 1)

    # FY26 Q2 divisional revenues.
    add("FY26 Q2", "North America", "Footwear", 3542, 3236, 9, 9)
    add("FY26 Q2", "North America", "Apparel", 1811, 1693, 7, 7)
    add("FY26 Q2", "North America", "Equipment", 280, 250, 12, 12)
    add("FY26 Q2", "North America", "Total", 5633, 5179, 9, 9)
    add("FY26 Q2", "Europe, Middle East & Africa", "Footwear", 2012, 1982, 2, -2)
    add("FY26 Q2", "Europe, Middle East & Africa", "Apparel", 1196, 1136, 5, 1)
    add("FY26 Q2", "Europe, Middle East & Africa", "Equipment", 184, 185, -1, -5)
    add("FY26 Q2", "Europe, Middle East & Africa", "Total", 3392, 3303, 3, -1)
    add("FY26 Q2", "Greater China", "Footwear", 954, 1203, -21, -20)
    add("FY26 Q2", "Greater China", "Apparel", 442, 472, -6, -6)
    add("FY26 Q2", "Greater China", "Equipment", 27, 36, -25, -24)
    add("FY26 Q2", "Greater China", "Total", 1423, 1711, -17, -16)
    add("FY26 Q2", "Asia Pacific & Latin America", "Footwear", 1151, 1234, -7, -7)
    add("FY26 Q2", "Asia Pacific & Latin America", "Apparel", 457, 437, 5, 6)
    add("FY26 Q2", "Asia Pacific & Latin America", "Equipment", 59, 73, -19, -18)
    add("FY26 Q2", "Asia Pacific & Latin America", "Total", 1667, 1744, -4, -4)

    # FY26 Q3 divisional revenues.
    add("FY26 Q3", "North America", "Footwear", 3326, 3132, 6, 6)
    add("FY26 Q3", "North America", "Apparel", 1480, 1510, -2, -2)
    add("FY26 Q3", "North America", "Equipment", 220, 222, -1, -1)
    add("FY26 Q3", "North America", "Total", 5026, 4864, 3, 3)
    add("FY26 Q3", "Europe, Middle East & Africa", "Footwear", 1789, 1742, 3, -7)
    add("FY26 Q3", "Europe, Middle East & Africa", "Apparel", 926, 913, 1, -8)
    add("FY26 Q3", "Europe, Middle East & Africa", "Equipment", 159, 156, 2, -8)
    add("FY26 Q3", "Europe, Middle East & Africa", "Total", 2874, 2811, 2, -7)
    add("FY26 Q3", "Greater China", "Footwear", 1187, 1282, -7, -10)
    add("FY26 Q3", "Greater China", "Apparel", 397, 412, -4, -7)
    add("FY26 Q3", "Greater China", "Equipment", 31, 39, -21, -22)
    add("FY26 Q3", "Greater China", "Total", 1615, 1733, -7, -10)
    add("FY26 Q3", "Asia Pacific & Latin America", "Footwear", 1051, 1052, 0, -3)
    add("FY26 Q3", "Asia Pacific & Latin America", "Apparel", 381, 358, 6, 4)
    add("FY26 Q3", "Asia Pacific & Latin America", "Equipment", 58, 60, -3, -7)
    add("FY26 Q3", "Asia Pacific & Latin America", "Total", 1490, 1470, 1, -2)

    pd.DataFrame(rows).to_csv(DATA_DIR / "nike_divisional_revenue.csv", index=False)

    social = pd.DataFrame(
        [
            {
                "platform": "Instagram",
                "handle": "@nike",
                "date": "2026-05-25",
                "audience_m": 292.018934,
                "scale_metric_m": 292.018934,
                "scale_metric_label": "followers",
                "content_count": 1630,
                "source": "AltIndex Instagram followers; PostWithProof post count",
                "source_url": "https://altindex.com/ticker/nke/instagram-followers",
            },
            {
                "platform": "TikTok",
                "handle": "@nike",
                "date": "2026-05-25",
                "audience_m": 8.5,
                "scale_metric_m": 43.5,
                "scale_metric_label": "likes",
                "content_count": 1075,
                "source": "Social Blade TikTok public profile snapshot",
                "source_url": "https://socialblade.com/tiktok/user/nike",
            },
            {
                "platform": "YouTube",
                "handle": "Nike",
                "date": "2026-03-25",
                "audience_m": 2.22,
                "scale_metric_m": 392.3,
                "scale_metric_label": "lifetime views",
                "content_count": 627,
                "source": "HunterTuber YouTube analytics snapshot",
                "source_url": "https://huntertuber.com/UCUFgkRb0ZHc4Rpq15VRCICA",
            },
        ]
    )
    social.to_csv(DATA_DIR / "nike_social_snapshot.csv", index=False)

    instagram_monthly = pd.DataFrame(
        [
            {"month": "2026-01-01", "followers": 298284695},
            {"month": "2026-02-01", "followers": 297972307},
            {"month": "2026-03-01", "followers": 297709037},
            {"month": "2026-04-01", "followers": 297365073},
            {"month": "2026-05-25", "followers": 292018934},
        ]
    )
    instagram_monthly.to_csv(DATA_DIR / "nike_instagram_followers.csv", index=False)


def fetch_yahoo_stock() -> None:
    url = "https://query1.finance.yahoo.com/v8/finance/chart/NKE"
    start = int(datetime(2025, 8, 1, tzinfo=timezone.utc).timestamp())
    end = int(datetime(2026, 5, 26, tzinfo=timezone.utc).timestamp())
    params = {"period1": start, "period2": end, "interval": "1d", "events": "history"}
    response = requests.get(url, params=params, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()
    result = response.json()["chart"]["result"][0]
    timestamps = result["timestamp"]
    quote = result["indicators"]["quote"][0]
    adjclose = result["indicators"].get("adjclose", [{}])[0].get("adjclose", quote["close"])
    stock = pd.DataFrame(
        {
            "date": pd.to_datetime(timestamps, unit="s").date,
            "open": quote["open"],
            "high": quote["high"],
            "low": quote["low"],
            "close": quote["close"],
            "adj_close": adjclose,
            "volume": quote["volume"],
        }
    )
    stock["daily_return_pct"] = stock["adj_close"].pct_change() * 100
    stock.to_csv(DATA_DIR / "nke_stock_prices.csv", index=False)


def fetch_gdelt_series(mode: str) -> dict:
    url = "https://api.gdeltproject.org/api/v2/doc/doc"
    params = {
        "query": "Nike sourcelang:english",
        "mode": mode,
        "format": "json",
        "startdatetime": "20250901000000",
        "enddatetime": "20260525000000",
    }
    response = requests.get(url, params=params, timeout=45)
    response.raise_for_status()
    return response.json()


def fetch_gdelt_news() -> None:
    volume = fetch_gdelt_series("timelinevolraw")
    time.sleep(6)
    tone = fetch_gdelt_series("timelinetone")

    def timeline_to_frame(payload: dict, value_col: str) -> pd.DataFrame:
        data = payload["timeline"][0]["data"]
        frame = pd.DataFrame(data)
        frame["date"] = pd.to_datetime(frame["date"]).dt.date
        return frame[["date", "value"]].rename(columns={"value": value_col})

    volume_df = timeline_to_frame(volume, "article_count")
    tone_df = timeline_to_frame(tone, "average_tone")
    merged = volume_df.merge(tone_df, on="date", how="outer").sort_values("date")
    merged["article_count_7d_avg"] = merged["article_count"].rolling(7, min_periods=1).mean()
    merged["average_tone_7d_avg"] = merged["average_tone"].rolling(7, min_periods=1).mean()
    merged.to_csv(DATA_DIR / "gdelt_nike_news_sentiment.csv", index=False)

    raw_dir = DATA_DIR / "raw"
    raw_dir.mkdir(exist_ok=True)
    (raw_dir / "gdelt_timelinevolraw_response.json").write_text(json.dumps(volume, indent=2))
    (raw_dir / "gdelt_timelinetone_response.json").write_text(json.dumps(tone, indent=2))


def main() -> None:
    write_financial_data()
    fetch_yahoo_stock()
    fetch_gdelt_news()
    print(f"Data refreshed in {DATA_DIR}")


if __name__ == "__main__":
    main()
