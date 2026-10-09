import streamlit as st

from content import texts as T
from utils import ui

SID = "7.1"
X = T.QUIZ
QUESTIONS = X["questions"]


def check(choice: str) -> None:
    st.session_state.quiz_checked = True
    if choice == QUESTIONS[st.session_state.quiz_idx]["answer"]:
        st.session_state.quiz_score += 1


def next_question() -> None:
    st.session_state.quiz_idx += 1
    st.session_state.quiz_checked = False
    if st.session_state.quiz_idx >= len(QUESTIONS):
        ui.go("7.2")


def render() -> None:
    for key, default in (("quiz_idx", 0), ("quiz_score", 0), ("quiz_checked", False)):
        st.session_state.setdefault(key, default)
    idx = min(st.session_state.quiz_idx, len(QUESTIONS) - 1)
    q = QUESTIONS[idx]
    ui.top_bar(SID)
    ui.small_fact(X["progress"].format(n=idx + 1, total=len(QUESTIONS)))
    ui.html(f'<div class="card-title">{ui.h(q["q"])}</div>')
    checked = st.session_state.quiz_checked
    choice = st.radio(ui.esc(q["q"]), q["options"], index=None, key=f"quiz_{idx}", format_func=ui.esc,
                      label_visibility="collapsed", disabled=checked)
    if not checked:
        st.button(X["check"], key="quiz_check", type="primary", disabled=choice is None, on_click=check,
                  args=(choice,), width="stretch")
    else:
        if choice == q["answer"]:
            ui.result_line(f"{X['right']} {q['why']}", "success")
        else:
            ui.result_line(f"{X['wrong'].format(answer=q['answer'])} {q['why']}", "error")
        last = idx == len(QUESTIONS) - 1
        st.button(X["finish"] if last else X["next"], key="quiz_next", type="primary", on_click=next_question,
                  width="stretch")
    ui.nav_bar(SID, show_next=st.session_state.quiz_idx >= len(QUESTIONS))
