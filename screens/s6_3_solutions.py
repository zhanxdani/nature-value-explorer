import streamlit as st

import screens
from content import texts as T
from utils import img, ui

SID = "6.3"
X = T.SOLUTIONS
CARDS = X["cards"]


def move(step: int) -> None:
    st.session_state.sol_idx = (st.session_state.get("sol_idx", 0) + step) % len(CARDS)


def render() -> None:
    i = st.session_state.get("sol_idx", 0)
    card = CARDS[i]
    ui.top_bar(SID, X["learn"])
    ui.html(img.card(f"solutions/{card['key']}", card["fallback"], "tall"))
    ui.html(f'<div class="card-title">{ui.h(card["title"])}</div>'
            f'<div class="story">{ui.h(card["what"])}</div>'
            f'<div class="small-fact">{ui.h(card["example"])}</div>')
    st.button(X["fixes"].format(n=card["chapter"]), key="sol_fixes", type="tertiary", icon=":material/link:",
              on_click=ui.go, args=(screens.first_screen(card["chapter"]),))
    with st.container(key="row_sol", horizontal=True, vertical_alignment="center"):
        st.button("‹", key="sol_prev", on_click=move, args=(-1,), width="stretch")
        ui.html(f'<div class="nav-dots">{i + 1}/{len(CARDS)}</div>')
        st.button("›", key="sol_next", on_click=move, args=(1,), width="stretch")
    ui.nav_bar(SID)
