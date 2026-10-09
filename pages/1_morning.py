import streamlit as st

from content import texts as T
from utils import ui

N = 1
C = T.CH1
ITEMS = {i["item"]: i for i in T.MORNING_ITEMS}

ui.chapter_header(N)
ui.learn(C["learn"])

ui.play(C["play"])
picked = st.pills(C["pick"], list(ITEMS), selection_mode="multi", key="morning_items")

if picked:
    ui.md("### " + C["counter"].format(n=len(picked)))
    for name in picked:
        item = ITEMS[name]
        with ui.card():
            st.markdown(f"**{name}**")
            ui.md(item["text"])
            st.markdown(" ".join(f":green-badge[{s}]" for s in item["services"]))
else:
    st.info(C["empty"])

ui.remember(C["remember"])

with ui.more():
    ui.md(C["more_intro"])
    st.markdown("\n".join(f"- {s}" for s in T.SEVENTEEN_SERVICES))
    st.caption("Source: Costanza et al. (1997), Table 1.")

ui.nav_buttons(N)
