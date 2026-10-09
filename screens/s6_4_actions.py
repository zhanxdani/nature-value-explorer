import streamlit as st

from content import texts as T
from utils import ui

SID = "6.4"
X = T.ACTIONS
TILES = X["tiles"]


def toggle(key: str) -> None:
    picked = st.session_state.setdefault("actions", [])
    if key in picked:
        picked.remove(key)
    else:
        picked.append(key)
    if len(picked) < X["min"]:
        st.session_state.ally_celebrated = False


def render() -> None:
    picked = st.session_state.setdefault("actions", [])
    ui.top_bar(SID, X["learn"])
    ui.small_fact(X["hint"])
    css = []
    for row in range(2):
        with st.container(key=f"row_actions_{row}", horizontal=True, gap="small"):
            for tile in TILES[row * 3:(row + 1) * 3]:
                st.button(tile["label"], key=f"tile_{tile['key']}", icon=tile["icon"], on_click=toggle,
                          args=(tile["key"],), width="stretch")
                if tile["key"] in picked:
                    css.append(f".st-key-tile_{tile['key']} button {{ border: 3px solid {ui.GREEN} !important; "
                               "background-color: #E8F5E9; }")
    ui.extra_css(css)
    if len(picked) >= X["min"]:
        ui.result_line(X["ally"], "success")
        if not st.session_state.get("ally_celebrated"):
            st.balloons()
            st.session_state.ally_celebrated = True
    else:
        ui.result_line(f"{len(picked)} / {X['min']}", "info")
    ui.nav_bar(SID)
