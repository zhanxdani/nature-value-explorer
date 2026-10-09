import streamlit as st

from content import rules as R
from content import texts as T
from utils import games, img, ui

SID = "6.1"
S = R.SAVE_FOREST
X = T.SAVE_FOREST
KEY = "offer"


def _state() -> tuple[str, int, float]:
    story = st.session_state.get("sf_story", S["default_story"])
    profit = st.session_state.get("sf_profit", S["default_profit"])
    return story, profit, games.forest_value(ui.biomes(), story)


@st.dialog(X["change_title"])
def change_story() -> None:
    story, profit, _ = _state()
    new_story = st.pills(X["forest_pick"], list(S["stories"]), format_func=S["stories"].get,
                         default=story, key="sf_story_pick")
    new_profit = st.slider(X["profit_slider"], 0, S["profit_max"], profit, S["step"], format="$%d",
                           key="sf_profit_pick")
    if st.button(X["apply"], type="primary", **{"width": "stretch"}):
        st.session_state.sf_story = new_story or story
        st.session_state.sf_profit = new_profit
        st.session_state.pop(KEY, None)
        st.session_state.sf_celebrated = False
        st.rerun()


def _strip(profit: float, value: float, offer: float, top: float) -> str:
    """Coloured zones (Ana says no | Win-win | Overpaying), widths proportional to the money,
    with a marker on the current offer and a legend underneath."""
    win_end = max(profit, value)
    zones = [(0, profit, "#E57373", X["zone_no"]), (profit, value, "#81C784", X["zone_win"]),
             (win_end, top, "#E0E0E0", X["zone_over"])]
    shown = [z for z in zones if z[1] > z[0]]
    parts = "".join(
        f'<div style="flex:{end - start:.0f} 0 0;background:{color}"></div>' for start, end, color, _ in shown
    )
    legend = "".join(
        f'<span><i style="background:{color}"></i>{ui.h(label)}</span>' for _, _, color, label in shown
    )
    left = max(1.0, min(99.0, offer / top * 100))
    return (
        f'<div class="strip-wrap"><div class="strip">{parts}</div>'
        f'<div class="strip-marker" style="left:{left:.1f}%"></div></div>'
        f'<div class="strip-legend">{legend}</div>'
    )


def render() -> None:
    story, profit, value = _state()
    top = games.max_offer(value)
    offer = st.session_state.get(KEY, 0)
    out = games.deal_outcome(offer, profit, value)
    status = out["status"]

    ui.top_bar(SID, X["learn"])
    face = S["ana_faces"][status]
    overlay = f'<div class="overlay">{img.avatar(face, R.PEOPLE["ana"]["fallback"], games.deal_approval(offer, profit, value)[0], "Ana")}</div>'
    caption = X["story"].format(profit=profit, forest=S["stories"][story].lower(),
                                value=games.money_about(value))
    ui.scene("scenes/forest_0" if out["forest_saved"] else "scenes/forest_2",
             "🌳" if out["forest_saved"] else "🪓", overlay, caption)

    with st.container(key="row_label_offer", horizontal=True, vertical_alignment="center"):
        ui.slider_label(X["slider"])
        if st.button(X["change"], key="change_story", type="tertiary", icon=":material/edit:"):
            change_story()
    offer = st.slider(X["slider"], 0, top, step=S["step"], format="$%d", key=KEY,
                      label_visibility="collapsed")
    out = games.deal_outcome(offer, profit, value)
    status = out["status"]
    ui.html(_strip(profit, value, offer, top))

    results = X["results"]
    if out["no_deal_possible"]:
        ui.result_line(X["no_win_win"], "warning")
    elif status == "reject":
        ui.result_line(results["reject"].format(value=games.money_about(value)), "error")
    elif status == "cheapest":
        ui.result_line(results["cheapest"], "success")
        if not st.session_state.get("sf_celebrated"):
            st.balloons()
            st.session_state.sf_celebrated = True
    elif status == "win-win":
        ui.result_line(results["win-win"].format(offer=games.money_about(offer), value=games.money_about(value),
                                                 gain=games.money_about(out["gain"])), "success")
    else:
        ui.result_line(results["overpay"], "warning")

    gain = out["gain"]
    ui.meter(":material/forest:", X["forest"], 100 if out["forest_saved"] else 5,
             X["saved"] if out["forest_saved"] else X["cleared"])
    ui.meter(":material/payments:", X["gain"], min(100, max(5, 50 + 50 * gain / value)),
             f"{'+' if gain >= 0 else ''}{games.money_short(gain)}/yr")
    ui.approval_row(S["people"], games.deal_approval(offer, profit, value), {"ana": face})
    ui.nav_bar(SID)
