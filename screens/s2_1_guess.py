import streamlit as st

import config
from content import texts as T
from utils import ui

SID = "2.1"
G = T.GUESS


def reveal() -> None:
    st.session_state.guess_revealed = True


def render() -> None:
    ui.top_bar(SID, G["learn"])
    ui.scene("hero", "💰")
    ui.slider_label(G["slider"])
    guess = st.slider(G["slider"], 0, 100, 5, 1, key="guess", label_visibility="collapsed")
    if not st.session_state.get("guess_revealed"):
        st.button(G["reveal"], type="primary", key="reveal", on_click=reveal, width="stretch")
    else:
        top = max(guess, config.TOTAL_HIGH_TN)
        bars = [
            (":material/person:", G["your_guess"], guess, f"${guess}T"),
            (":material/forest:", G["nature"].format(low=config.TOTAL_LOW_TN, high=config.TOTAL_HIGH_TN),
             config.TOTAL_AVG_TN, f"≈ ${config.TOTAL_AVG_TN}T"),
            (":material/public:", G["economy"], config.WORLD_GNP_1997_TN, f"≈ ${config.WORLD_GNP_1997_TN}T"),
        ]
        for icon, label, value, text in bars:
            ui.meter(icon, label, value / top * 100, text)
        ui.result_line(G["result"], "success")
    ui.nav_bar(SID)
