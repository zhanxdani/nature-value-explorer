import streamlit as st

from content import texts as T
from utils import ui

N = 5
C = T.CH5
CARDS = T.GOOD_BAD_CARDS
PERSONAS = {p["who"]: p for p in T.PERSONAS}

st.session_state.setdefault("gb_card", 0)
st.session_state.setdefault("persona", None)


def next_card() -> None:
    st.session_state.gb_card += 1


def restart_cards() -> None:
    st.session_state.gb_card = 0


def choose_persona(who: str) -> None:
    st.session_state.persona = who


ui.chapter_header(N)
ui.learn(C["learn"])

# ---------------------------------------------------------------- Play A: good or bad?
ui.play(C["play_a"])
idx = st.session_state.gb_card
if idx < len(CARDS):
    c = CARDS[idx]
    with ui.card():
        st.caption(C["card_of"].format(n=idx + 1, total=len(CARDS)))
        st.markdown(f"## {c['card']}")
        vote = st.segmented_control(C["vote"], C["votes"], key=f"gb_vote_{idx}")
        if vote:
            ui.md(C["heres_the_thing"].format(text=c["text"]))
    if vote:
        st.button(C["next_card"], on_click=next_card, type="primary", **ui.stretch(st.button))
else:
    st.info(C["cards_done"])
    st.button(C["play_again"], on_click=restart_cards, **ui.stretch(st.button))

# ---------------------------------------------------------------- Play B: nature or culture?
ui.play(C["play_b"])
with ui.card():
    ui.md(C["bridge"])
    answer = st.pills("Your answer", C["bridge_options"], key="bridge", label_visibility="collapsed")
    if answer:
        prefix = "🎉 " if answer == C["bridge_options"][-1] else "🤔 "
        ui.md(prefix + C["bridge_answer"])

# ---------------------------------------------------------------- Play C: who decides?
ui.play(C["play_c"])
ui.md(f"**{C['who_intro']}**")
cols = st.columns(2)
for i, who in enumerate(PERSONAS):
    with cols[i % 2]:
        st.button(who, key=f"persona_{i}", on_click=choose_persona, args=(who,),
                  type="primary" if st.session_state.persona == who else "secondary",
                  **ui.stretch(st.button))
if st.session_state.persona:
    p = PERSONAS[st.session_state.persona]
    with ui.card():
        st.markdown(f"**{p['who']}** → **{p['choice']}**")
        ui.md(f"*\"{p['why']}\"*")

mine = st.pills(C["you_choose"], [p["choice"] for p in T.PERSONAS], key="my_choice")
if mine:
    st.info(C["you_answer"])

# ---------------------------------------------------------------- old view vs new view
st.subheader(C["compare_heading"])
for view in (T.OLD_VIEW, T.NEW_VIEW):
    with ui.card():
        st.markdown(f"**{view['title']}**")
        st.markdown("\n".join(f"- {point}" for point in view["points"]))
ui.md(C["ncp_groups"])

ui.remember(C["remember"])
with ui.more():
    ui.md(C["more"])
    st.caption("Source: Díaz et al. (2018), Science 359, 270–272.")

ui.nav_buttons(N)
