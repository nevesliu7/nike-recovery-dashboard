SELECT
    date,
    open,
    high,
    low,
    close,
    adj_close,
    volume,
    daily_return_pct
FROM nke_stock_prices
ORDER BY date
