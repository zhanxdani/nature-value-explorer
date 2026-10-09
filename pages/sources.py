import streamlit as st

from content import texts as T
from utils import ui

S = T.SOURCES

st.title(S["title"])
for ref in S["refs"]:
    with ui.card():
        st.markdown(ref)
st.info(S["note"])
st.caption(S["values"])

ui.page_link(ui.PAGES[0], "🏠 Back to the start")
