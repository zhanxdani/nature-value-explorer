import plotly.graph_objects as go
import streamlit as st

from utils import calc, ui

FORESTS = ["Tropical forest", "Temperate/boreal forest", "Tidal marsh/mangroves"]

ui.header(
    "Deal builder: Payments for Ecosystem Services",
    "A farmer can clear forest for cropland. Can we pay them to keep it — "
    "and is it worth it for society?",
)

biomes = ui.biomes()
f = ui.factor()

c1, c2 = st.columns(2)
forest = c1.selectbox("Type of forest", FORESTS)
area = c2.slider("Area (ha)", min_value=10, max_value=10_000, value=100, step=10)

ui.illustrative_badge()
c3, c4 = st.columns(2)
cur = ui.currency_label()
opportunity_cost = c3.slider(
    f"Farmer's profit from clearing ({cur}/ha/yr)", min_value=0, max_value=2_000, value=300, step=10
)
payment = c4.slider(
    f"Payment offered to keep the forest ({cur}/ha/yr)", min_value=0, max_value=2_500, value=150, step=10
)

# Sliders are in the displayed currency, so convert the paper's values to match.
services_saved = (calc.biome_value(biomes, forest) - calc.biome_value(biomes, "Cropland")) * f
deal = calc.pes_deal(services_saved, opportunity_cost, payment, area)

m1, m2, m3 = st.columns(3)
m1.metric("Farmer's decision", "✅ Accepts" if deal["farmer_accepts"] else "❌ Says no")
m2.metric("Forest", "🌳 Kept" if deal["forest_kept"] else "🪓 Cleared")
if deal["farmer_accepts"]:
    m3.metric("Society's net gain / yr", ui.money(deal["society_net_gain"], convert=False))
else:
    m3.metric("Society's net gain / yr", ui.money(-deal["loss"], convert=False))
    st.error(
        ui.esc(
            f"The farmer clears the forest. Society loses {ui.money(deal['loss'], convert=False)} "
            "of services every year."
        )
    )

if not deal["has_deal_zone"]:
    st.warning("No win-win deal possible with these numbers")

# Number line of possible payments
x_max = max(services_saved, opportunity_cost, payment) * 1.15
zone_end = max(opportunity_cost, services_saved)
fig = go.Figure()
segments = [(0, opportunity_cost, "rgba(208,59,59,0.35)", "Farmer says no")]
if deal["has_deal_zone"]:
    segments.append((opportunity_cost, services_saved, "rgba(12,163,12,0.40)", "Win-win deal zone"))
segments.append((zone_end, x_max, "rgba(137,135,129,0.35)", "Society overpays"))
for x0, x1, color, label in segments:
    if x1 <= x0:
        continue
    fig.add_shape(type="rect", x0=x0, x1=x1, y0=0, y1=1, fillcolor=color, line_width=0, layer="below")
    fig.add_annotation(x=(x0 + x1) / 2, y=0.5, text=label, showarrow=False)
fig.add_trace(
    go.Scatter(
        x=[payment], y=[1.12], mode="markers+text",
        marker=dict(symbol="triangle-down", size=22, color=ui.BLUE),
        text=[f"Your offer: {ui.money(payment, convert=False)}"],
        textposition="top center",
        hovertemplate="Payment: $%{x:,.0f} /ha/yr<extra></extra>",
    )
)
fig.update_layout(
    xaxis=dict(title=f"Payment, {cur} per ha per year", range=[0, x_max], tickprefix="$", showgrid=False),
    yaxis=dict(visible=False, range=[-0.1, 1.6]),
    showlegend=False,
    height=230,
)
ui.chart(fig)
st.caption(
    ui.esc(
        f"Services saved by keeping 1 ha of {forest.lower()} instead of cropland: "
        f"{ui.money(services_saved, convert=False)} per year."
    )
)

st.subheader("Solutions in the real world")
st.markdown(
    "- **Payments for ecosystem services:** Costa Rica's national program since 1997.\n"
    "- **Natural capital accounting:** UN SEEA Ecosystem Accounting standard (2021).\n"
    "- **Protected areas:** 30×30 target of the Kunming-Montreal Global Biodiversity Framework (2022).\n"
    "- **Co-management** with indigenous and local communities (Díaz et al. 2018)."
)

ui.takeaway(
    "Paying to protect nature works when the payment beats the farmer's profit "
    "but stays below the value of what we save."
)
ui.speaker_notes(
    [
        "PES turns Costanza's \"invisible value\" into real money for real people.",
        "It doesn't work everywhere: sometimes the numbers don't add up, as with the temperate forest.",
        "Best results come from combining money (Costanza) with local values and knowledge (Díaz).",
    ]
)
ui.source_footer(
    f"Forest and cropland values: {ui.COSTANZA}, Table 2. "
    "Farmer's profit and payment are illustrative inputs."
)
