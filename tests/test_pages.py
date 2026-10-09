"""Smoke tests: every page renders through app.py, with and without ?presenter=1."""

from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from content import texts as T
from utils import ui

ROOT = Path(__file__).resolve().parent.parent
APP = str(ROOT / "app.py")
ALL_PAGES = list(ui.PAGES.values()) + [ui.GLOSSARY_PAGE, ui.SOURCES_PAGE, ui.SHARE_PAGE]
TIMEOUT = 60


def open_page(page: str, presenter: bool = False) -> AppTest:
    at = AppTest.from_file(APP, default_timeout=TIMEOUT)
    if presenter:
        at.query_params["presenter"] = "1"
    at.run()
    at.switch_page(page).run()
    assert not at.exception, at.exception
    return at


def test_every_page_file_exists():
    for page in ALL_PAGES:
        assert (ROOT / page).is_file(), page


@pytest.mark.parametrize("page", ALL_PAGES)
@pytest.mark.parametrize("presenter", [False, True], ids=["student", "presenter"])
def test_page_renders(page, presenter):
    open_page(page, presenter)


@pytest.mark.parametrize("n", range(1, T.LAST_CHAPTER + 1))
def test_speaker_notes_only_for_presenter(n):
    label = T.COMMON["speaker_notes"]
    student = open_page(ui.PAGES[n])
    presenter = open_page(ui.PAGES[n], presenter=True)
    assert not any(e.label == label for e in student.expander)
    assert any(e.label == label for e in presenter.expander)


def test_morning_counter():
    at = open_page(ui.PAGES[1])
    at.pills(key="morning_items").set_value(["☕ Coffee", "🍎 Apple"]).run()
    assert not at.exception
    assert any("2" in m.value and "before lunch" in m.value for m in at.markdown)


def test_higher_lower_full_game():
    at = open_page(ui.PAGES[2])
    for _ in T.HIGHER_LOWER:
        at.button(key="big_hl_b").click().run()  # the second option is always the right one
        assert not at.exception
        next(b for b in at.button if b.label in (T.CH2["next_round"], T.CH2["see_score"])).click().run()
    assert any("5 of 5" in m.value for m in at.markdown)


def test_build_or_keep_trade():
    at = open_page(ui.PAGES[3])
    at.pills(key="trade_nature").set_value("tropical_forest").run()
    at.pills(key="trade_build").set_value("cropland").run()
    next(b for b in at.button if b.label == T.CH3["build"]).click().run()
    assert not at.exception
    text = " ".join(m.value for m in at.markdown)
    assert "2,000" in text and "92" in text


def test_tipping_point_collapse_and_restart():
    at = open_page(ui.PAGES[4])
    for _ in range(20):
        clear = [b for b in at.button if b.label == T.CH4["clear"]]
        if not clear:
            break
        clear[0].click().run()
    assert not at.exception
    assert at.session_state["tip_game"]["status"] == "collapsed"
    next(b for b in at.button if b.label == T.CH4["play_again"]).click().run()
    assert at.session_state["tip_game"]["status"] == "playing"
    assert at.session_state["tip_game"]["cleared"] == 0


def test_save_the_forest_offer():
    at = open_page(ui.PAGES[6])
    at.pills(key="ana_offer").set_value(300).run()
    assert not at.exception
    assert len(at.success) >= 1


def test_quiz_full_run():
    at = open_page(ui.PAGES[7])
    for q in T.QUIZ:
        at.radio[0].set_value(q["answer"]).run()
        next(b for b in at.button if b.label == T.CH7["check"]).click().run()
        assert at.success
        next(b for b in at.button if b.label in (T.CH7["next"], T.CH7["finish"])).click().run()
    assert not at.exception
    assert any("5 / 5" in m.value for m in at.markdown)


def test_next_marks_chapter_done():
    at = open_page(ui.PAGES[1])
    at.button(key="next_1").click().run()
    assert not at.exception
    assert 1 in at.session_state["done"]
