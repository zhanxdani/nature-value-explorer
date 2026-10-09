import streamlit as st

from content import texts as T
from utils import games, ui

N = 4
C = T.CH4

if "tip_game" not in st.session_state:
    st.session_state.tip_game = games.new_tipping_game()


def clear() -> None:
    st.session_state.tip_game = games.clear_patch(st.session_state.tip_game)


def stop() -> None:
    st.session_state.tip_game = games.stop_game(st.session_state.tip_game)


def restart() -> None:
    st.session_state.tip_game = games.new_tipping_game()


ui.chapter_header(N)
ui.learn(C["learn"])

ui.play(C["play"])
ui.model_badge(C["badge"])
ui.md(C["intro"])

game = st.session_state.tip_game
playing = game["status"] == "playing"

grid = "".join(f"<span>{e}</span>" for e in games.forest_grid(game))
st.markdown(f'<div class="forest-grid">{grid}</div>', unsafe_allow_html=True)

money = games.money_from_farms(game)
services = games.services_left(game)
ui.bar(C["money"], f"+{money}", money / games.TIP_PATCHES, ui.BLUE)
ui.bar(C["services"], f"{services}%", services / 100,
       ui.GREEN if services > 50 else ui.RED)

if playing:
    st.button(C["clear"], on_click=clear, type="primary", **ui.stretch(st.button))
    st.button(C["stop"], on_click=stop, **ui.stretch(st.button))
else:
    if game["status"] == "collapsed":
        st.error(f"## {C['collapse']}")
        ui.md(C["collapse_text"])
    else:
        st.success(C["win"])
    ui.md(C["edge"].format(threshold=game["threshold"], cleared=game["cleared"]))
    st.button(C["play_again"], on_click=restart, type="primary", **ui.stretch(st.button))
    st.caption(C["play_again_hint"])

ui.remember(C["remember"])
with ui.more():
    for line in C["more"]:
        ui.md(line)

ui.nav_buttons(N)
