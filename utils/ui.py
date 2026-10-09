"""Shared UI components, navigation and mobile-first CSS."""

from __future__ import annotations

import html
import inspect
from io import BytesIO

import qrcode
import streamlit as st

from content import texts as T
from utils import games

PAGES = {
    0: "pages/0_welcome.py",
    1: "pages/1_morning.py",
    2: "pages/2_worth.py",
    3: "pages/3_build_or_keep.py",
    4: "pages/4_tipping_point.py",
    5: "pages/5_contributions.py",
    6: "pages/6_solutions.py",
    7: "pages/7_quiz.py",
}
GLOSSARY_PAGE = "pages/glossary.py"
SOURCES_PAGE = "pages/sources.py"
SHARE_PAGE = "pages/share.py"

GREEN = "#2E7D32"
LIGHT_GREEN = "#81C784"
RED = "#E57373"
GREY = "#BDBDBD"
BLUE = "#1E88E5"

CSS = """
<style>
/* Comfortable reading width and side gutters on phones */
.block-container { padding: 3.5rem 1rem 3rem 1rem; max-width: 760px; }
html, body { overflow-x: hidden; }
[data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] li {
    font-size: 1.05rem; line-height: 1.55;
}

/* Tap-friendly controls: at least 48px high */
.stButton > button, [data-testid="stPageLink"] a { min-height: 48px; }
.stButton > button p { font-size: 1.05rem; }
[data-testid="stButtonGroup"] button { min-height: 44px; }
[data-testid="stButtonGroup"] button p { font-size: 1rem; }
[class*="st-key-big_"] .stButton > button { min-height: 76px; }
[class*="st-key-big_"] .stButton > button p { font-size: 1.2rem; font-weight: 600; }

/* Back / Next stay side by side even on narrow screens */
[class*="st-key-nav"] [data-testid="stHorizontalBlock"] { flex-wrap: nowrap; gap: 0.75rem; }
[class*="st-key-nav"] [data-testid="stColumn"] { min-width: 0; flex: 1 1 0; width: auto; }

/* Badges, bars, grids */
.model-badge {
    display: inline-block; padding: 0.3rem 0.8rem; border-radius: 999px;
    background: #FFF3CD; color: #5D4200; border: 1px solid #F0C36D; font-weight: 600; font-size: 0.95rem;
}
.done-badge {
    display: block; text-align: center; padding: 1rem; border-radius: 16px;
    background: #E8F5E9; color: #1B5E20; border: 2px solid #2E7D32; font-weight: 700; font-size: 1.3rem;
}
.big-number { font-size: 2.2rem; font-weight: 800; line-height: 1.2; margin: 0.25rem 0 0.75rem 0; }
.stat { margin: 0.4rem 0 0.9rem 0; }
.stat-row { display: flex; justify-content: space-between; gap: 0.5rem; font-size: 1.05rem; }
.stat-track { height: 22px; background: #EEEEEE; border-radius: 11px; overflow: hidden; margin-top: 0.25rem; }
.stat-fill { height: 100%; border-radius: 11px; transition: width 0.3s; }
.forest-grid {
    display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.2rem; max-width: 340px;
    margin: 0.5rem auto; text-align: center; font-size: clamp(2.1rem, 11vw, 3rem); line-height: 1.25;
}
.strip-wrap { position: relative; padding-top: 1.9rem; margin: 0.5rem 0 0.25rem 0; }
.strip { display: flex; height: 30px; border-radius: 10px; overflow: hidden; }
.strip-marker {
    position: absolute; top: 0; transform: translateX(-50%); white-space: nowrap;
    font-weight: 700; font-size: 0.95rem;
}
.strip-scale { display: flex; justify-content: space-between; font-size: 0.9rem; color: #555; }
.qr-url { font-size: clamp(1.3rem, 5vw, 2.4rem); font-weight: 800; text-align: center; word-break: break-all; }
</style>
"""


def inject_css() -> None:
    st.markdown(CSS, unsafe_allow_html=True)


# ---------------------------------------------------------------- data

@st.cache_data
def biomes():
    return games.load_biomes()


@st.cache_data
def lost_services():
    return games.load_lost_services()


# ---------------------------------------------------------------- formatting

def esc(text: str) -> str:
    """Escape dollar signs so Streamlit markdown does not render them as math."""
    return text.replace("$", r"\$")


def md(text: str) -> None:
    st.markdown(esc(text))


def html_text(text: str) -> str:
    """Escape text for raw HTML blocks (including $, which markdown would treat as math)."""
    return html.escape(text).replace("$", "&#36;")


def usd(x: float) -> str:
    """Rounded dollars for display: $92, $2,000, $20 million."""
    v = games.nice_round(x)
    if abs(v) >= 1e9:
        return f"${v / 1e9:,.3g} billion"
    if abs(v) >= 1e6:
        return f"${v / 1e6:,.3g} million"
    return f"${v:,.0f}"


def stretch(element) -> dict:
    """Full-width keyword for an element, on both old and new Streamlit versions."""
    if "width" in inspect.signature(element).parameters:
        return {"width": "stretch"}
    return {"use_container_width": True}


# ---------------------------------------------------------------- progress and navigation

def is_presenter() -> bool:
    return bool(st.session_state.get("presenter", False))


def done() -> set[int]:
    if "done" not in st.session_state:
        st.session_state.done = set()
    return st.session_state.done


def mark_done(n: int) -> None:
    done().add(n)


def sync_from_query_params() -> None:
    """Restore presenter mode and finished chapters from the URL (survives a page reload)."""
    qp = st.query_params
    if qp.get("presenter") == "1":
        st.session_state.presenter = True
    for part in qp.get("done", "").split(","):
        if part.isdigit():
            done().add(int(part))


def nav_params() -> dict:
    params = {}
    if done():
        params["done"] = ",".join(str(n) for n in sorted(done()))
    if is_presenter():
        params["presenter"] = "1"
    return params


def go(page: str) -> None:
    st.switch_page(page, query_params=nav_params())


def page_link(page: str, label: str) -> None:
    st.page_link(page, label=label, query_params=nav_params(), **stretch(st.page_link))


def nav_buttons(n: int) -> None:
    st.divider()
    with st.container(key="nav"):
        back_col, next_col = st.columns(2)
        back = n > 0 and back_col.button(T.COMMON["back"], key=f"back_{n}", **stretch(st.button))
        nxt = n < T.LAST_CHAPTER and next_col.button(
            T.COMMON["next"], key=f"next_{n}", type="primary", **stretch(st.button)
        )
    if back:
        go(PAGES[n - 1])
    if nxt:
        mark_done(n)
        go(PAGES[n + 1])


# ---------------------------------------------------------------- chapter building blocks

def chapter_header(n: int) -> None:
    ch = T.CHAPTERS[n]
    st.progress(n / T.LAST_CHAPTER, text=T.COMMON["chapter_of"].format(n=n, total=T.LAST_CHAPTER))
    st.title(f"{ch['emoji']} {ch['title']}")
    if is_presenter() and n in T.SPEAKER_NOTES:
        with st.expander(T.COMMON["speaker_notes"], expanded=True):
            md(T.SPEAKER_NOTES[n])


def learn(text: str) -> None:
    st.subheader(T.COMMON["learn"])
    md(text)


def play(title: str) -> None:
    st.subheader(T.COMMON["play"].format(title=title))


def remember(text: str) -> None:
    st.success(esc(T.COMMON["remember"].format(text=text)))


def more():
    return st.expander(T.COMMON["more"])


def card():
    return st.container(border=True)


def model_badge(text: str) -> None:
    st.markdown(f'<span class="model-badge">{html_text(text)}</span>', unsafe_allow_html=True)


def big_number(text: str) -> None:
    st.markdown(f'<div class="big-number">{html_text(text)}</div>', unsafe_allow_html=True)


def bar(label: str, value: str, fraction: float, color: str = GREEN) -> None:
    """Labelled horizontal bar; the value is always written out, never colour alone."""
    pct = max(0.0, min(1.0, fraction)) * 100
    st.markdown(
        f'<div class="stat"><div class="stat-row"><span>{html_text(label)}</span>'
        f"<b>{html_text(value)}</b></div>"
        f'<div class="stat-track"><div class="stat-fill" style="width:{pct:.1f}%;background:{color}">'
        "</div></div></div>",
        unsafe_allow_html=True,
    )


def color_strip(zones: list[tuple[float, float, str]], marker: float, marker_label: str,
                scale_max: float) -> None:
    """Coloured zones on a 0..scale_max line with a ▼ marker at `marker`."""
    parts = "".join(
        f'<div style="width:{(end - start) / scale_max * 100:.2f}%;background:{color}"></div>'
        for start, end, color in zones
    )
    left = max(6.0, min(94.0, marker / scale_max * 100))
    st.markdown(
        f'<div class="strip-wrap"><div class="strip-marker" style="left:{left:.1f}%">'
        f"▼ {html_text(marker_label)}</div><div class=\"strip\">{parts}</div></div>"
        f'<div class="strip-scale"><span>{html_text(usd(0))}</span>'
        f"<span>{html_text(usd(scale_max))}</span></div>",
        unsafe_allow_html=True,
    )


def qr_png(url: str) -> bytes:
    img = qrcode.make(url, box_size=10, border=2)
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()
