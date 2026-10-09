import streamlit as st

import config
from content import texts as T
from utils import games, ui

N = 2
C = T.CH2
ROUNDS = T.HIGHER_LOWER
biomes = ui.biomes()

ui.chapter_header(N)
ui.learn(C["learn"])

# ---------------------------------------------------------------- Play A: guess the price
ui.play(C["play_a"])
guess = st.pills(C["question"], C["options"], key="worth_guess")
if guess:
    with ui.card():
        st.markdown(f"### {C['right'] if guess == C['correct'] else C['wrong']}")
        ui.md(
            C["answer"].format(
                avg=config.TOTAL_AVG_TN, low=config.TOTAL_LOW_TN,
                high=config.TOTAL_HIGH_TN, gnp=config.WORLD_GNP_1997_TN,
            )
        )
        top = max(config.TOTAL_AVG_TN, config.WORLD_GNP_1997_TN)
        ui.bar(C["bar_nature"], f"${config.TOTAL_AVG_TN} trillion", config.TOTAL_AVG_TN / top, ui.GREEN)
        ui.bar(C["bar_economy"], f"${config.WORLD_GNP_1997_TN} trillion",
               config.WORLD_GNP_1997_TN / top, ui.GREY)
        st.caption(C["trillion_note"])

# ---------------------------------------------------------------- Play B: which is worth more?
ui.play(C["play_b"])
ui.md(C["play_b_intro"])

st.session_state.setdefault("hl_round", 0)
st.session_state.setdefault("hl_score", 0)
st.session_state.setdefault("hl_pick", None)


def label(key: str) -> str:
    name = T.SHORT_NAMES.get(key, biomes.loc[key, "name"])
    return f"{biomes.loc[key, 'emoji']} {name}"


def pick(key: str) -> None:
    r = ROUNDS[st.session_state.hl_round]
    st.session_state.hl_pick = key
    if games.guess_is_right(biomes, r["a"], r["b"], key):
        st.session_state.hl_score += 1


def next_round() -> None:
    st.session_state.hl_round += 1
    st.session_state.hl_pick = None


def restart() -> None:
    st.session_state.hl_round = 0
    st.session_state.hl_score = 0
    st.session_state.hl_pick = None


rnd = st.session_state.hl_round
if rnd < len(ROUNDS):
    r = ROUNDS[rnd]
    answered = st.session_state.hl_pick is not None
    st.caption(C["round"].format(n=rnd + 1, total=len(ROUNDS), score=st.session_state.hl_score))
    col_a, col_b = st.columns(2)
    for col, key, slot in [(col_a, r["a"], "a"), (col_b, r["b"], "b")]:
        with col:
            st.button(label(key), key=f"big_hl_{slot}", on_click=pick, args=(key,),
                      disabled=answered, **ui.stretch(st.button))
    if answered:
        right = games.guess_is_right(biomes, r["a"], r["b"], st.session_state.hl_pick)
        with ui.card():
            st.markdown(f"### {C['right_b'] if right else C['wrong_b']}")
            for key in (r["a"], r["b"]):
                ui.md(f"{label(key)}: **about {ui.usd(games.value_per_ha(biomes, key))}** {C['per_ha']}")
            ui.md(r["fact"])
        last = rnd == len(ROUNDS) - 1
        st.button(C["see_score"] if last else C["next_round"], on_click=next_round,
                  type="primary", **ui.stretch(st.button))
else:
    with ui.card():
        ui.md("### " + C["final"].format(score=st.session_state.hl_score, total=len(ROUNDS)))
    st.button(C["play_again"], on_click=restart, **ui.stretch(st.button))

ui.remember(C["remember"])
with ui.more():
    for line in C["more"]:
        ui.md(line)
    st.caption("Source: Costanza et al. (1997), Table 2.")

ui.nav_buttons(N)
