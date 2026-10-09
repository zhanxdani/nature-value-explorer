"""Screen order and lookup. Each screen is a module with a `render()` function."""

from __future__ import annotations

import importlib

# The journey, in order. The id is shown in the URL as ?s=<id>.
ORDER = [
    ("0", "s0_welcome"),
    ("1.1", "s1_1_morning"),
    ("1.2", "s1_2_bees"),
    ("2.1", "s2_1_guess"),
    ("2.2", "s2_2_higher_lower"),
    ("3.1", "s3_1_wetland"),
    ("4.1", "s4_1_tipping"),
    ("5.1", "s5_1_good_bad"),
    ("5.2", "s5_2_bridge"),
    ("5.3", "s5_3_who_decides"),
    ("6.1", "s6_1_save_forest"),
    ("6.2", "s6_2_coast"),
    ("6.3", "s6_3_solutions"),
    ("6.4", "s6_4_actions"),
    ("7.1", "s7_1_quiz"),
    ("7.2", "s7_2_finish"),
]
# Screens outside the journey
EXTRA = [("share", "s_share")]

IDS = [sid for sid, _ in ORDER]
ALL_IDS = IDS + [sid for sid, _ in EXTRA]
_MODULES = dict(ORDER + EXTRA)
FIRST = IDS[0]


def chapter_of(sid: str) -> int | None:
    """Chapter number of a screen id ("3.1" -> 3); None for the welcome and extra screens."""
    head = sid.split(".")[0]
    return int(head) if "." in sid and head.isdigit() else None


def chapter_screens(chapter: int) -> list[str]:
    return [sid for sid in IDS if chapter_of(sid) == chapter]


def first_screen(chapter: int) -> str:
    return chapter_screens(chapter)[0]


def chapters() -> list[int]:
    return sorted({c for c in map(chapter_of, IDS) if c is not None})


def neighbour(sid: str, step: int) -> str | None:
    if sid not in IDS:
        return None
    i = IDS.index(sid) + step
    return IDS[i] if 0 <= i < len(IDS) else None


def module(sid: str):
    return importlib.import_module(f"screens.{_MODULES[sid]}")
