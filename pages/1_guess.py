import plotly.graph_objects as go
import streamlit as st

import config
from utils import calc, ui

ui.header(
    "Guess the value of nature",
    "Your guess vs. the real estimate of what nature gives us every year.",
)

services = ui.services()
biomes = ui.biomes()
f = ui.factor()

st.session_state.setdefault("guess_revealed", False)

guess = st.slider(
    f"Your guess: how much does nature give us every year? (trillion {ui.currency_label()})",
    min_value=0,
    max_value=100,
    value=5,
    step=1,
)
if st.button("Reveal", type="primary"):
    st.session_state.guess_revealed = True

if st.session_state.guess_revealed:
    avg = config.TOTAL_AVG_TN * f
    low = config.TOTAL_LOW_TN * f
    high = config.TOTAL_HIGH_TN * f
    gnp = config.WORLD_GNP_1997_TN * f

    fig = go.Figure(
        go.Bar(
            x=["Your guess", "Nature", "World GNP 1997"],
            y=[guess, avg, gnp],
            marker_color=[ui.BLUE, ui.AQUA, ui.GREY],
            text=[f"{guess:.0f}", f"{avg:.1f}", f"{gnp:.0f}"],
            textposition="inside",
            insidetextanchor="start",
            hovertemplate="%{x}: %{y:.1f} trillion<extra></extra>",
        )
    )
    # Range of the estimate, drawn only on the Nature bar
    fig.add_trace(
        go.Scatter(
            x=["Nature"],
            y=[avg],
            mode="markers",
            marker=dict(size=1, opacity=0),
            error_y=dict(
                type="data",
                symmetric=False,
                array=[high - avg],
                arrayminus=[avg - low],
                thickness=3,
                width=14,
                color=ui.GREY,
            ),
            hovertemplate=f"Range: {low:.0f}–{high:.0f} trillion<extra></extra>",
        )
    )
    fig.update_layout(
        yaxis_title=f"trillion {ui.currency_label()} / year",
        showlegend=False,
        height=400,
        title=f"Nature: {low:.0f}–{high:.0f} trillion per year (bar = average)",
    )
    ui.chart(fig)

    ratio = calc.nature_vs_gnp(config.TOTAL_AVG_TN, config.WORLD_GNP_1997_TN)
    person = calc.per_person(config.TOTAL_AVG_TN, config.WORLD_POP_1997)
    c1, c2 = st.columns(2)
    c1.metric("Nature vs. the whole world economy", f"≈ {ratio:.1f} ×")
    c2.metric(
        "Your yearly bill from nature, per person",
        f"≈ {ui.money(person)}",
        help=f"Total value / world population in 1997 ({config.WORLD_POP_1997 / 1e9:.2f} bn)",
    )
    c2.caption(ui.esc(f"≈ {ui.money(person / 365)} per day"))

    share = calc.market_share(services)
    df = services.sort_values("global_value_bn", ascending=True).copy()
    df["value"] = df["global_value_bn"] * f
    fig2 = go.Figure()
    for group, color in [("Outside markets", ui.AQUA), (calc.MARKET_GROUP, ui.ORANGE)]:
        part = df[df["simple_group"] == group]
        fig2.add_trace(
            go.Bar(
                x=part["value"],
                y=part["service"],
                orientation="h",
                name=group,
                marker_color=color,
                hovertemplate="%{y}: %{x:,.0f} bn<extra></extra>",
            )
        )
    fig2.update_layout(
        title=f"The {len(services)} services, billion {ui.currency_label()} / year",
        yaxis=dict(categoryorder="array", categoryarray=df["service"].tolist()),
        legend=dict(title="Our simple grouping", orientation="h", y=-0.12),
        height=560,
        barmode="overlay",
    )
    ui.chart(fig2)
    st.markdown(f"Only **~{share * 100:.0f}%** of this value is goods we buy and sell.")

ui.takeaway(
    "Nature's services are worth more than the entire world economy — "
    "yet almost none of this value shows up in prices."
)

top = services.loc[services["global_value_bn"].idxmax()]
ui.speaker_notes(
    [
        f"Costanza et al. combined 100+ studies: {len(services)} services × {len(biomes)} biomes.",
        f"Range ${config.TOTAL_LOW_TN}–{config.TOTAL_HIGH_TN} trillion/yr, average "
        f"${config.TOTAL_AVG_TN:.0f}T, vs. world GNP ≈ ${config.WORLD_GNP_1997_TN}T.",
        f"The biggest item, {top['service'].lower()} (~${top['global_value_bn'] / 1000:.0f}T), "
        "has no market at all.",
        "The authors call it a *minimum* estimate.",
    ]
)
ui.source_footer(f"{ui.COSTANZA}, Table 2. Grouping into market / non-market is ours.")
