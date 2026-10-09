"""AppTest smoke tests: every screen renders via ?s=..., also with ?presenter=1 and with no images."""

from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

import screens
from utils import img

ROOT = Path(__file__).resolve().parent.parent
APP = str(ROOT / "app.py")


@pytest.fixture
def no_images(tmp_path, monkeypatch):
    monkeypatch.setattr(img, "IMG_DIR", tmp_path)


def open_screen(sid: str, presenter: bool = False) -> AppTest:
    at = AppTest.from_file(APP, default_timeout=60)
    at.query_params["s"] = sid
    if presenter:
        at.query_params["presenter"] = "1"
    at.run()
    assert not at.exception, at.exception
    return at


def html(at: AppTest) -> str:
    return " ".join(m.value for m in at.markdown)


@pytest.mark.parametrize("sid", screens.ALL_IDS)
@pytest.mark.parametrize("presenter", [False, True], ids=["student", "presenter"])
def test_screen_renders_without_images(sid, presenter, no_images):
    at = open_screen(sid, presenter)
    assert at.session_state["screen"] == sid
    assert 'class="fallback"' in html(at) or sid in ("1.1", "6.4", "7.1", "share")


@pytest.mark.parametrize("sid", screens.ALL_IDS)
def test_screen_renders_with_images(sid):
    open_screen(sid)


def test_unknown_screen_falls_back_to_welcome():
    assert open_screen("nope").session_state["screen"] == screens.FIRST


def test_next_button_moves_on():
    at = open_screen("1.1")
    at.button(key="nav_next").click().run()
    assert at.session_state["screen"] == "1.2"
    assert at.query_params["s"] == ["1.2"] or at.query_params["s"] == "1.2"


def test_presenter_sees_notes_button_students_do_not():
    assert not [b for b in open_screen("3.1").button if b.key == "tb_notes"]
    assert [b for b in open_screen("3.1", presenter=True).button if b.key == "tb_notes"]


def test_wetland_storm_floods_when_drained():
    at = open_screen("3.1")
    at.select_slider(key="wetland").set_value("All").run()
    at.button(key="storm_btn").click().run()
    assert not at.exception
    assert "village floods" in html(at)


def test_tipping_collapse_and_sliding_back():
    at = open_screen("4.1")
    t = at.session_state["tip_game"]["T"]
    at.slider(key="cleared").set_value(100).run()
    assert at.session_state["tip_game"]["state"] == "collapsed"
    assert f"Collapse at {t}%" in html(at)
    at.slider(key="cleared").set_value(t - 5).run()
    assert "Sliding back" in html(at)
    at.slider(key="cleared").set_value(0).run()
    assert at.session_state["tip_game"]["state"] == "recovering"


def test_save_the_forest_cheapest_deal():
    at = open_screen("6.1")
    at.slider(key="offer").set_value(300).run()
    assert not at.exception
    assert "cheapest deal" in html(at)


def test_quiz_to_finish():
    from content import texts as T

    at = open_screen("7.1")
    for q in T.QUIZ["questions"]:
        at.radio[0].set_value(q["answer"]).run()
        at.button(key="quiz_check").click().run()
        at.button(key="quiz_next").click().run()
    assert not at.exception
    assert at.session_state["screen"] == "7.2"
    assert "5 / 5" in html(at)
