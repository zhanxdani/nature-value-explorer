import streamlit as st

from content import texts as T
from utils import games, img, ui

SID = "2.2"
X = T.HIGHER_LOWER
ROUNDS = X["rounds"]


def pick(key: str) -> None:
    st.session_state.hl_pick = key
    r = ROUNDS[st.session_state.hl_round]
    if games.guess_is_right(ui.biomes(), r["a"], r["b"], key):
        st.session_state.hl_score += 1


def next_round() -> None:
    st.session_state.hl_round += 1
    st.session_state.hl_pick = None


def restart() -> None:
    st.session_state.hl_round = 0
    st.session_state.hl_score = 0
    st.session_state.hl_pick = None


def render() -> None:
    biomes = ui.biomes()
    for key, default in (("hl_round", 0), ("hl_score", 0), ("hl_pick", None)):
        st.session_state.setdefault(key, default)
    rnd = st.session_state.hl_round
    ui.top_bar(SID, X["learn"])
    dots = "".join("●" if i < rnd else ("◉" if i == rnd else "○") for i in range(len(ROUNDS)))
    ui.html(f'<div class="nav-dots">{dots}</div>')

    if rnd >= len(ROUNDS):
        ui.scene("hero", "🏅")
        ui.result_line(X["final"].format(score=st.session_state.hl_score, total=len(ROUNDS)), "success")
        st.button(T.COMMON["play_again"], key="hl_again", icon=":material/replay:", on_click=restart,
                  width="stretch")
        ui.nav_bar(SID)
        return

    r = ROUNDS[rnd]
    picked = st.session_state.hl_pick
    ui.small_fact(X["hint"])
    with st.container(key="row_hl", horizontal=True, gap="small"):
        for key in (r["a"], r["b"]):
            b = biomes.loc[key]
            with st.container(key=f"hl_card_{key}"):
                ui.html(img.card(b["image"], b["fallback"], "short"))
                label = b["name"]
                if picked:
                    mark = "✅ " if key == games.higher_of(biomes, r["a"], r["b"]) else ""
                    label = f"{mark}{b['name']}"
                st.button(label, key=f"hl_{key}", on_click=pick, args=(key,), disabled=picked is not None,
                          type="primary" if picked == key else "secondary", width="stretch")
    if picked:
        right = games.guess_is_right(biomes, r["a"], r["b"], picked)
        prices = " · ".join(f"{biomes.loc[k, 'name']}: {games.money_about(games.value_per_ha(biomes, k))}"
                            for k in (r["a"], r["b"]))
        ui.result_line(f"{X['right'] if right else X['wrong']} {prices} {T.COMMON['per_ha']}",
                       "success" if right else "error")
        ui.small_fact(r["fact"])
        last = rnd == len(ROUNDS) - 1
        st.button(X["score"] if last else X["next"], key="hl_next", type="primary", on_click=next_round,
                  width="stretch")
    ui.nav_bar(SID)
