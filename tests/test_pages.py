"""Smoke tests: every page renders without exceptions."""

from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parent.parent
PAGES = sorted((ROOT / "pages").glob("*.py"))
TIMEOUT = 60


def run(path, **state) -> AppTest:
    at = AppTest.from_file(str(path), default_timeout=TIMEOUT)
    for key, value in state.items():
        at.session_state[key] = value
    at.run()
    assert not at.exception, at.exception
    return at


def test_all_pages_found():
    assert len(PAGES) == 7


@pytest.mark.parametrize("page", PAGES, ids=lambda p: p.stem)
@pytest.mark.parametrize("today", [False, True], ids=["1994", "today"])
def test_page_renders(page, today):
    run(page, today_dollars=today)


@pytest.mark.parametrize("presenter", [False, True], ids=["normal", "presenter"])
def test_app_renders(presenter):
    run(ROOT / "app.py", presenter=presenter)


def test_guess_reveal():
    at = run(ROOT / "pages" / "1_guess.py")
    at.button[0].click().run()
    assert not at.exception
    assert any("1.8" in m.value for m in at.metric)


def test_converter_default_loss():
    at = run(ROOT / "pages" / "2_converter.py")
    loss = next(m for m in at.metric if m.label == "Loss per year")
    assert loss.value == "$1.915 bn"


def test_tipping_point_near_threshold():
    at = run(ROOT / "pages" / "4_tipping_point.py")
    at.select_slider[0].set_value(22).run()
    assert not at.exception
    assert len(at.error) == 1


def test_value_lens_investor_preset():
    at = run(ROOT / "pages" / "5_value_lens.py")
    next(b for b in at.button if b.label == "Investor").click().run()
    assert not at.exception
    assert any("Winner for Investor: Oil palm plantation" in m.value for m in at.markdown)


def test_deal_builder_no_deal_for_temperate_forest():
    at = run(ROOT / "pages" / "6_deal_builder.py")
    at.selectbox[0].set_value("Temperate/boreal forest").run()
    assert not at.exception
    assert len(at.warning) == 1


def test_quiz_full_run():
    at = run(ROOT / "pages" / "7_quiz.py")
    answers = [
        "$33T",
        "Nutrient cycling",
        "Estuaries",
        "Many services are missing and thresholds are ignored",
        "The role of culture and indigenous & local knowledge",
        "Regulating, material, non-material",
    ]
    for answer in answers:
        at.radio[0].set_value(answer).run()
        at.button[0].click().run()  # Check
        assert at.success
        at.button[0].click().run()  # Next
    assert not at.exception
    assert any("6 / 6" in m.value for m in at.markdown)
