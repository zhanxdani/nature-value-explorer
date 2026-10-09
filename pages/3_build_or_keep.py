import streamlit as st

import config
from content import texts as T
from utils import games, ui

N = 3
C = T.CH3
biomes = ui.biomes()
lost = ui.lost_services()


def reset_trade() -> None:
    st.session_state.trade_built = False
    st.session_state.trade_undo = False


st.session_state.setdefault("trade_built", False)
st.session_state.setdefault("trade_undo", False)

ui.chapter_header(N)
ui.learn(C["learn"])

ui.play(C["play"])
nature = st.pills(C["choose_nature"], list(T.TRADE_NATURE), format_func=T.TRADE_NATURE.get,
                  key="trade_nature", on_change=reset_trade)
build = st.pills(C["choose_build"], list(T.TRADE_BUILD), format_func=T.TRADE_BUILD.get,
                 key="trade_build", on_change=reset_trade)

if st.button(C["build"], type="primary", disabled=not (nature and build), **ui.stretch(st.button)):
    st.session_state.trade_built = True
    st.session_state.trade_undo = False

if not (nature and build):
    st.info(C["pick_first"])
elif st.session_state.trade_built:
    result = games.trade(biomes, lost, nature, build)
    with ui.card():
        ui.md(C["result_title"])
        if result["gain_estimated"]:
            ui.md(C["gain_farm"].format(value=ui.usd(result["gain"])))
            st.caption(" · ".join(
                f"{row.emoji} {row.service} {ui.usd(row.value_per_ha)}"
                for row in result["built_services"].itertuples()
            ).replace("$", r"\$"))
        else:
            ui.md(C["gain_city"])
        ui.md(C["lose"].format(value=ui.usd(result["loss"])))
        ui.md(C["lost_heading"])
        st.markdown("\n".join(
            ui.esc(f"- ~~{row.emoji} {row.service} — about {ui.usd(row.value_per_ha)}~~")
            for row in result["lost_services"].itertuples()
        ))

    area = st.segmented_control(C["how_big"], list(T.TRADE_AREAS), format_func=T.TRADE_AREAS.get,
                                default=1, key="trade_area")
    area = area or 1
    big = games.trade(biomes, lost, nature, build, area_ha=area)
    pitches = area * config.PITCHES_PER_HA
    ui.md(C["how_big_text"].format(pitches=f"{pitches:,.1f}".removesuffix(".0"), value=ui.usd(big["loss"])))

    if st.button(C["undo"], **ui.stretch(st.button)):
        st.session_state.trade_undo = True
    if st.session_state.trade_undo:
        st.warning(C["undo_text"])

ui.remember(C["remember"])
with ui.more():
    ui.md(C["more"])
    st.caption("Source: Costanza et al. (1997), Table 2.")

ui.nav_buttons(N)
