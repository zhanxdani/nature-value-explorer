import streamlit as st

from content import rules as R
from content import texts as T
from utils import games, ui

SID = "3.1"
W = R.WETLAND
X = T.WETLAND


def reset_storm() -> None:
    st.session_state.storm = False


def toggle_storm() -> None:
    st.session_state.storm = not st.session_state.get("storm", False)


def learn_extra() -> None:
    ui.md(f"**{X['services_heading']}**")
    for row in ui.wetland_services().itertuples():
        ui.md(f"- {row.service}: {games.money_about(row.value_per_ha)}")
    st.caption(ui.esc(X["note"]))


def render() -> None:
    biomes = ui.biomes()
    if "wetland" not in st.session_state:  # new visit: slider starts at "Keep it", no storm
        st.session_state.storm = False
    stop = W["stops"].index(st.session_state.get("wetland", W["stops"][0]))
    storm = st.session_state.get("storm", False)
    flooded = storm and games.storm_floods(stop)

    ui.top_bar(SID, X["learn"], learn_extra)
    scene = W["flood_scene"] if flooded else W["scenes"][stop]
    ui.scene(scene, "🌧️🏚️" if flooded else ["🌿🦆", "🌿🌾", "🌾🌾", "🌾🌾"][stop], caption=X["story"])

    with st.container(key="row_label_wetland", horizontal=True, vertical_alignment="center"):
        ui.slider_label(X["slider"])
        st.button(X["storm"], key="storm_btn", type="tertiary", icon=":material/thunderstorm:",
                  on_click=toggle_storm)
    stop = W["stops"].index(st.select_slider(X["slider"], W["stops"], key="wetland",
                                             label_visibility="collapsed", on_change=reset_storm))
    p = W["drained"][stop]
    income = games.wetland_farm_income(p)
    nature = games.wetland_nature_value(biomes, p)
    nature_max = games.wetland_nature_value(biomes, 0)

    if storm:
        ui.result_line(X["flooded"] if flooded else X["dry"], "error" if flooded else "success")
    elif stop == 0:
        ui.result_line(X["kept"], "success")
    else:
        ui.result_line(X["result"].format(gain=games.money_short(income),
                                          loss=games.money_short(nature_max - nature)), "warning")

    income_max = games.wetland_farm_income(1)
    ui.meter(":material/agriculture:", X["income"], income / income_max * 100, f"{games.money_short(income)}/yr")
    ui.meter(":material/water_drop:", X["nature"], nature / nature_max * 100, f"{games.money_short(nature)}/yr")
    ui.meter(":material/shield:", X["flood"], W["flood_safety"][stop], f"{W['flood_safety'][stop]}%")
    approval = W["storm_approval"] if flooded else W["approval"][stop]
    ui.approval_row(W["people"], approval)
    ui.nav_bar(SID)
