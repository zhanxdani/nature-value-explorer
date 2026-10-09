import plotly.graph_objects as go
import streamlit as st

from utils import calc, ui

CRITERIA_HELP = {
    "Material": "food, timber, income",
    "Regulating": "climate, water, soil",
    "Non-material": "identity, spirituality, recreation",
    "Intrinsic": "biodiversity for its own sake",
}
KEYS = [f"lens_w_{c}" for c in calc.LENS_CRITERIA]

ui.header(
    "Value lens: from services to contributions",
    "One forest, three futures — pick whose values count and see which future wins.",
)
ui.illustrative_badge()


def apply_role(role: str) -> None:
    for key, w in zip(KEYS, calc.ROLE_PRESETS[role]):
        st.session_state[key] = float(w)
    st.session_state.lens_role = role


def mark_custom() -> None:
    st.session_state.lens_role = "Custom weights"


st.session_state.setdefault("lens_role", "Balanced")
start = calc.ROLE_PRESETS.get(st.session_state.lens_role, calc.ROLE_PRESETS["Balanced"])
for key, w in zip(KEYS, start):
    st.session_state.setdefault(key, float(w))

st.markdown("**Whose eyes do we look through?**")
cols = st.columns(len(calc.ROLE_PRESETS))
for col, role in zip(cols, calc.ROLE_PRESETS):
    col.button(
        role,
        on_click=apply_role,
        args=(role,),
        type="primary" if st.session_state.lens_role == role else "secondary",
        **ui.stretch(st.button),
    )

wcols = st.columns(len(calc.LENS_CRITERIA))
for col, crit, key in zip(wcols, calc.LENS_CRITERIA, KEYS):
    col.slider(
        f"{crit} ({CRITERIA_HELP[crit]})",
        min_value=0.0,
        max_value=10.0,
        step=0.5,
        key=key,
        on_change=mark_custom,
    )

weights = [st.session_state[k] for k in KEYS]
if sum(weights) == 0:
    st.info("All weights are zero, so every criterion counts equally.")
scores = calc.lens_scores(weights)
winner = scores.index[0]

st.markdown(
    f'<p class="big-text">Winner for {st.session_state.lens_role}: {winner}</p>',
    unsafe_allow_html=True,
)

ordered = scores.sort_values(ascending=True)
fig = go.Figure(
    go.Bar(
        x=ordered.values,
        y=ordered.index,
        orientation="h",
        marker_color=[ui.AQUA if name == winner else ui.GREY for name in ordered.index],
        text=[f"{v:.1f}" for v in ordered.values],
        textposition="outside",
        hovertemplate="%{y}: %{x:.2f} / 10<extra></extra>",
    )
)
fig.update_layout(
    xaxis=dict(title="Weighted score (0–10)", range=[0, 10.5]),
    showlegend=False,
    height=300,
)
ui.chart(fig)

norm = calc.normalize_weights(weights)
st.caption(
    "Weights used: "
    + " · ".join(f"{c} {w * 100:.0f}%" for c, w in zip(calc.LENS_CRITERIA, norm))
)

with st.expander("Scores"):
    table = calc.LENS_SCORES.rename(columns={c: f"{c} ({CRITERIA_HELP[c]})" for c in calc.LENS_CRITERIA})
    st.dataframe(table)
    st.caption(
        "Material, regulating and non-material are the NCP groups from Díaz et al. 2018; "
        "intrinsic value is added by us. Scores (0–10) are our illustration."
    )

ui.takeaway(
    "There is no single 'value of nature'. Whose values count changes the answer — "
    "that's why IPBES moved from ecosystem services to nature's contributions to people."
)
ui.speaker_notes(
    [
        "Costanza: one number in dollars. Díaz: multiple values and multiple knowledge systems.",
        "Culture runs through all NCP groups instead of being one \"cultural services\" box.",
        "Question to the class: who should set the weights?",
    ]
)
ui.source_footer(f"{ui.DIAZ}. Options and scores are illustrative.")
