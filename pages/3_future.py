import plotly.graph_objects as go
import streamlit as st

import config
from utils import calc, ui

HORIZON_YEARS = 100
R_MIN, R_MAX, R_STEP = 0.5, 10.0, 0.5  # discount rate slider, %

ui.header(
    "How much do we care about the future?",
    "How the discount rate changes what one hectare of nature is worth today.",
)

biomes = ui.biomes()
f = ui.factor()

options = biomes.loc[biomes["has_data"] & (biomes["value_per_ha"] > 0), "biome"].tolist()
c1, c2 = st.columns(2)
biome = c1.selectbox("Ecosystem", options, index=options.index("Tropical forest"))
r_pct = c2.slider(
    "Discount rate (%)",
    min_value=R_MIN,
    max_value=R_MAX,
    value=config.DEFAULT_DISCOUNT * 100,
    step=R_STEP,
)
r = r_pct / 100
a = calc.biome_value(biomes, biome)

l1, l2 = st.columns(2)
with l1:
    st.caption("Value over T years")
    st.latex(r"PV = A \times \frac{1 - (1+r)^{-T}}{r}")
with l2:
    st.caption("Value forever")
    st.latex(r"PV_{\infty} = \frac{A}{r}")

m1, m2, m3 = st.columns(3)
m1.metric("Value per hectare per year", ui.money(a))
m2.metric(f"Value over {HORIZON_YEARS} years", ui.money(calc.pv_annuity(a, r, HORIZON_YEARS)))
m3.metric("Value forever", ui.money(calc.perpetuity(a, r)))

rates = [R_MIN + i * R_STEP for i in range(int((R_MAX - R_MIN) / R_STEP) + 1)]
values = [calc.perpetuity(a, x / 100) * f for x in rates]
div, unit = ui.axis_unit(max(values))
fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=rates,
        y=[v / div for v in values],
        mode="lines",
        line=dict(color=ui.BLUE, width=3),
        hovertemplate=f"r = %{{x}}%: $%{{y:,.1f}} {unit}<extra></extra>",
        name="Value forever",
    )
)
fig.add_trace(
    go.Scatter(
        x=[r_pct],
        y=[calc.perpetuity(a, r) * f / div],
        mode="markers",
        marker=dict(size=16, color=ui.ORANGE, line=dict(width=2, color="white")),
        hovertemplate="Your choice: r = %{x}%<extra></extra>",
        name="Your choice",
    )
)
fig.update_layout(
    title=f"Value forever of 1 ha of {biome.lower()}",
    xaxis=dict(title="Discount rate r (%)", ticksuffix="%"),
    yaxis=dict(title=f"{unit} {ui.currency_label()}".strip(), tickprefix="$", rangemode="tozero"),
    showlegend=False,
    height=400,
)
ui.chart(fig)

compare_to = R_MAX if r_pct < R_MAX else 1.0
low_r, high_r = min(r_pct, compare_to), max(r_pct, compare_to)
times = calc.perpetuity(a, low_r / 100) / calc.perpetuity(a, high_r / 100)
st.markdown(
    f'<p class="big-text">At r = {low_r:g}% this hectare is worth {times:.0f}× more '
    f"than at r = {high_r:g}%</p>",
    unsafe_allow_html=True,
)

ui.takeaway(
    "The discount rate is an ethical choice: the higher it is, the less the future counts."
)
ui.speaker_notes(
    [
        f"Costanza used {config.DEFAULT_DISCOUNT * 100:.0f}% to convert stock values into annual flows.",
        "r = 0 would make the forest's value infinite.",
        "Question to the class: what rate would you choose for your grandchildren?",
    ]
)
ui.source_footer(f"{ui.COSTANZA}, Table 2 and Methods (discounting).")
