import streamlit as st

from content import rules as R
from content import texts as T
from utils import games, ui

SID = "5.3"
W = R.WHO_DECIDES
X = T.WHO_DECIDES
FALLBACK = {"plantation": "🌴🚜", "agro": "🌳🌾🐝", "sacred": "🌳🙏"}


def render() -> None:
    stop = W["stops"].index(st.session_state.get("who", W["stops"][0]))
    future = W["futures"][stop]
    ui.top_bar(SID, X["learn"])
    ui.scene(W["scenes"][future], FALLBACK[future])
    ui.slider_label(X["slider"])
    stop = W["stops"].index(st.select_slider(X["slider"], W["stops"], key="who",
                                             label_visibility="collapsed"))
    future = W["futures"][stop]
    ui.result_line(X["results"][future], "info")
    ui.small_fact(X["always"])
    approvals = W["approval"][stop]
    avg = games.average_approval(approvals)
    ui.meter(":material/groups:", X["average"], avg, f"{avg}%")
    ui.approval_row(W["people"], approvals)
    ui.nav_bar(SID)
