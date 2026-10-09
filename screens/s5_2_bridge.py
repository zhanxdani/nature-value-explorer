import streamlit as st

from content import texts as T
from utils import img, ui

SID = "5.2"
X = T.BRIDGE


def answer(choice: str) -> None:
    st.session_state.bridge = choice


def render() -> None:
    ui.top_bar(SID, X["learn"], learn_source="Díaz, S. et al. (2018). Science 359, 270–272.")
    ui.html(img.card("ncp/root_bridge", "🌳🌉", "tall"))
    ui.story(X["line"])
    ui.html(f'<div class="card-title">{ui.h(X["question"])}</div>')
    with st.container(key="row_bridge", horizontal=True, gap="small"):
        for i, label in enumerate(X["buttons"]):
            chosen = st.session_state.get("bridge") == label
            st.button(label, key=f"bridge_{i}", on_click=answer, args=(label,), width="stretch",
                      type="primary" if chosen else "secondary")
    if st.session_state.get("bridge"):
        right = st.session_state.bridge == X["buttons"][-1]
        ui.result_line(("🎉 " if right else "🤔 ") + X["answer"], "success" if right else "info")
    ui.nav_bar(SID)
