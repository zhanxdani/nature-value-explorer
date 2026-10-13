"""Shared screen components, router, dialogs and mobile CSS.

Every screen follows the same template (top to bottom):
top_bar → scene → slider → result_line → meters → approval_row → nav_bar (fixed at the bottom).
Anything that does not fit on a phone screen goes into a dialog.
"""

from __future__ import annotations

import re
from html import escape
from io import BytesIO

import qrcode
import streamlit as st

import screens
from content import rules as R
from content import texts as T
from utils import games, img

GREEN = "#2E7D32"
AMBER = "#F9A825"
RED = "#C62828"
GREY = "#BDBDBD"

CSS = """
<style>
/* ---- page frame: no header, tight spacing, room for the fixed nav bar ---- */
:root { --nav-h: 72px; }
[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] { display: none !important; }
[data-testid="stMain"] { padding: 0 !important; }
/* The screen is centered horizontally (max 640px) and vertically in the free space above the nav bar. */
[data-testid="stMainBlockContainer"], .block-container {
    padding: 0.5rem 0.75rem calc(var(--nav-h) + 8px) 0.75rem !important; max-width: 640px;
    margin-left: auto !important; margin-right: auto !important;
    min-height: 100vh; min-height: 100dvh; height: auto !important;
    display: flex !important; flex-direction: column !important; flex-shrink: 0 !important;
    box-sizing: border-box !important;
}
/* "Safe" vertical centering: auto margins center the screen, but a screen taller than the phone
   starts at the top and scrolls instead of being cut off at the top. */
[data-testid="stMainBlockContainer"] > *, .block-container > * {
    margin-top: auto !important; margin-bottom: auto !important; width: 100%;
}
[data-testid="stMain"] [data-testid="stVerticalBlock"] { gap: 0.3rem; }
[data-testid="stMarkdownContainer"] { margin-bottom: 0 !important; }
[data-testid="stMarkdownContainer"] p { margin-bottom: 0; }
html, body { overflow-x: hidden; }
.stButton button { min-height: 44px; }

/* ---- top bar ---- */
.st-key-topbar { min-height: 44px; flex-wrap: nowrap !important; }
.st-key-topbar .stButton button { min-height: 40px; padding: 0 6px; }
.st-key-topbar [data-testid="stElementContainer"]:has(.tb) { flex: 1 1 auto; min-width: 0; }
.tb { min-width: 0; line-height: 1.2; }
.tb-sub { display: flex; justify-content: space-between; gap: 6px; font-size: 0.75rem; color: #5f6368; }
.tb-ch { overflow: hidden; white-space: nowrap; text-overflow: ellipsis; }
.tb-dots { flex-shrink: 0; color: #2E7D32; letter-spacing: 1px; }
.tb-title { font-weight: 700; font-size: 1.05rem; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; }

/* ---- scene ---- */
.scene { position: relative; height: clamp(110px, 23vh, 240px); border-radius: 14px; overflow: hidden;
         background: #E8F5E9; }
.scene img { width: 100%; height: 100%; object-fit: cover; display: block; animation: fadein 0.4s ease; }
.scene .fallback, .card-pic .fallback {
    width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;
    font-size: clamp(2.5rem, 10vh, 4.5rem); animation: fadein 0.4s ease;
}
.scene .overlay { position: absolute; right: 8px; bottom: 6px; width: 64px; }
.scene .overlay .avatar-pic { width: 58px; height: 58px; background: #fff; }
.scene .overlay .avatar-pic .fallback { font-size: 1.9rem; }
.scene .overlay .avatar-name { display: none; }
.scene .overlay .avatar-pct { background: rgba(255, 255, 255, 0.85); border-radius: 6px; }
.scene .caption { position: absolute; left: 0; right: 0; top: 0; padding: 6px 10px;
                  background: rgba(255, 255, 255, 0.88); font-size: 0.85rem; line-height: 1.25; }
@keyframes fadein { from { opacity: 0; } to { opacity: 1; } }
.card-pic { aspect-ratio: 1 / 1; width: 100%; border-radius: 14px; overflow: hidden; background: #E8F5E9; }
.card-pic img { width: 100%; height: 100%; object-fit: cover; display: block; animation: fadein 0.4s ease; }
.card-pic.short { aspect-ratio: auto; height: clamp(100px, 22vh, 200px); }
.card-pic.tall { aspect-ratio: auto; height: clamp(150px, 38vh, 320px); }
.card-title { font-weight: 800; font-size: 1.15rem; line-height: 1.25; }
.st-key-qr img { width: min(80vw, 60vh); height: auto; }

/* ---- one-line texts ---- */
.story { font-size: 0.92rem; line-height: 1.3; }
.result { font-weight: 700; padding: 0.3rem 0.6rem; border-radius: 8px; border-left: 5px solid;
          font-size: 0.92rem; line-height: 1.3; }
.result.success { background: #E8F5E9; border-color: #2E7D32; color: #1B5E20; }
.result.warning { background: #FFF8E1; border-color: #F9A825; color: #6D4C00; }
.result.error { background: #FFEBEE; border-color: #C62828; color: #8E0000; }
.result.info { background: #E3F2FD; border-color: #1565C0; color: #0D47A1; }
.small-fact { font-size: 0.78rem; color: #5f6368; line-height: 1.25; }
.model-badge { display: inline-block; font-size: 0.72rem; padding: 1px 8px; border-radius: 999px;
               background: #FFF3CD; color: #5D4200; border: 1px solid #F0C36D; }
.slider-label { font-weight: 600; font-size: 0.92rem; }
[class*="st-key-row_label"] { align-items: center; min-height: 32px; }
[class*="st-key-row_label"] .stButton button { min-height: 32px; padding: 0 4px; }
[class*="st-key-row_label"] > div:has(.slider-label) { flex: 1 1 auto; }
[class*="st-key-row_label"] > div:has(.stButton) { flex: 0 0 auto; }

/* ---- meters ---- */
[data-testid="stMarkdownContainer"] p:has(> .m-track) {
    display: flex; align-items: center; gap: 6px; font-size: 0.88rem; line-height: 1.2;
}
.m-label { flex: 0 0 40%; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.m-track { flex: 1 1 auto; height: 10px; background: #EEEEEE; border-radius: 5px; overflow: hidden; }
.m-fill { display: block; height: 100%; border-radius: 5px; }
.m-val { flex: 0 0 auto; min-width: 3.4em; text-align: right; font-weight: 700; }

/* ---- approval row ---- */
.st-key-approval { flex-wrap: nowrap !important; align-items: flex-end; }
.st-key-approval [data-testid="stElementContainer"]:has(.who) { flex: 1 1 auto; min-width: 0; }
.st-key-approval .stButton button { min-height: 40px; padding: 0 4px; }
.who-label { font-size: 0.7rem; color: #5f6368; font-weight: 700; text-transform: uppercase;
             letter-spacing: 0.03em; }
.avatars { display: flex; gap: 4px; justify-content: space-between; }
.avatar { flex: 1 1 0; min-width: 0; text-align: center; }
.avatar-pic { width: 50px; height: 50px; border-radius: 50%; margin: 0 auto; overflow: hidden;
              border: 3px solid; box-sizing: border-box; background: #F1F8E9;
              display: flex; align-items: center; justify-content: center; }
.avatar-pic img { width: 100%; height: 100%; object-fit: cover; }
.avatar-pic .fallback { font-size: 1.5rem; }
.ring-low { border-color: #C62828; }
.ring-mid { border-color: #F9A825; }
.ring-high { border-color: #2E7D32; }
.avatar-name { font-size: 0.7rem; line-height: 1.1; margin-top: 2px; white-space: nowrap; overflow: hidden;
               text-overflow: ellipsis; }
.avatar-pct { font-size: 0.8rem; font-weight: 700; line-height: 1.1; }

/* ---- sliders: big thumb, space above and below ---- */
[data-testid="stSlider"] { padding: 2px 12px 0 12px; }
[data-testid="stSlider"] div:has(> div > input[type="range"]) {
    width: 28px !important; height: 28px !important; }

/* ---- zone strip (6.1) ---- */
.strip-wrap { position: relative; padding: 3px 0; }
.strip { display: flex; height: 18px; border-radius: 6px; overflow: hidden; }
.strip-marker { position: absolute; top: 0; bottom: 0; width: 5px; margin-left: -2.5px; background: #212121;
                border-radius: 3px; box-shadow: 0 0 0 2px #fff; }
.strip-legend { display: flex; justify-content: space-between; gap: 6px; font-size: 0.72rem; color: #3c4043; }
.strip-legend i { display: inline-block; width: 10px; height: 10px; border-radius: 3px; margin-right: 4px;
                  vertical-align: -1px; }

/* ---- rows that must not stack on phones ---- */
[class*="st-key-row"] { flex-wrap: nowrap !important; }
[class*="st-key-row"] > div { min-width: 0; flex: 1 1 0; }

/* ---- fixed bottom navigation: round ← and → grouped in the center of the screen ---- */
.st-key-navbar {
    position: fixed !important; bottom: 0; left: 0; right: 0; z-index: 100; background: #FFFFFF;
    box-shadow: 0 -2px 12px rgba(0, 0, 0, 0.08);
    flex-wrap: nowrap !important; justify-content: center !important; align-items: center !important;
    gap: 16px !important; margin: 0 !important; box-sizing: border-box !important;
    min-height: var(--nav-h);
    padding: 8px 16px calc(8px + env(safe-area-inset-bottom, 0px)) !important;
}
.st-key-navbar > * { flex: 0 0 auto !important; width: auto !important; min-width: 0 !important; }
.st-key-navbar [data-testid="stElementContainer"]:has(.nav-dots) { min-width: 56px !important; }
.st-key-nav_back, .st-key-nav_next, .st-key-nav_next_off { width: 56px !important; flex: 0 0 56px !important; }
.st-key-nav_back button, .st-key-nav_next button, .st-key-nav_next_off button {
    width: 56px !important; height: 56px !important; min-width: 56px !important; min-height: 56px !important;
    padding: 0 !important; border-radius: 50% !important;
    display: flex !important; align-items: center !important; justify-content: center !important;
    touch-action: manipulation; -webkit-tap-highlight-color: transparent;
}
.st-key-nav_back button { background: #FFFFFF !important; border: 2px solid #2E7D32 !important; color: #2E7D32 !important; }
.st-key-nav_next button { border: 2px solid #2E7D32 !important; box-shadow: 0 4px 12px rgba(46, 125, 50, 0.35); }
.st-key-nav_back button p, .st-key-nav_next button p { margin: 0 !important; line-height: 1 !important; }
.st-key-nav_back button [data-testid="stIconMaterial"],
.st-key-nav_next button [data-testid="stIconMaterial"] { font-size: 28px !important; }
.st-key-nav_back button:active, .st-key-nav_next button:active { transform: scale(0.94); }
.st-key-nav_back button:disabled, .st-key-nav_next button:disabled { opacity: 0.3 !important; box-shadow: none !important; }
.st-key-nav_next_off { visibility: hidden !important; }  /* keeps ← in place when there is no next screen */
.nav-dots { text-align: center; color: #2E7D32; letter-spacing: 3px; font-size: 0.9rem; white-space: nowrap; }

/* ---- tiles (1.1 items, 6.4 actions) ---- */
[class*="st-key-tile_"] button {
    width: 100%; aspect-ratio: 1 / 1; min-height: 0; padding: 4px; flex-direction: column; gap: 2px;
    background-size: cover; background-position: center; border-radius: 14px;
}
[class*="st-key-tile_"] button > div,
[class*="st-key-tile_"] button span[data-has-shortcut] { display: flex; flex-direction: column;
                                                          align-items: center; gap: 2px; }
[class*="st-key-tile_"] button p { font-size: 0.72rem; line-height: 1.1; white-space: normal;
                                   overflow-wrap: anywhere; text-align: center; }
.st-key-sol_prev button p, .st-key-sol_next button p { font-size: 1.6rem; line-height: 1; }
[class*="st-key-tile_"] button [data-testid="stIconEmoji"],
[class*="st-key-tile_"] button [data-testid="stIconMaterial"] { font-size: 1.7rem; }

/* ---- welcome, finish, share ---- */
.hero .scene { height: clamp(160px, 38vh, 340px); }
.card-pic.badge { width: clamp(110px, 30vh, 200px); margin: 0 auto; border-radius: 50%; }
.qr-url { font-size: clamp(1.2rem, 5vw, 2.4rem); font-weight: 800; text-align: center; word-break: break-all; }
.welcome-title { font-size: 2rem; font-weight: 800; line-height: 1.15; margin-top: 0.4rem; }
.welcome-sub { font-size: 1.05rem; color: #3c4043; }
.big-score { font-size: 2.6rem; font-weight: 800; text-align: center; line-height: 1.1; }
.center { text-align: center; }
</style>
"""


def inject_css() -> None:
    st.markdown(CSS, unsafe_allow_html=True)


def extra_css(rules: list[str]) -> None:
    """Per-run CSS (e.g. background images or selected borders on tiles)."""
    if rules:
        st.markdown("<style>" + "\n".join(rules) + "</style>", unsafe_allow_html=True)


# ---------------------------------------------------------------- data

@st.cache_data
def biomes():
    return games.load_biomes()


@st.cache_data
def wetland_services():
    return games.load_wetland_services()


# ---------------------------------------------------------------- text helpers

def esc(text: str) -> str:
    """Escape dollar signs so Streamlit markdown does not render them as math."""
    return text.replace("$", r"\$")


def md(text: str) -> None:
    st.markdown(esc(text))


def h(text: str) -> str:
    """Escape text for a raw HTML block and turn **bold** into <b>."""
    safe = escape(text).replace("$", "&#36;")
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", safe)


def html(block: str) -> None:
    st.markdown(block, unsafe_allow_html=True)


# ---------------------------------------------------------------- router

def init_router() -> None:
    """Pick the current screen from session state or the ?s= query parameter."""
    qp = st.query_params
    if qp.get("presenter") == "1":
        st.session_state.presenter = True
    if "screen" not in st.session_state:
        requested = qp.get("s", screens.FIRST)
        st.session_state.screen = requested if requested in screens.ALL_IDS else screens.FIRST
    if qp.get("s") != st.session_state.screen:
        st.query_params["s"] = st.session_state.screen
    st.session_state.setdefault("visited", set()).add(st.session_state.screen)


def current() -> str:
    return st.session_state.screen


def go(sid: str) -> None:
    """Switch screen. Safe to use as a button callback."""
    st.session_state.screen = sid
    st.query_params["s"] = sid
    st.session_state.setdefault("visited", set()).add(sid)


def is_presenter() -> bool:
    return bool(st.session_state.get("presenter", False))


def chapter_done(chapter: int) -> bool:
    visited = st.session_state.get("visited", set())
    return all(sid in visited for sid in screens.chapter_screens(chapter))


def open_next(name: str) -> None:
    """Open a dialog on the next run (a dialog cannot open another dialog directly)."""
    st.session_state.next_dialog = name


# ---------------------------------------------------------------- dialogs

@st.dialog(T.COMMON["learn_title"])
def learn_dialog(sid: str, text: str, extra=None, source: str | None = None) -> None:
    st.markdown(f"**{esc(T.SCREEN_TITLES.get(sid, ''))}**")
    md(text)
    if extra:
        extra()
    if source:
        st.caption(esc(source))


@st.dialog(T.COMMON["why_title"])
def why_dialog(items: list[tuple[str, float, str]]) -> None:
    for key, approval, image in items:
        p = R.PEOPLE[key]
        with st.container(horizontal=True, vertical_alignment="center", key=f"why_{key}"):
            html(img.avatar(image, p["fallback"], approval, p["name"], R.APPROVAL_LOW, R.APPROVAL_HIGH))
            md(f"**{p['name']}** ({p['role']}) — {T.COMMON['cares'].format(cares=p['cares'])}.")
    st.caption(T.COMMON["approval_note"])


@st.dialog(T.COMMON["menu_title"])
def menu_dialog() -> None:
    for ch in screens.chapters():
        tick = "✅" if chapter_done(ch) else "▫️"
        if st.button(f"{tick} {ch} · {T.CHAPTERS[ch]['title']}", key=f"menu_{ch}", type="tertiary"):
            go(screens.first_screen(ch))
            st.rerun()
    st.divider()
    with st.container(horizontal=True, key="row_menu"):
        if st.button(T.MENU["glossary"], icon=":material/menu_book:", key="menu_glossary"):
            open_next("glossary")
            st.rerun()
        if st.button(T.MENU["sources"], icon=":material/library_books:", key="menu_sources"):
            open_next("sources")
            st.rerun()
    with st.container(horizontal=True, key="row_menu2"):
        if st.button(T.MENU["share"], icon=":material/qr_code_2:", key="menu_share"):
            go("share")
            st.rerun()
        if st.button(T.MENU["start"], icon=":material/home:", key="menu_home"):
            go(screens.FIRST)
            st.rerun()


@st.dialog(T.MENU["glossary"])
def glossary_dialog() -> None:
    for term, definition in T.GLOSSARY:
        md(f"**{term}** — {definition}")


@st.dialog(T.MENU["sources"])
def sources_dialog() -> None:
    for ref in T.SOURCES["refs"]:
        st.markdown(f"- {esc(ref)}")
    st.caption(T.SOURCES["note"])


@st.dialog(T.COMMON["notes_title"])
def notes_dialog(chapter: int) -> None:
    md(T.SPEAKER_NOTES.get(chapter, ""))


def run_pending_dialog() -> None:
    name = st.session_state.pop("next_dialog", None)
    if name == "glossary":
        glossary_dialog()
    elif name == "sources":
        sources_dialog()


# ---------------------------------------------------------------- screen template

def top_bar(sid: str, learn: str | None = None, learn_extra=None, learn_source: str | None = None) -> None:
    ch = screens.chapter_of(sid)
    dots = "".join("●" if c <= ch else "○" for c in screens.chapters())
    sub = f"Chapter {ch} · {T.CHAPTERS[ch]['title']}"
    with st.container(key="topbar", horizontal=True, vertical_alignment="center", gap="small"):
        if st.button(":material/menu:", key="tb_menu", type="tertiary"):
            menu_dialog()
        html(
            f'<div class="tb"><div class="tb-sub"><span class="tb-ch">{h(sub)}</span>'
            f'<span class="tb-dots">{dots}</span></div>'
            f'<div class="tb-title">{h(T.SCREEN_TITLES[sid])}</div></div>'
        )
        if is_presenter() and st.button(":material/mic:", key="tb_notes", type="tertiary"):
            notes_dialog(ch)
        if learn and st.button(":material/info:", key="tb_info", type="tertiary"):
            learn_dialog(sid, learn, learn_extra, learn_source)


def scene(name: str, fallback: str, overlay: str = "", caption: str | None = None) -> None:
    """Scene picture; `caption` is a short story line laid over the top of the picture."""
    if caption:
        overlay = f'<div class="caption">{h(caption)}</div>' + overlay
    html(img.scene(name, fallback, overlay))


def story(text: str) -> None:
    html(f'<div class="story">{h(text)}</div>')


def slider_label(text: str) -> None:
    html(f'<div class="slider-label">{h(text)}</div>')


def result_line(text: str, tone: str = "info") -> None:
    html(f'<div class="result {tone}">{h(text)}</div>')


def small_fact(text: str) -> None:
    html(f'<div class="small-fact">{h(text)}</div>')


def model_badge() -> None:
    html(f'<span class="model-badge">{h(T.COMMON["model_badge"])}</span>')


def _tone_color(goodness: float) -> str:
    if goodness > R.APPROVAL_HIGH:
        return GREEN
    if goodness >= R.APPROVAL_LOW:
        return AMBER
    return RED


def meter(icon: str, label: str, value_pct: float, value_text: str, good_high: bool = True) -> None:
    """Thin consequence bar: green when good, red when bad, value always written out."""
    pct = max(0.0, min(100.0, value_pct))
    color = _tone_color(pct if good_high else 100 - pct)
    st.markdown(
        f'{icon}<span class="m-label">&nbsp;{h(label)}</span>'
        f'<span class="m-track"><span class="m-fill" style="width:{pct:.0f}%;background:{color}"></span></span>'
        f'<span class="m-val">{h(value_text)}</span>',
        unsafe_allow_html=True,
    )


def approval_row(people: list[str], approvals: list[float], images: dict[str, str] | None = None) -> None:
    """Row of avatars with approval rings, and a Why? button that explains each one."""
    images = images or {}
    items = [(key, a, images.get(key, R.PEOPLE[key]["image"])) for key, a in zip(people, approvals)]
    avatars = "".join(
        img.avatar(image, R.PEOPLE[key]["fallback"], a, R.PEOPLE[key]["name"], R.APPROVAL_LOW, R.APPROVAL_HIGH)
        for key, a, image in items
    )
    with st.container(key="approval", horizontal=True, gap="small"):
        html(f'<div class="who"><div class="who-label">{h(T.COMMON["who_approves"])}</div>'
             f'<div class="avatars">{avatars}</div></div>')
        if st.button(T.COMMON["why"], key="why_btn", type="tertiary", icon=":material/chevron_right:",
                     icon_position="right"):
            why_dialog(items)


def nav_bar(sid: str, show_next: bool = True) -> None:
    """Fixed bottom bar: round ← and → in the center of the screen, chapter dots between them.

    The group always stays centered: a missing previous screen greys ← out, `show_next=False`
    greys → out, and on the last screen an invisible placeholder keeps ← in place.
    """
    prev, nxt = screens.neighbour(sid, -1), screens.neighbour(sid, 1)
    ch = screens.chapter_of(sid)
    dots = ""
    if ch is not None:
        dots = "".join("●" if s == sid else "○" for s in screens.chapter_screens(ch))
    with st.container(key="navbar", horizontal=True, vertical_alignment="center"):
        st.button(":material/arrow_back:", key="nav_back", on_click=go, args=(prev,),
                  disabled=prev is None)
        html(f'<div class="nav-dots">{dots}</div>')
        if nxt:
            st.button(":material/arrow_forward:", key="nav_next", type="primary", on_click=go,
                      args=(nxt,), disabled=not show_next)
        else:
            st.button(":material/arrow_forward:", key="nav_next_off", disabled=True)


def qr_png(url: str) -> bytes:
    image = qrcode.make(url, box_size=10, border=2)
    buf = BytesIO()
    image.save(buf, format="PNG")
    return buf.getvalue()
