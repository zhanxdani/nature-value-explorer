import streamlit as st

import config
import screens
from content import texts as T
from utils import ui

X = T.SHARE


def back() -> None:
    visited = [s for s in screens.IDS if s in st.session_state.get("visited", set())]
    ui.go(visited[-1] if visited else screens.FIRST)


def render() -> None:
    with st.container(key="share"):
        ui.html(f'<div class="welcome-title center">{ui.h(X["title"])}</div>')
        if config.APP_URL:
            with st.container(key="qr", horizontal_alignment="center"):
                st.image(ui.qr_png(config.APP_URL), width=min(560, 9999))
            ui.html(f'<div class="qr-url">{ui.h(config.APP_URL.removeprefix("https://"))}</div>')
        else:
            st.info(X["no_url"])
        st.button(X["back"], key="share_back", icon=":material/arrow_back:", on_click=back, width="stretch")
