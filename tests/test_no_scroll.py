"""Playwright: no screen scrolls on phone sizes, in any game state or with a dialog open.

Needs `pip install playwright` and `python -m playwright install chromium`; skipped otherwise.
"""

import sys
from pathlib import Path

import pytest

sync_api = pytest.importorskip("playwright.sync_api")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from measure import measure, streamlit_server, wait_ready  # noqa: E402

import screens  # noqa: E402

SIZES = [(375, 667), (390, 844)]


def click(page, selector: str) -> None:
    page.click(selector)
    wait_ready(page)


def slider_key(page, container: str, key: str, times: int = 1) -> None:
    handle = page.locator(f"{container} input[type='range']").first
    handle.focus()
    for _ in range(times):
        handle.press(key)
        page.wait_for_timeout(60)
    handle.blur()
    wait_ready(page)


# State name -> (screen, steps to reach it)
STATES = {
    "1.1 items picked": ("1.1", lambda p: [click(p, f".st-key-tile_{k} button") for k in ("coffee", "medicine", "hike")]),
    "1.2 no pollinators": ("1.2", lambda p: slider_key(p, ".st-key-bees", "End")),
    "2.1 after reveal": ("2.1", lambda p: click(p, ".st-key-reveal button")),
    "2.2 answered": ("2.2", lambda p: click(p, ".st-key-hl_swamp button")),
    "3.1 after storm": ("3.1", lambda p: (slider_key(p, ".st-key-wetland", "End"), click(p, ".st-key-storm_btn button"))),
    "4.1 collapse": ("4.1", lambda p: slider_key(p, ".st-key-cleared", "End")),
    "4.1 sliding back": ("4.1", lambda p: (slider_key(p, ".st-key-cleared", "End"),
                                           slider_key(p, ".st-key-cleared", "ArrowLeft", 6))),
    "5.1 answered": ("5.1", lambda p: click(p, ".st-key-gb_0 button")),
    "5.2 answered": ("5.2", lambda p: click(p, ".st-key-bridge_2 button")),
    "5.3 sacred forest": ("5.3", lambda p: slider_key(p, ".st-key-who", "End")),
    "6.1 win-win": ("6.1", lambda p: slider_key(p, ".st-key-offer", "ArrowRight", 20)),
    "6.1 no win-win story": ("6.1", lambda p: (click(p, ".st-key-change_story button"),
                                               p.get_by_text("Northern forest").click(), wait_ready(p),
                                               click(p, "[role='dialog'] button[kind='primary']"))),
    "6.2 all nature": ("6.2", lambda p: slider_key(p, ".st-key-coast", "End")),
    "6.4 ally": ("6.4", lambda p: [click(p, f".st-key-tile_{k} button") for k in ("plants", "bike", "reuse")]),
    "7.1 checked": ("7.1", lambda p: (p.get_by_text("Weather forecasts").click(), wait_ready(p),
                                      click(p, ".st-key-quiz_check button"))),
    "dialog learn": ("6.1", lambda p: click(p, ".st-key-tb_info button")),
    "dialog why": ("3.1", lambda p: click(p, ".st-key-why_btn button")),
    "dialog menu": ("4.1", lambda p: click(p, ".st-key-tb_menu button")),
    "dialog notes": ("5.3&presenter=1", lambda p: click(p, ".st-key-tb_notes button")),
}


@pytest.fixture(scope="module")
def server():
    with streamlit_server() as url:
        yield url


@pytest.fixture(scope="module")
def browser():
    with sync_api.sync_playwright() as p:
        try:
            b = p.chromium.launch()
        except Exception as exc:  # Chromium not installed
            pytest.skip(f"Chromium not available: {exc}")
        yield b
        b.close()


@pytest.fixture(params=SIZES, ids=lambda s: f"{s[0]}x{s[1]}")
def page(request, browser):
    w, h = request.param
    pg = browser.new_page(viewport={"width": w, "height": h})
    yield pg
    pg.close()


def assert_fits(page, label: str) -> None:
    m = measure(page)
    assert m["over"] <= 2, f"{label}: scrolls by {m['over']}px"
    assert m["wide"] <= 0, f"{label}: horizontal scroll {m['wide']}px"


@pytest.mark.parametrize("sid", screens.ALL_IDS)
def test_screen_fits(server, page, sid):
    page.goto(f"{server}/?s={sid}")
    wait_ready(page)
    assert_fits(page, sid)


LAYOUT_JS = """() => {
  const box = s => { const e = document.querySelector(s); if (!e) return null;
    const b = e.getBoundingClientRect(); return {x: b.x, w: b.width, h: b.height, cy: b.y + b.height / 2}; };
  const back = box('.st-key-nav_back button');
  const next = box('.st-key-nav_next button') || box('.st-key-nav_next_off button');
  const nav = document.querySelector('.st-key-navbar');
  const block = document.querySelector('[data-testid="stMainBlockContainer"]');
  const limit = nav ? nav.getBoundingClientRect().top : innerHeight;
  const rects = [...block.querySelectorAll('[data-testid="stElementContainer"]')]
    .filter(e => !(nav && nav.contains(e)))
    .map(e => e.getBoundingClientRect())
    .filter(r => r.width > 0 && r.height > 0);
  const top = Math.min(...rects.map(r => r.top));
  const bottom = Math.max(...rects.map(r => r.bottom));
  return {vw: innerWidth, back, next, above: top, below: limit - bottom};
}"""


@pytest.mark.parametrize("sid", screens.ALL_IDS)
def test_screen_centered(server, page, sid):
    """Round ← / → are centered and thumb-sized; the screen sits in the middle of the free space."""
    page.goto(f"{server}/?s={sid}")
    wait_ready(page)
    m = page.evaluate(LAYOUT_JS)
    back, nxt = m["back"], m["next"]
    if back:
        group_center = (back["x"] + nxt["x"] + nxt["w"]) / 2
        assert abs(group_center - m["vw"] / 2) <= 2, f"{sid}: arrows off-center by {group_center - m['vw'] / 2:.0f}px"
        assert min(back["w"], back["h"], nxt["w"], nxt["h"]) >= 56, f"{sid}: arrow buttons smaller than 56px"
        assert abs(back["cy"] - nxt["cy"]) < 1, f"{sid}: arrows are not in one row"
    if measure(page)["over"] <= 2:
        assert abs(m["above"] - m["below"]) <= 16, (
            f"{sid}: not vertically centered (space above {m['above']:.0f}px, below {m['below']:.0f}px)")


@pytest.mark.parametrize("state", list(STATES))
def test_state_fits(server, page, state):
    sid, steps = STATES[state]
    page.goto(f"{server}/?s={sid}")
    wait_ready(page)
    steps(page)
    assert_fits(page, state)
