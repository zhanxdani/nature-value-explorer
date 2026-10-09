import plotly.graph_objects as go
import streamlit as st

import config
from utils import calc, ui

ui.header(
    "The land converter",
    "How much nature's services we lose when we turn wild land into farms or cities.",
)

biomes = ui.biomes()
f = ui.factor()

TARGETS = ["Cropland", "Urban", "Grass/rangelands"]
sources = biomes.loc[
    biomes["has_data"] & ~biomes["biome"].isin(["Cropland", "Urban"]), "biome"
].tolist()

c1, c2 = st.columns(2)
src = c1.selectbox("Nature to remove", sources, index=sources.index("Tropical forest"))
dst = c2.selectbox("Turn it into", TARGETS, index=0)
c3, c4 = st.columns(2)
area = c3.select_slider(
    "Area (hectares)",
    options=[100, 1_000, 10_000, 100_000, 1_000_000, 10_000_000],
    value=1_000_000,
    format_func=lambda v: f"{v:,}",
)
years = c4.slider("Years", min_value=1, max_value=50, value=30)

v_from = calc.biome_value(biomes, src)
v_to = calc.biome_value(biomes, dst)
loss = calc.conversion_loss(area, v_from, v_to)
cumulative = calc.cumulative_loss(loss, years)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Value before / yr", ui.money(area * v_from))
m2.metric("Value after / yr", ui.money(area * v_to))
m3.metric("Loss per year", ui.money(loss), delta=f"-{ui.money(loss)}", delta_color="normal")
m4.metric(f"Lost over {years} years", ui.money(cumulative[-1]))

if dst == "Urban":
    st.caption(f"Urban: {calc.biome_note(biomes, 'Urban')}.")

div, unit = ui.axis_unit(cumulative[-1] * f)
fig = go.Figure(
    go.Scatter(
        x=list(range(1, years + 1)),
        y=[v * f / div for v in cumulative],
        mode="lines",
        line=dict(color=ui.CRITICAL, width=3),
        fill="tozeroy",
        fillcolor="rgba(208,59,59,0.12)",
        hovertemplate=f"Year %{{x}}: $%{{y:,.2f}} {unit}<extra></extra>",
    )
)
fig.update_layout(
    title="Accumulated loss (not discounted)",
    xaxis_title="Years after conversion",
    yaxis=dict(title=f"{unit} {ui.currency_label()}".strip(), tickprefix="$", rangemode="tozero"),
    height=380,
    showlegend=False,
)
ui.chart(fig)

ui.takeaway(
    "Clearing nature only looks profitable because the lost services are free — "
    "nobody sends us the bill."
)

crop = calc.biome_value(biomes, "Cropland")
wet = [calc.biome_value(biomes, b) / crop for b in ["Estuaries", "Swamps/floodplains", "Tidal marsh/mangroves"]]
lo, hi = int(min(wet) // 50 * 50), int(-(-max(wet) // 50) * 50)
ui.speaker_notes(
    [
        "Value per hectare comes straight from Costanza's Table 2.",
        f"Wetlands and estuaries are worth {lo}–{hi}× more per hectare than cropland.",
        f"These are 1994 dollars; toggle \"today's dollars\" to multiply by {config.CPI_FACTOR} "
        "(roughly double).",
    ]
)
ui.source_footer(f"{ui.COSTANZA}, Table 2 (value per hectare per year).")
