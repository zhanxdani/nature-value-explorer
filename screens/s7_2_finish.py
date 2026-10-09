import streamlit as st

import screens
from content import texts as T
from utils import img, ui

SID = "7.2"
X = T.FINISH


def restart() -> None:
    for key in list(st.session_state.keys()):
        if key != "presenter":
            del st.session_state[key]
    ui.go(screens.FIRST)


def render() -> None:
    ui.top_bar(SID)
    score = st.session_state.get("quiz_score", 0)
    total = len(T.QUIZ["questions"])
    ui.html(img.card("badge", "🏅", "badge"))
    ui.html(f'<div class="big-score">{ui.h(X["score"].format(score=score, total=total))}</div>'
            f'<div class="card-title center">{ui.h(X["completed"])}</div>')
    st.button(X["share"], key="fin_share", type="primary", icon=":material/qr_code_2:", on_click=ui.go,
              args=("share",), width="stretch")
    with st.container(key="row_finish", horizontal=True, gap="small"):
        if st.button(X["sources"], key="fin_sources", icon=":material/library_books:", width="stretch"):
            ui.sources_dialog()
        st.button(X["restart"], key="fin_restart", icon=":material/replay:", on_click=restart, width="stretch")
    ui.nav_bar(SID, show_next=False)
