import streamlit as st

from content import texts as T
from utils import ui

W = T.WELCOME

st.title(W["title"])
ui.md(f"*{W['subtitle']}*")

if st.button(W["start"], type="primary", key="big_start", **ui.stretch(st.button)):
    ui.go(ui.PAGES[1])

st.subheader(W["chapters_heading"])
finished = ui.done()
for n, ch in enumerate(T.CHAPTERS[1:], start=1):
    tick = "✅" if n in finished else "⬜"
    ui.page_link(ui.PAGES[n], f"{tick} {n} · {ch['emoji']} {ch['title']}")

st.caption(W["more_heading"])
c1, c2 = st.columns(2)
with c1:
    ui.page_link(ui.GLOSSARY_PAGE, "📖 Glossary")
with c2:
    ui.page_link(ui.SOURCES_PAGE, "📚 Sources")
