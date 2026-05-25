SELECT
    quarter,
    region,
    product,
    revenue_m,
    prior_year_revenue_m,
    reported_change_pct,
    currency_neutral_change_pct
FROM nike_divisional_revenue
ORDER BY quarter, region, product
