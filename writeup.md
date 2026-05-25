# Nike Global Brand Recovery Dashboard

GitHub Repository: https://github.com/nevesliu7/nike-recovery-dashboard. Render URL: https://nike-recovery-dashboard.onrender.com.

## Data Source and Project Motivation

This dashboard studies Nike's FY2026 recovery using public data. The core financial data comes from Nike's official investor releases for FY2026 Q1, Q2, and Q3. These releases include revenue, gross margin, net income, channel performance, regional revenue, and product revenue. To connect business results with public perception, the dashboard also uses GDELT Project news volume and average tone for English-language Nike coverage, Yahoo Finance daily NKE prices, and public social platform snapshots from AltIndex, Social Blade, and HunterTuber.

We chose Path C, an API-backed data product, because it demonstrates a stronger publication architecture than a repository-only project. The cleaned sample data remains in the GitHub repository for reproducibility, while the app is designed to request the same tables from Tinybird SQL Pipe endpoints when deployed. Render runs the Dash app and GitHub documents the code, data sample, requirements, writeup, and architecture.

## Visualization Choices

The line chart shows Nike's quarterly path and lets users switch between revenue, NIKE Brand revenue, gross margin, net income, and EPS. The grouped bar chart compares Wholesale, NIKE Direct, and Converse, which is important because the recovery is tied to channel mix rather than total revenue alone.

The animated bubble chart compares regions across Q1-Q3. Revenue is shown on the x-axis, year-over-year change on the y-axis, and bubble size reinforces scale. Hover details show exact revenue, prior-year revenue, reported growth, and currency-neutral growth.

The sunburst chart shows the revenue hierarchy by region and product category. The public attention chart adds GDELT news tone, news volume, and stock price to show whether market and media reaction changed around the earnings period. The social bubble chart gives a public view of Nike's digital reach across Instagram, TikTok, and YouTube.

## Key Findings

Nike's recovery is uneven. Total revenue is relatively stable, but profitability is under pressure. Gross margin falls from 42.2% in Q1 to 40.2% in Q3, and net income declines year over year in every quarter.

Wholesale is the strongest channel signal. It grows in all three quarters, while NIKE Direct declines. This suggests Nike's recovery is partly supported by renewed wholesale momentum rather than direct-to-consumer strength.

Greater China remains a major pressure point. It posts negative reported and currency-neutral growth in all three quarters. North America is much stronger and is the clearest regional driver of stabilization.

Converse is a persistent drag. Its revenue declines sharply across Q1-Q3, with the Q3 decline reaching 35% reported year over year. Public attention is not the same as positive sentiment; GDELT volume shows attention, while tone and stock price help interpret confidence or concern.

## Assumptions, Bias, and Limitations

This project uses public data only. Nike's official releases are reliable for financial figures, but some channel values are rounded in the release text. Social platform data comes from third-party public snapshots, so those numbers should be treated as directional rather than exact internal engagement data.

GDELT news tone is a proxy for public opinion, not a survey of customers. It reflects English-language online news coverage and may overrepresent media narratives, investor concerns, or high-visibility markets. It does not fully capture private customer behavior, non-English coverage, or platform-specific comments.

The Path C architecture separates the data layer from the dashboard, but it also introduces token management and API availability risks. For grading and reproducibility, the app can fall back to local CSV files if the Tinybird token is unavailable.

## Outlook

With more resources, the project could connect Nike's public financial results to product-level sales, regional store traffic, advertising spend, athlete sponsorship data, customer reviews, and full social listening data across TikTok, Instagram, Reddit, X, and YouTube comments.

A stronger version could compare Nike directly with Adidas, Puma, On, Hoka, Lululemon, and Under Armour. The API layer could then serve competitor tables, live public attention feeds, and predictive models estimating which regions and channels are most likely to recover first.

## Collaboration Statement

We used ChatGPT/Codex to help brainstorm the dashboard structure, build and debug the Dash app, organize public data sources, add the Path C Tinybird/Render architecture, draft the README, and generate the PDF writeup. The final project decisions, interpretation of findings, design choices, and submitted work remain the responsibility of the group.

Neves proposed the original Nike FY2026 recovery idea and helped define the dashboard direction and research questions. Mike supported dashboard structure, visualization planning, API-backed publication planning, and interpretation. Both group members should review the final project before submission and update this statement if the actual division of work changes.
