import streamlit as st

from content import texts as T
from utils import img, ui

SID = "1.1"
M = T.MORNING
ITEMS = {i["key"]: i for i in T.MORNING_ITEMS}


def toggle(key: str) -> None:
    picked = st.session_state.setdefault("morning", [])
    if key in picked:
        picked.remove(key)
    else:
        picked.append(key)
    st.session_state.morning_last = key


def render() -> None:
    picked = st.session_state.setdefault("morning", [])
    ui.top_bar(SID, M["learn"])
    ui.small_fact(M["hint"])

    css = []
    for row, keys in enumerate((list(ITEMS)[:4], list(ITEMS)[4:])):
        with st.container(key=f"row_items_{row}", horizontal=True, gap="small"):
            for key in keys:
                item = ITEMS[key]
                url = img.url(f"items/{key}")
                st.button(item["name"], key=f"tile_{key}", on_click=toggle, args=(key,),
                          icon=None if url else item["fallback"], width="stretch")
                if url:
                    css.append(f'.st-key-tile_{key} button {{ background-image: url("{url}"); '
                               "justify-content: flex-end; color: #fff; text-shadow: 0 1px 3px #000; }")
                if key in picked:
                    css.append(f".st-key-tile_{key} button {{ border: 3px solid {ui.GREEN} !important; "
                               "background-color: #E8F5E9; }")
    ui.extra_css(css)

    last = st.session_state.get("morning_last")
    if last and last in picked:
        item = ITEMS[last]
        with st.container(border=True, key="morning_card"):
            ui.html(f'<div class="story"><b>{ui.h(item["name"])}:</b> {ui.h(item["line"])}</div>')
            st.markdown(" ".join(f":green-badge[{s}]" for s in item["services"]))
    ui.result_line(M["counter"].format(n=len(picked)), "success" if picked else "info")
    ui.nav_bar(SID)
