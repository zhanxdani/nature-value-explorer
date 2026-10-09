import streamlit as st

import config
from content import texts as T
from utils import games, ui

N = 6
C = T.CH6
SOLUTIONS = T.SOLUTIONS
biomes = ui.biomes()

# Services Ana's forest gives everyone, compared with a farm (per ha per year)
services_saved = games.value_per_ha(biomes, "tropical_forest") - games.value_per_ha(biomes, "cropland")
farm_profit = config.ANA_FARM_PROFIT
scale_max = max(T.ANA_OFFERS)

st.session_state.setdefault("sol_idx", 0)
st.session_state.setdefault("ally_celebrated", False)


def move(step: int) -> None:
    st.session_state.sol_idx = (st.session_state.sol_idx + step) % len(SOLUTIONS)


def actions_changed() -> None:
    picked = st.session_state.get("my_actions") or []
    if len(picked) >= T.ALLY_MIN and not st.session_state.ally_celebrated:
        st.session_state.ally_celebrated = "now"
    elif len(picked) < T.ALLY_MIN:
        st.session_state.ally_celebrated = False


ui.chapter_header(N)
ui.learn(C["learn"])

# ---------------------------------------------------------------- Play A: save the forest
ui.play(C["play_a"])
ui.model_badge(C["badge"])
with ui.card():
    ui.md(C["story"])
    offer = st.pills(C["offer"], T.ANA_OFFERS, format_func=lambda v: f"${v:,}", key="ana_offer")

if offer is not None:
    outcome = games.deal_outcome(offer, farm_profit, services_saved)
    show = {"reject": st.error, "deal": st.success, "overpay": st.warning}[outcome]
    show(ui.esc(T.ANA_REACTIONS[offer]))
    ui.color_strip(
        [(0, farm_profit, ui.RED), (farm_profit, services_saved, ui.LIGHT_GREEN),
         (services_saved, scale_max, ui.GREY)],
        marker=offer, marker_label=f"${offer:,}", scale_max=scale_max,
    )
    ui.md(f"{C['zone_no']}  \n{C['zone_win']}  \n{C['zone_over']}")
    ui.md(C["sweet_spot"])

# ---------------------------------------------------------------- Play B: six real solutions
ui.play(C["play_b"])
i = st.session_state.sol_idx
s = SOLUTIONS[i]
with ui.card():
    st.caption(f"{i + 1} / {len(SOLUTIONS)}")
    st.markdown(f"### {s['title']}")
    ui.md(f"{C['what']} {s['what']}")
    ui.md(f"{C['example']} {s['example']}")
    ui.page_link(ui.PAGES[s["chapter"]], "🔗 " + C["fixes"].format(n=s["chapter"], problem=s["problem"]))
    ui.md(f"{C['limits']} {s['limits']}")
with st.container(key="nav_solutions"):
    prev_col, next_col = st.columns(2)
    prev_col.button(C["prev"], on_click=move, args=(-1,), key="sol_prev", **ui.stretch(st.button))
    next_col.button(C["next"], on_click=move, args=(1,), key="sol_next", **ui.stretch(st.button))

# ---------------------------------------------------------------- Play C: what can you do?
ui.play(C["play_c"])
actions = st.pills(C["pick_actions"], T.YOUR_ACTIONS, selection_mode="multi",
                   key="my_actions", on_change=actions_changed)
if len(actions) >= T.ALLY_MIN:
    st.success(C["ally"])
    if st.session_state.ally_celebrated == "now":
        st.balloons()
        st.session_state.ally_celebrated = True
elif actions:
    st.caption(C["pick_more"])

ui.remember(C["remember"])
with ui.more():
    ui.md(C["more"])

ui.nav_buttons(N)
