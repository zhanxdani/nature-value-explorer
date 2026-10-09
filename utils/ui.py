"""Shared UI helpers used by every page."""

from __future__ import annotations

import inspect
import math

import pandas as pd
import streamlit as st

import config
from utils import calc

# Chart colors (validated categorical + status palette)
BLUE = "#2a78d6"
ORANGE = "#eb6834"
AQUA = "#1baf7a"
GREY = "#898781"
GOOD = "#0ca30c"
WARNING = "#fab219"
CRITICAL = "#d03b3b"

PLOTLY_CONFIG = {"displayModeBar": False}

COSTANZA = "Costanza, R. et al. (1997). Nature 387, 253–260"
DIAZ = "Díaz, S. et al. (2018). Science 359, 270–272"


# ---------------------------------------------------------------- data

@st.cache_data
def biomes() -> pd.DataFrame:
    return calc.load_biomes()


@st.cache_data
def services() -> pd.DataFrame:
    return calc.load_services()


# ---------------------------------------------------------------- state

def presenter_mode() -> bool:
    return bool(st.session_state.get("presenter", False))


def today_dollars() -> bool:
    return bool(st.session_state.get("today_dollars", False))


def factor() -> float:
    """Multiplier applied to every displayed amount (1994 $ -> today's $)."""
    return config.CPI_FACTOR if today_dollars() else 1.0


def currency_label() -> str:
    return "today's US$ (2024)" if today_dollars() else "US$ (1994)"


# ---------------------------------------------------------------- formatting

def _short(v: float) -> str:
    if v >= 100:
        return f"{v:.1f}"
    if v >= 10:
        return f"{v:.2f}"
    return f"{v:.3f}"


def money(x: float, convert: bool = True) -> str:
    """Format a 1994-US$ amount, converted to today's dollars if the toggle is on."""
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "n/a"
    if math.isinf(x):
        return "∞"
    if convert:
        x = x * factor()
    sign = "−" if x < 0 else ""
    a = abs(x)
    if a >= 1e12:
        return f"{sign}${_short(a / 1e12)} T"
    if a >= 1e9:
        return f"{sign}${_short(a / 1e9)} bn"
    if a >= 1e6:
        return f"{sign}${_short(a / 1e6)} M"
    if a < 100 and a != round(a):
        return f"{sign}${a:,.1f}"
    return f"{sign}${a:,.0f}"


def axis_unit(max_value: float) -> tuple[float, str]:
    """Divisor and unit name so chart axes show readable numbers."""
    for div, name in [(1e12, "trillion"), (1e9, "billion"), (1e6, "million"), (1e3, "thousand")]:
        if max_value >= div:
            return div, name
    return 1.0, ""


def esc(text: str) -> str:
    """Escape dollar signs so Streamlit markdown does not render them as LaTeX."""
    return text.replace("$", r"\$")


# ---------------------------------------------------------------- page building blocks

def header(title: str, what: str) -> None:
    st.title(title)
    st.markdown(f"**What you'll see:** {what}")


def takeaway(text: str) -> None:
    st.success(f"**Takeaway:** {esc(text)}", icon="💡")


def speaker_notes(notes: list[str]) -> None:
    if presenter_mode():
        return
    with st.expander("Speaker notes"):
        st.markdown("\n".join(f"- {esc(n)}" for n in notes))


def source_footer(text: str = COSTANZA) -> None:
    if presenter_mode():
        return
    st.caption(f"Source: {text}")


def illustrative_badge() -> None:
    st.markdown(
        '<span class="illustrative-badge">⚠ Illustrative model — not data from the paper</span>',
        unsafe_allow_html=True,
    )


def stretch(element) -> dict:
    """Full-width keyword for an element, on both old and new Streamlit versions."""
    if "width" in inspect.signature(element).parameters:
        return {"width": "stretch"}
    return {"use_container_width": True}


def chart(fig) -> None:
    """Full-width Plotly chart with shared styling."""
    fig.update_layout(font=dict(size=15))
    if fig.layout.margin.t is None:
        fig.update_layout(margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig, config=PLOTLY_CONFIG, **stretch(st.plotly_chart))
