import plotly.graph_objects as go
import streamlit as st

from utils import calc, ui

ECOSYSTEMS = ["Swamps/floodplains", "Tidal marsh/mangroves", "Coral reefs"]
STATUS_ICON = {"Safe": "🟢", "Warning": "🟡", "Danger": "🔴"}

ui.header(
    "Tipping point",
    "As an ecosystem shrinks, each lost hectare becomes more valuable than the last.",
)
ui.illustrative_badge()

biomes = ui.biomes()
f = ui.factor()

eco = st.selectbox("Ecosystem", ECOSYSTEMS)
v0 = calc.biome_value(biomes, eco)

main = st.container()
with st.expander("Model settings"):
    q_min = st.slider("Critical minimum (%)", min_value=5, max_value=40, value=20)
    log_y = st.toggle("Log scale", value=False)

# Keep the remaining-area slider valid when the critical minimum moves up.
if st.session_state.get("tp_q", 100) <= q_min:
    st.session_state.tp_q = q_min + 1
st.session_state.setdefault("tp_q", 100)

with main:
    q = st.select_slider(
        "How much is left? (%)",
        options=list(range(100, q_min, -1)),
        key="tp_q",
    )

mult = calc.tipping_multiplier(q, q_min)
value = calc.tipping_value(v0, q, q_min)
status = calc.tipping_status(mult)

m1, m2, m3 = st.columns(3)
m1.metric("Value of the next hectare lost", f"{ui.money(value)} /ha/yr")
m2.metric("Compared with today", f"×{mult:.1f}")
m3.metric("Status", f"{STATUS_ICON[status]} {status}")

if q - q_min <= 3:
    st.error("Near the threshold the value shoots towards infinity — and the loss may be irreversible.")

# Curve
qs = list(range(q_min + 1, 101))
ys = [calc.tipping_value(v0, x, q_min) * f for x in qs]
q2, q5 = calc.tipping_zone_edges(q_min)
x_left, x_right = 101, q_min - 3

fig = go.Figure()
for x0, x1, color in [
    (x_left, q2, "rgba(12,163,12,0.12)"),
    (q2, q5, "rgba(250,178,25,0.18)"),
    (q5, x_right, "rgba(208,59,59,0.14)"),
]:
    fig.add_vrect(x0=x0, x1=x1, fillcolor=color, line_width=0, layer="below")
for x, label in [((100 + q2) / 2, "Safe ×<2"), ((q2 + q5) / 2, "Warning ×2–5"), ((q5 + q_min) / 2, "Danger ×>5")]:
    fig.add_annotation(x=x, y=1.0, yref="paper", text=label, showarrow=False, yanchor="bottom")
fig.add_vline(x=q_min, line_dash="dash", line_color=ui.CRITICAL, line_width=2)
fig.add_annotation(
    x=q_min, y=0.5, yref="paper", text="Point of no return", textangle=-90,
    showarrow=False, xanchor="left", font=dict(color=ui.CRITICAL),
)
fig.add_trace(
    go.Scatter(
        x=qs, y=ys, mode="lines", line=dict(color=ui.BLUE, width=3),
        hovertemplate="%{x}% left: $%{y:,.0f} /ha/yr<extra></extra>",
    )
)
fig.add_trace(
    go.Scatter(
        x=[q], y=[value * f], mode="markers",
        marker=dict(size=18, color=ui.ORANGE, line=dict(width=2, color="white")),
        hovertemplate="Now: %{x}% left<extra></extra>",
    )
)
fig.update_layout(
    xaxis=dict(title="Area left (%) → more loss", range=[x_left, x_right], ticksuffix="%"),
    yaxis=dict(
        title=f"{ui.currency_label()} per ha per year",
        type="log" if log_y else "linear",
        tickprefix="$",
    ),
    showlegend=False,
    height=440,
    margin=dict(t=60),
)
ui.chart(fig)

ui.takeaway(
    "Every lost hectare costs more than the one before. "
    "Near a threshold, 'just a little more' becomes a catastrophe."
)
ui.speaker_notes(
    [
        "Costanza assumed no thresholds, so the authors themselves say the real value is higher.",
        "Real examples: coral bleaching, wetland collapse.",
        "Hypothesis: the closer an ecosystem is to its threshold, the faster its marginal value grows.",
    ]
)
ui.source_footer(
    f"Starting value per hectare: {ui.COSTANZA}, Table 2. "
    "Curve shape inspired by Fig. 1b of the paper; the formula is our illustration."
)
