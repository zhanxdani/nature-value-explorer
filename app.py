"""Nature Value Explorer: page config, CSS, router and presenter flag."""

import streamlit as st

import screens
from utils import ui

st.set_page_config(
    page_title="Nature Value Explorer",
    page_icon="🌍",
    layout="centered",
    initial_sidebar_state="collapsed",
)

ui.inject_css()
ui.init_router()
screens.module(ui.current()).render()
ui.run_pending_dialog()
