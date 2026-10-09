import streamlit as st

from content import texts as T
from utils import ui

N = 7
C = T.CH7
QUIZ = T.QUIZ

st.session_state.setdefault("quiz_idx", 0)
st.session_state.setdefault("quiz_score", 0)
st.session_state.setdefault("quiz_checked", False)
st.session_state.setdefault("quiz_correct", False)
st.session_state.setdefault("quiz_celebrated", False)


def check(choice: str) -> None:
    st.session_state.quiz_checked = True
    st.session_state.quiz_correct = choice == QUIZ[st.session_state.quiz_idx]["answer"]
    if st.session_state.quiz_correct:
        st.session_state.quiz_score += 1


def next_question() -> None:
    st.session_state.quiz_idx += 1
    st.session_state.quiz_checked = False


def reset_quiz() -> None:
    st.session_state.quiz_idx = 0
    st.session_state.quiz_score = 0
    st.session_state.quiz_checked = False
    st.session_state.quiz_celebrated = False


ui.chapter_header(N)

idx = st.session_state.quiz_idx
if idx < len(QUIZ):
    q = QUIZ[idx]
    ui.md(C["intro"])
    st.caption(C["question_of"].format(n=idx + 1, total=len(QUIZ), score=st.session_state.quiz_score))
    with ui.card():
        choice = st.radio(
            ui.esc(f"**{q['q']}**"),
            q["options"],
            index=None,
            key=f"quiz_choice_{idx}",
            format_func=ui.esc,
            disabled=st.session_state.quiz_checked,
        )
    if not st.session_state.quiz_checked:
        st.button(C["check"], type="primary", disabled=choice is None, on_click=check, args=(choice,),
                  **ui.stretch(st.button))
    else:
        if st.session_state.quiz_correct:
            st.success(ui.esc(f"{C['right']} {q['why']}"))
        else:
            st.error(ui.esc(f"{C['wrong'].format(answer=q['answer'])} {q['why']}"))
        last = idx == len(QUIZ) - 1
        st.button(C["finish"] if last else C["next"], type="primary", on_click=next_question,
                  **ui.stretch(st.button))
else:
    ui.mark_done(N)
    score = st.session_state.quiz_score
    ui.big_number(C["score"].format(score=score, total=len(QUIZ)))
    st.markdown(f'<div class="done-badge">{ui.html_text(C["badge"])}</div>', unsafe_allow_html=True)
    st.write("")
    if score >= T.QUIZ_BALLOONS_MIN:
        st.success(C["great"])
        if not st.session_state.quiz_celebrated:
            st.balloons()
            st.session_state.quiz_celebrated = True
    else:
        st.info(C["ok"])

    if st.button(C["share"], type="primary", **ui.stretch(st.button)):
        ui.go(ui.SHARE_PAGE)
    if st.button(C["sources"], **ui.stretch(st.button)):
        ui.go(ui.SOURCES_PAGE)
    if st.button(C["restart"], **ui.stretch(st.button)):
        reset_quiz()
        ui.done().clear()
        ui.go(ui.PAGES[0])

ui.nav_buttons(N)
