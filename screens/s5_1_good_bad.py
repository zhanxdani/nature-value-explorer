import streamlit as st

from content import texts as T
from utils import img, ui

SID = "5.1"
X = T.GOOD_BAD
CARDS = X["cards"]


def answer(choice: str) -> None:
    st.session_state.gb_answer = choice


def next_card() -> None:
    st.session_state.gb_idx += 1
    st.session_state.gb_answer = None


def restart() -> None:
    st.session_state.gb_idx = 0
    st.session_state.gb_answer = None


def render() -> None:
    st.session_state.setdefault("gb_idx", 0)
    st.session_state.setdefault("gb_answer", None)
    idx = st.session_state.gb_idx
    ui.top_bar(SID, X["learn"])
    dots = "".join("●" if i < idx else ("◉" if i == idx else "○") for i in range(len(CARDS)))
    ui.html(f'<div class="nav-dots">{dots}</div>')

    if idx >= len(CARDS):
        ui.scene("hero", "🐺🦟🌊🐝")
        ui.result_line(X["done"], "info")
        st.button(T.COMMON["play_again"], key="gb_again", icon=":material/replay:", on_click=restart,
                  width="stretch")
        ui.nav_bar(SID)
        return

    card = CARDS[idx]
    ui.html(img.card(f"ncp/{card['key']}", card["fallback"], "tall"))
    ui.html(f'<div class="card-title">{ui.h(card["name"])}</div>')
    if st.session_state.gb_answer is None:
        with st.container(key="row_gb", horizontal=True, gap="small"):
            for i, label in enumerate(X["buttons"]):
                st.button(label, key=f"gb_{i}", on_click=answer, args=(label,), width="stretch")
    else:
        ui.result_line(card["text"], "info")
        st.button(X["next"], key="gb_next", type="primary", icon=":material/arrow_forward:",
                  icon_position="right", on_click=next_card, width="stretch")
    ui.nav_bar(SID)
