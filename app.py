"""Nature Value Explorer: page config, global CSS, navigation and presenter flag."""

import streamlit as st

from content import texts as T
from utils import ui

st.set_page_config(
    page_title="Nature Value Explorer",
    page_icon="🌍",
    layout="centered",
    initial_sidebar_state="collapsed",
)

ui.sync_from_query_params()
ui.inject_css()

journey = [
    st.Page(ui.PAGES[n], title=ch["nav"], icon=ch["emoji"], default=(n == 0))
    for n, ch in enumerate(T.CHAPTERS)
]
extras = [
    st.Page(ui.GLOSSARY_PAGE, title="Glossary", icon="📖"),
    st.Page(ui.SOURCES_PAGE, title="Sources", icon="📚"),
    st.Page(ui.SHARE_PAGE, title="Share", icon="📱"),
]

pg = st.navigation({"Journey": journey, "More": extras}, position="top")
pg.run()
