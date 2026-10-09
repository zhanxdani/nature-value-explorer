import streamlit as st

from content import rules as R
from content import texts as T
from utils import ui

SID = "1.2"
B = R.BEES
X = T.BEES


def render() -> None:
    stop = B["stops"].index(st.session_state.get("bees", B["stops"][0]))
    ui.top_bar(SID, X["learn"], learn_source=X["source"])
    ui.scene(B["scenes"][stop], ["🍎🍯☕", "🍎☕", "🍞💧"][stop])
    ui.slider_label(X["slider"])
    stop = B["stops"].index(st.select_slider(X["slider"], B["stops"], key="bees", label_visibility="collapsed"))
    ui.result_line(X["results"][stop], ["success", "warning", "error"][stop])
    ui.small_fact(X["fact"])
    ui.meter(":material/restaurant:", X["food"], B["food_variety"][stop], f"{B['food_variety'][stop]}%")
    ui.meter(":material/sell:", X["prices"], B["prices_pct"][stop], B["prices"][stop], good_high=False)
    ui.approval_row(B["people"], B["approval"][stop])
    ui.nav_bar(SID)
