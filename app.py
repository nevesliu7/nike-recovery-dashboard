from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html
from plotly.subplots import make_subplots

from services.data_client import load_dashboard_data


ROOT = Path(__file__).resolve().parent

QUARTER_ORDER = {"FY26 Q1": 1, "FY26 Q2": 2, "FY26 Q3": 3}
REGION_COLORS = {
    "North America": "#C8FF00",
    "Europe, Middle East & Africa": "#FFFFFF",
    "Greater China": "#FF5A1F",
    "Asia Pacific & Latin America": "#00D4FF",
}
CHANNEL_COLORS = {
    "Wholesale": "#C8FF00",
    "NIKE Direct": "#FFFFFF",
    "Converse": "#FF5A1F",
}
TEMPLATE_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#F4F4F0", family="Inter, Arial, sans-serif"),
    margin=dict(l=46, r=28, t=58, b=52),
    hoverlabel=dict(bgcolor="#111111", bordercolor="#C8FF00", font_size=13),
)


DATA, DATA_SOURCE_LABEL = load_dashboard_data()
QUARTERS = DATA["quarterly"]["quarter"].tolist()
REGIONS = DATA["divisional"]["region"].drop_duplicates().tolist()
PRODUCTS = ["Footwear", "Apparel", "Equipment"]
CHANNELS = ["Wholesale", "NIKE Direct", "Converse"]

METRIC_OPTIONS = {
    "total_revenue_m": "Total revenue ($M)",
    "nike_brand_revenue_m": "NIKE Brand revenue ($M)",
    "gross_margin_pct": "Gross margin (%)",
    "net_income_m": "Net income ($M)",
    "diluted_eps": "Diluted EPS ($)",
}


def apply_figure_style(fig: go.Figure, title: str) -> go.Figure:
    fig.update_layout(**TEMPLATE_LAYOUT)
    fig.update_layout(title=dict(text=title, x=0.02, xanchor="left", font=dict(size=19)))
    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        linecolor="rgba(244,244,240,0.18)",
        tickfont=dict(color="#CBCBC4"),
        title_font=dict(color="#CBCBC4"),
    )
    fig.update_yaxes(
        gridcolor="rgba(244,244,240,0.10)",
        zeroline=False,
        linecolor="rgba(244,244,240,0.18)",
        tickfont=dict(color="#CBCBC4"),
        title_font=dict(color="#CBCBC4"),
    )
    return fig


def kpi_card(label: str, value: str, delta: str | None = None, tone: str = "neutral") -> html.Div:
    children = [html.Div(label, className="kpi-label"), html.Div(value, className="kpi-value")]
    if delta is not None:
        children.append(html.Div(delta, className=f"kpi-delta {tone}"))
    return html.Div(children, className="kpi-card")


app = Dash(__name__)
app.title = "Nike Brand Recovery Dashboard"
server = app.server

app.layout = html.Div(
    className="app-shell",
    children=[
        html.Section(
            className="hero",
            children=[
                html.Div(
                    className="hero-copy",
                    children=[
                        html.Div("FY2026 PUBLIC DATA DASHBOARD", className="eyebrow"),
                        html.H1("Nike Global Brand Recovery Tracker"),
                        html.P(
                            "A Dash and Plotly dashboard connecting Nike's quarterly recovery, regional pressure points, "
                            "channel mix, public news tone, market reaction, and social reach."
                        ),
                    ],
                ),
                html.Div(
                    className="hero-badge",
                    children=[
                        html.Div("WIN NOW", className="badge-main"),
                        html.Div("Q1-Q3 FY26", className="badge-sub"),
                    ],
                ),
            ],
        ),
        html.Section(
            className="controls",
            children=[
                html.Div(
                    className="control-block",
                    children=[
                        html.Label("Quarters"),
                        dcc.Checklist(
                            id="quarter-filter",
                            options=[{"label": q, "value": q} for q in QUARTERS],
                            value=QUARTERS,
                            inline=True,
                            className="pill-checklist",
                        ),
                    ],
                ),
                html.Div(
                    className="control-block",
                    children=[
                        html.Label("Regions"),
                        dcc.Dropdown(
                            id="region-filter",
                            options=[{"label": r, "value": r} for r in REGIONS],
                            value=REGIONS,
                            multi=True,
                            clearable=False,
                            className="dark-dropdown",
                        ),
                    ],
                ),
                html.Div(
                    className="control-block",
                    children=[
                        html.Label("Products"),
                        dcc.Dropdown(
                            id="product-filter",
                            options=[{"label": p, "value": p} for p in PRODUCTS],
                            value=PRODUCTS,
                            multi=True,
                            clearable=False,
                            className="dark-dropdown",
                        ),
                    ],
                ),
                html.Div(
                    className="control-block",
                    children=[
                        html.Label("Main metric"),
                        dcc.Dropdown(
                            id="metric-filter",
                            options=[{"label": label, "value": col} for col, label in METRIC_OPTIONS.items()],
                            value="total_revenue_m",
                            clearable=False,
                            className="dark-dropdown",
                        ),
                    ],
                ),
            ],
        ),
        html.Div(id="kpi-row", className="kpi-row"),
        html.Section(
            className="chart-grid",
            children=[
                html.Div(dcc.Graph(id="financial-line", config={"displayModeBar": False}), className="chart-card wide"),
                html.Div(
                    className="chart-card",
                    children=[
                        html.Div(
                            className="mini-control",
                            children=[
                                html.Label("Channel toggle"),
                                dcc.Checklist(
                                    id="channel-filter",
                                    options=[{"label": c, "value": c} for c in CHANNELS],
                                    value=CHANNELS,
                                    inline=True,
                                    className="pill-checklist compact",
                                ),
                            ],
                        ),
                        dcc.Graph(id="channel-bar", config={"displayModeBar": False}),
                    ],
                ),
                html.Div(dcc.Graph(id="regional-bubble", config={"displayModeBar": False}), className="chart-card"),
                html.Div(
                    className="chart-card",
                    children=[
                        html.Div(
                            className="mini-control",
                            children=[
                                html.Label("Sunburst quarter"),
                                dcc.Dropdown(
                                    id="sunburst-quarter",
                                    options=[{"label": q, "value": q} for q in QUARTERS],
                                    value="FY26 Q3",
                                    clearable=False,
                                    className="dark-dropdown small",
                                ),
                            ],
                        ),
                        dcc.Graph(id="sunburst", config={"displayModeBar": False}),
                    ],
                ),
                html.Div(
                    className="chart-card wide",
                    children=[
                        html.Div(
                            className="mini-control",
                            children=[
                                html.Label("Public attention layers"),
                                dcc.Checklist(
                                    id="sentiment-layer-filter",
                                    options=[
                                        {"label": "News volume", "value": "volume"},
                                        {"label": "News tone", "value": "tone"},
                                        {"label": "NKE close", "value": "stock"},
                                    ],
                                    value=["volume", "tone", "stock"],
                                    inline=True,
                                    className="pill-checklist compact",
                                ),
                            ],
                        ),
                        dcc.Graph(id="sentiment-stock", config={"displayModeBar": False}),
                    ],
                ),
                html.Div(dcc.Graph(id="social-bubble", config={"displayModeBar": False}), className="chart-card"),
                html.Div(dcc.Graph(id="instagram-line", config={"displayModeBar": False}), className="chart-card"),
            ],
        ),
        html.Footer(
            children=[
                html.Strong(f"Data layer: {DATA_SOURCE_LABEL}. "),
                "Sources: NIKE investor releases, GDELT Project DOC API, Yahoo Finance chart API, AltIndex, Social Blade, HunterTuber. "
                "Social and news metrics are public proxies, not direct internal Nike engagement data."
            ]
        ),
    ],
)


@app.callback(
    Output("kpi-row", "children"),
    Output("financial-line", "figure"),
    Output("channel-bar", "figure"),
    Output("regional-bubble", "figure"),
    Output("sunburst", "figure"),
    Output("sentiment-stock", "figure"),
    Output("social-bubble", "figure"),
    Output("instagram-line", "figure"),
    Input("quarter-filter", "value"),
    Input("region-filter", "value"),
    Input("product-filter", "value"),
    Input("metric-filter", "value"),
    Input("channel-filter", "value"),
    Input("sunburst-quarter", "value"),
    Input("sentiment-layer-filter", "value"),
)
def update_dashboard(
    selected_quarters,
    selected_regions,
    selected_products,
    metric,
    selected_channels,
    sunburst_quarter,
    sentiment_layers,
):
    selected_quarters = selected_quarters or QUARTERS
    selected_regions = selected_regions or REGIONS
    selected_products = selected_products or PRODUCTS
    selected_channels = selected_channels or CHANNELS
    sentiment_layers = sentiment_layers or ["volume"]

    quarterly = DATA["quarterly"][DATA["quarterly"]["quarter"].isin(selected_quarters)].sort_values("quarter_order")
    latest = quarterly.iloc[-1]

    kpis = [
        kpi_card(
            f"{latest['quarter']} revenue",
            f"${latest['total_revenue_m'] / 1000:.1f}B",
            f"{latest['reported_revenue_change_pct']:+.0f}% reported YoY",
            "positive" if latest["reported_revenue_change_pct"] >= 0 else "negative",
        ),
        kpi_card(
            "Gross margin",
            f"{latest['gross_margin_pct']:.1f}%",
            f"{latest['gross_margin_change_bps']:+.0f} bps YoY",
            "positive" if latest["gross_margin_change_bps"] >= 0 else "negative",
        ),
        kpi_card(
            "Net income",
            f"${latest['net_income_m']:.0f}M",
            f"{latest['net_income_change_pct']:+.0f}% YoY",
            "positive" if latest["net_income_change_pct"] >= 0 else "negative",
        ),
        kpi_card(
            "Inventory",
            f"${latest['inventories_m'] / 1000:.1f}B",
            f"{latest['inventory_change_pct']:+.0f}% YoY",
            "positive" if latest["inventory_change_pct"] <= 0 else "negative",
        ),
    ]

    metric_label = METRIC_OPTIONS[metric]
    line_df = quarterly.copy()
    if metric.endswith("_m"):
        line_df["metric_value"] = line_df[metric] / 1000
        metric_label_display = metric_label.replace("($M)", "($B)")
        hover_value = "$%{y:,.2f}B"
    elif metric == "diluted_eps":
        line_df["metric_value"] = line_df[metric]
        metric_label_display = metric_label
        hover_value = "$%{y:,.2f}"
    elif metric.endswith("_pct"):
        line_df["metric_value"] = line_df[metric]
        metric_label_display = metric_label
        hover_value = "%{y:,.1f}%"
    else:
        line_df["metric_value"] = line_df[metric]
        metric_label_display = metric_label
        hover_value = "%{y:,.2f}"
    line_fig = px.line(
        line_df,
        x="quarter",
        y="metric_value",
        markers=True,
        custom_data=["period_end", "reported_revenue_change_pct", "currency_neutral_revenue_change_pct"],
        color_discrete_sequence=["#C8FF00"],
    )
    line_fig.update_traces(
        line=dict(width=4),
        marker=dict(size=10, line=dict(color="#111111", width=2)),
        hovertemplate=(
            "<b>%{x}</b><br>"
            + metric_label_display
            + f": {hover_value}<br>"
            + "Period end: %{customdata[0]|%b %d, %Y}<br>"
            + "Reported revenue YoY: %{customdata[1]:+.0f}%<br>"
            + "Currency-neutral revenue YoY: %{customdata[2]:+.0f}%<extra></extra>"
        ),
    )
    line_fig = apply_figure_style(line_fig, "Core financial trajectory")
    line_fig.update_yaxes(title=metric_label_display)

    channel_map = {
        "Wholesale": "wholesale_revenue_m",
        "NIKE Direct": "direct_revenue_m",
        "Converse": "converse_revenue_m",
    }
    channel_rows = []
    for channel in selected_channels:
        col = channel_map[channel]
        change_col = col.replace("_revenue_m", "_reported_change_pct")
        for _, row in quarterly.iterrows():
            channel_rows.append(
                {
                    "quarter": row["quarter"],
                    "channel": channel,
                    "revenue_m": row[col],
                    "reported_change_pct": row[change_col],
                }
            )
    channel_df = pd.DataFrame(channel_rows)
    bar_fig = px.bar(
        channel_df,
        x="quarter",
        y="revenue_m",
        color="channel",
        barmode="group",
        color_discrete_map=CHANNEL_COLORS,
        custom_data=["reported_change_pct"],
    )
    bar_fig.update_traces(
        hovertemplate="<b>%{x}</b><br>%{fullData.name}: $%{y:,.0f}M<br>Reported YoY: %{customdata[0]:+.0f}%<extra></extra>"
    )
    bar_fig = apply_figure_style(bar_fig, "Channel mix: wholesale recovery vs direct pressure")
    bar_fig.update_yaxes(title="Revenue ($M)")
    bar_fig.update_layout(legend_title_text="")

    div = DATA["divisional"]
    region_totals = div[
        (div["product"] == "Total")
        & (div["quarter"].isin(selected_quarters))
        & (div["region"].isin(selected_regions))
    ].copy()
    region_totals["revenue_b"] = region_totals["revenue_m"] / 1000
    bubble_fig = px.scatter(
        region_totals,
        x="revenue_b",
        y="reported_change_pct",
        size="revenue_m",
        color="region",
        animation_frame="quarter",
        color_discrete_map=REGION_COLORS,
        size_max=54,
        custom_data=["region", "revenue_m", "prior_year_revenue_m", "currency_neutral_change_pct"],
    )
    bubble_fig.update_traces(
        marker=dict(line=dict(color="#111111", width=1.5), opacity=0.88),
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            + "Revenue: $%{customdata[1]:,.0f}M<br>"
            + "Prior year: $%{customdata[2]:,.0f}M<br>"
            + "Reported YoY: %{y:+.0f}%<br>"
            + "Currency-neutral YoY: %{customdata[3]:+.0f}%<extra></extra>"
        ),
    )
    bubble_fig.add_hline(y=0, line_width=1, line_color="rgba(244,244,240,0.35)")
    bubble_fig = apply_figure_style(bubble_fig, "Animated regional bubble chart")
    bubble_fig.update_xaxes(title="Quarterly revenue ($B)")
    bubble_fig.update_yaxes(title="Reported YoY change (%)")
    bubble_fig.update_layout(legend_title_text="", transition={"duration": 500})

    sunburst_df = div[
        (div["quarter"] == sunburst_quarter)
        & (div["region"].isin(selected_regions))
        & (div["product"].isin(selected_products))
    ].copy()
    sunburst_fig = px.sunburst(
        sunburst_df,
        path=["region", "product"],
        values="revenue_m",
        color="reported_change_pct",
        color_continuous_scale=["#FF5A1F", "#2E2E2E", "#C8FF00"],
        color_continuous_midpoint=0,
        custom_data=["reported_change_pct", "currency_neutral_change_pct"],
    )
    sunburst_fig.update_traces(
        insidetextorientation="radial",
        hovertemplate="<b>%{label}</b><br>Revenue: $%{value:,.0f}M<br>Reported YoY: %{customdata[0]:+.0f}%<br>Currency-neutral YoY: %{customdata[1]:+.0f}%<extra></extra>",
    )
    sunburst_fig = apply_figure_style(sunburst_fig, f"{sunburst_quarter} revenue hierarchy")
    sunburst_fig.update_layout(coloraxis_colorbar=dict(title="YoY %"))

    sentiment = DATA["sentiment"]
    stock = DATA["stock"]
    sentiment_fig = make_subplots(specs=[[{"secondary_y": True}]])
    if "volume" in sentiment_layers:
        sentiment_fig.add_trace(
            go.Scatter(
                x=sentiment["date"],
                y=sentiment["article_count_7d_avg"],
                name="News volume 7d avg",
                mode="lines",
                line=dict(color="#C8FF00", width=3),
                hovertemplate="%{x|%b %d, %Y}<br>Articles 7d avg: %{y:.1f}<extra></extra>",
            ),
            secondary_y=False,
        )
    if "tone" in sentiment_layers:
        sentiment_fig.add_trace(
            go.Scatter(
                x=sentiment["date"],
                y=sentiment["average_tone_7d_avg"],
                name="Average tone 7d avg",
                mode="lines",
                line=dict(color="#00D4FF", width=2),
                hovertemplate="%{x|%b %d, %Y}<br>Average tone: %{y:.2f}<extra></extra>",
            ),
            secondary_y=True,
        )
    if "stock" in sentiment_layers:
        sentiment_fig.add_trace(
            go.Scatter(
                x=stock["date"],
                y=stock["close"],
                name="NKE close",
                mode="lines",
                line=dict(color="#FF5A1F", width=2),
                hovertemplate="%{x|%b %d, %Y}<br>NKE close: $%{y:.2f}<extra></extra>",
            ),
            secondary_y=True,
        )
    for q in DATA["quarterly"].itertuples():
        sentiment_fig.add_vline(
            x=q.release_date,
            line_width=1,
            line_dash="dot",
            line_color="rgba(244,244,240,0.35)",
        )
    sentiment_fig = apply_figure_style(sentiment_fig, "Public attention and market reaction")
    sentiment_fig.update_yaxes(title="News article count", secondary_y=False)
    sentiment_fig.update_yaxes(title="Tone / stock close", secondary_y=True, gridcolor="rgba(0,0,0,0)")
    sentiment_fig.update_layout(legend_title_text="")

    social = DATA["social"].copy()
    social_fig = px.scatter(
        social,
        x="audience_m",
        y="scale_metric_m",
        size="content_count",
        color="platform",
        text="platform",
        log_x=True,
        log_y=True,
        size_max=58,
        color_discrete_sequence=["#C8FF00", "#FF5A1F", "#00D4FF"],
        custom_data=["handle", "scale_metric_label", "content_count", "source"],
    )
    social_fig.update_traces(
        textposition="top center",
        marker=dict(line=dict(color="#111111", width=1.5), opacity=0.88),
        hovertemplate=(
            "<b>%{text}</b> %{customdata[0]}<br>"
            + "Audience: %{x:.2f}M<br>"
            + "Scale metric: %{y:.2f}M %{customdata[1]}<br>"
            + "Content count: %{customdata[2]:,.0f}<br>"
            + "%{customdata[3]}<extra></extra>"
        ),
    )
    social_fig = apply_figure_style(social_fig, "Social platform scale snapshot")
    social_fig.update_xaxes(title="Audience (millions, log)")
    social_fig.update_yaxes(title="Public scale metric (millions, log)")
    social_fig.update_layout(showlegend=False)

    insta = DATA["instagram"].copy()
    insta["followers_m"] = insta["followers"] / 1_000_000
    instagram_fig = px.line(
        insta,
        x="month",
        y="followers_m",
        markers=True,
        color_discrete_sequence=["#C8FF00"],
    )
    instagram_fig.update_traces(
        line=dict(width=3),
        marker=dict(size=9, line=dict(color="#111111", width=2)),
        hovertemplate="%{x|%b %d, %Y}<br>Instagram followers: %{y:.1f}M<extra></extra>",
    )
    instagram_fig = apply_figure_style(instagram_fig, "Instagram audience trend")
    instagram_fig.update_yaxes(title="Followers (millions)")
    instagram_fig.update_xaxes(title="")

    return kpis, line_fig, bar_fig, bubble_fig, sunburst_fig, sentiment_fig, social_fig, instagram_fig


if __name__ == "__main__":
    app.run(debug=False)
