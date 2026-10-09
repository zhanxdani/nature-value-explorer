import streamlit as st

import config
from utils import calc, ui

services = ui.services()
biomes = ui.biomes()
top_service = services.loc[services["global_value_bn"].idxmax()]
top_biome = biomes.loc[biomes["value_per_ha"].idxmax()]
ratio = calc.nature_vs_gnp(config.TOTAL_AVG_TN, config.WORLD_GNP_1997_TN)

QUESTIONS = [
    {
        "q": "Costanza et al. (1997): average annual value of the world's ecosystem services?",
        "options": ["$3.3T", "$18T", "$33T", "$330T"],
        "answer": "$33T",
        "why": f"Range ${config.TOTAL_LOW_TN}–{config.TOTAL_HIGH_TN}T, about {ratio:.1f}× world GNP.",
    },
    {
        "q": "Which single service was valued highest?",
        "options": ["Food production", "Nutrient cycling", "Recreation", "Climate regulation"],
        "answer": "Nutrient cycling",
        "why": f"About ${top_service['global_value_bn'] / 1000:.0f}T per year.",
    },
    {
        "q": "Which biome has the highest value per hectare?",
        "options": ["Tropical forest", "Open ocean", "Estuaries", "Cropland"],
        "answer": "Estuaries",
        "why": f"About ${round(top_biome['value_per_ha'], -2):,.0f} per ha per year.",
    },
    {
        "q": "Why do the authors call their estimate a *minimum*?",
        "options": [
            "They used inflated prices",
            "Many services are missing and thresholds are ignored",
            "Only oceans were counted",
            "Markets overvalue nature",
        ],
        "answer": "Many services are missing and thresholds are ignored",
        "why": "Some biomes (desert, tundra, ice/rock) and services had no studies, "
        "and the curve near thresholds was not modelled.",
    },
    {
        "q": "What does the NCP approach (Díaz et al. 2018) add?",
        "options": [
            "Only monetary values",
            "The role of culture and indigenous & local knowledge",
            "It removes regulating services",
            "It replaces ecology with economics",
        ],
        "answer": "The role of culture and indigenous & local knowledge",
        "why": "Culture runs through all contributions, and many knowledge systems count.",
    },
    {
        "q": "The three broad groups of NCP are:",
        "options": [
            "Provisioning, regulating, supporting",
            "Regulating, material, non-material",
            "Market, non-market, cultural",
            "Food, water, air",
        ],
        "answer": "Regulating, material, non-material",
        "why": "Provisioning/supporting is the older ecosystem-services language.",
    },
]
PASS_SCORE = len(QUESTIONS) - 1

st.session_state.setdefault("quiz_idx", 0)
st.session_state.setdefault("quiz_score", 0)
st.session_state.setdefault("quiz_checked", False)
st.session_state.setdefault("quiz_correct", False)


def check(choice: str) -> None:
    q = QUESTIONS[st.session_state.quiz_idx]
    st.session_state.quiz_checked = True
    st.session_state.quiz_correct = choice == q["answer"]
    if st.session_state.quiz_correct:
        st.session_state.quiz_score += 1


def next_question() -> None:
    st.session_state.quiz_idx += 1
    st.session_state.quiz_checked = False


def restart() -> None:
    st.session_state.quiz_idx = 0
    st.session_state.quiz_score = 0
    st.session_state.quiz_checked = False


ui.header("Quiz", f"{len(QUESTIONS)} quick questions on both papers. One at a time.")

idx = st.session_state.quiz_idx
if idx < len(QUESTIONS):
    q = QUESTIONS[idx]
    st.progress(idx / len(QUESTIONS), text=f"Question {idx + 1} of {len(QUESTIONS)} · "
                f"Score: {st.session_state.quiz_score}")
    choice = st.radio(
        ui.esc(f"**{q['q']}**"),
        q["options"],
        index=None,
        key=f"quiz_choice_{idx}",
        format_func=ui.esc,
        disabled=st.session_state.quiz_checked,
    )
    if not st.session_state.quiz_checked:
        st.button("Check", type="primary", disabled=choice is None, on_click=check, args=(choice,))
    else:
        if st.session_state.quiz_correct:
            st.success(ui.esc(f"Correct! {q['why']}"))
        else:
            st.error(ui.esc(f"Not quite. The answer is **{q['answer']}**. {q['why']}"))
        last = idx == len(QUESTIONS) - 1
        st.button("See my score" if last else "Next", type="primary", on_click=next_question)
else:
    score = st.session_state.quiz_score
    st.markdown(
        f'<p class="big-text">Your score: {score} / {len(QUESTIONS)}</p>',
        unsafe_allow_html=True,
    )
    if score >= PASS_SCORE:
        st.balloons()
        st.success("Excellent — you know how to value nature!")
    else:
        st.info("Good try! Have another go.")
    st.button("Restart", type="primary", on_click=restart)

ui.source_footer(f"{ui.COSTANZA}; {ui.DIAZ}")
