import streamlit as st

from content import texts as T
from utils import ui

st.title("📖 Glossary")
for term, definition in T.GLOSSARY:
    with st.expander(term):
        ui.md(definition)

ui.page_link(ui.PAGES[0], "🏠 Back to the start")
