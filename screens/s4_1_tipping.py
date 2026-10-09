import streamlit as st

from content import rules as R
from content import texts as T
from utils import games, ui

SID = "4.1"
X = T.TIPPING
KEY = "cleared"
FALLBACK = {"scenes/forest_0": "🌳🌳🌳", "scenes/forest_1": "🌳🌾🌳", "scenes/forest_2": "🌾🌳🌾",
            "scenes/forest_3": "🥀🏜️", "scenes/forest_4": "🌱🌱"}


def moved() -> None:
    st.session_state.tip_game = games.update_tipping(st.session_state.tip_game, st.session_state[KEY])


def play_again() -> None:
    st.session_state.tip_game = games.new_tipping_game()
    st.session_state[KEY] = 0


def render() -> None:
    if "tip_game" not in st.session_state:
        st.session_state.tip_game = games.new_tipping_game()
    game = st.session_state.tip_game
    if KEY not in st.session_state:  # coming back to this screen: put the slider where the game is
        st.session_state[KEY] = game["cleared"]

    ui.top_bar(SID, X["learn"])
    with st.container(key="row_label_badge", horizontal=True, vertical_alignment="center"):
        ui.model_badge()
        st.button(T.COMMON["play_again"], key="tip_again", type="tertiary", icon=":material/replay:",
                  on_click=play_again)
    scene = games.tipping_scene(game)
    ui.scene(scene, FALLBACK[scene])
    ui.slider_label(X["slider"])
    st.slider(X["slider"], 0, 100, step=5, format="%d%%", key=KEY, on_change=moved,
              label_visibility="collapsed")
    game = st.session_state.tip_game

    if game["state"] == "collapsed":
        if games.sliding_back(game):
            ui.result_line(X["sliding_back"], "error")
        else:
            ui.result_line(X["collapse"].format(T=game["T"]), "error")
    elif game["state"] == "recovering":
        ui.result_line(X["recovering"], "warning")
    else:
        ui.result_line(X["ok"], "success" if game["cleared"] < 50 else "warning")

    services = games.tipping_services(game)
    income = games.tipping_income(game)
    ui.meter(":material/water_drop:", X["services"], services, f"{services:.0f}%")
    ui.meter(":material/agriculture:", X["income"], income, f"{income:.0f}%")
    ui.approval_row(R.TIPPING["people"], games.tipping_approval(game))
    if game["state"] != "ok":
        ui.small_fact(X["hint"])
    ui.nav_bar(SID)
