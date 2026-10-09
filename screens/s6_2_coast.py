import streamlit as st

from content import rules as R
from content import texts as T
from utils import games, ui

SID = "6.2"
C = R.COAST
X = T.COAST


def render() -> None:
    stop = C["stops"].index(st.session_state.get("coast", C["stops"][0]))
    ui.top_bar(SID, X["learn"], learn_source=X["source"])
    ui.scene(C["scenes"][stop], ["🧱🌊", "🧱🌴", "🌴🪸🐟"][stop])
    ui.slider_label(X["slider"])
    stop = C["stops"].index(st.select_slider(X["slider"], C["stops"], key="coast", label_visibility="collapsed"))
    ratio = f"{games.concrete_vs_nature_ratio():.0f}"
    ui.result_line(X["results"][stop].format(ratio=ratio), ["warning", "info", "success"][stop])
    ui.small_fact(X["fact"])
    cost = games.coast_cost_per_km(C["nature_share"][stop])
    ui.meter(":material/payments:", X["cost"], cost / games.coast_cost_per_km(0) * 100,
             games.money_short(cost), good_high=False)
    ui.meter(":material/shield:", X["ready"], C["ready_pct"][stop], f"{C['ready_pct'][stop]}%")
    ui.meter(":material/set_meal:", X["fish"], C["fish_pct"][stop], f"{C['fish_pct'][stop]}%")
    ui.approval_row(C["people"], C["approval"][stop])
    ui.nav_bar(SID)
