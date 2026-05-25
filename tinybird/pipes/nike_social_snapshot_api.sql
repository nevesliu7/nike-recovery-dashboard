SELECT
    platform,
    handle,
    date,
    audience_m,
    scale_metric_m,
    scale_metric_label,
    content_count,
    source,
    source_url
FROM nike_social_snapshot
ORDER BY platform
