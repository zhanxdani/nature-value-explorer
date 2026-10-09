import streamlit as st

import screens
from content import texts as T
from utils import ui

W = T.WELCOME


def render() -> None:
    with st.container(key="welcome"):
        ui.html('<div class="hero">' + ui.img.scene("hero", "🌍") + "</div>")
        ui.html(f'<div class="welcome-title">{ui.h(W["title"])}</div>'
                f'<div class="welcome-sub">{ui.h(W["subtitle"])}</div>')
        st.button(W["start"], type="primary", key="start", on_click=ui.go,
                  args=(screens.neighbour(screens.FIRST, 1),), width="stretch")
        with st.container(key="row_welcome_links", horizontal=True):
            if st.button(T.MENU["glossary"], icon=":material/menu_book:", type="tertiary", key="w_glossary"):
                ui.glossary_dialog()
            if st.button(T.MENU["sources"], icon=":material/library_books:", type="tertiary", key="w_sources"):
                ui.sources_dialog()
