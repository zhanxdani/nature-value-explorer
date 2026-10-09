"""Pure game logic. No Streamlit imports here, so everything is easy to test."""

from __future__ import annotations

import random
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


# ---------------------------------------------------------------- data

def load_biomes() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "biomes.csv").set_index("key")


def load_lost_services() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "lost_services.csv")


def value_per_ha(biomes: pd.DataFrame, key: str) -> float:
    return float(biomes.loc[key, "value_per_ha"])


# ---------------------------------------------------------------- rounding for display

def _round_to(x: float, step: float) -> float:
    return float((Decimal(str(x)) / Decimal(str(step))).quantize(Decimal(1), ROUND_HALF_UP) * Decimal(str(step)))


def nice_round(x: float) -> float:
    """Round for "about" numbers: 92 -> 92, 252 -> 250, 2007 -> 2000, 19580 -> 20000."""
    a = abs(x)
    if a < 100:
        return round(x)
    if a < 1_000:
        return _round_to(x, 10)
    digits = len(str(int(a)))
    return _round_to(x, 10 ** (digits - 2))  # two significant figures


# ---------------------------------------------------------------- chapter 2: higher or lower

def higher_of(biomes: pd.DataFrame, a: str, b: str) -> str:
    """Key of the biome with the higher value per hectare."""
    return a if value_per_ha(biomes, a) > value_per_ha(biomes, b) else b


def guess_is_right(biomes: pd.DataFrame, a: str, b: str, pick: str) -> bool:
    return pick == higher_of(biomes, a, b)


# ---------------------------------------------------------------- chapter 3: build or keep

def trade(biomes: pd.DataFrame, lost: pd.DataFrame, nature: str, build: str, area_ha: float = 1) -> dict:
    """What we gain and lose (per year) when `area_ha` of nature is turned into `build`."""
    return {
        "gain": value_per_ha(biomes, build) * area_ha,
        "gain_estimated": build != "urban",
        "loss": value_per_ha(biomes, nature) * area_ha,
        "lost_services": lost[lost["biome_key"] == nature].reset_index(drop=True),
        "built_services": lost[lost["biome_key"] == build].reset_index(drop=True),
    }


# ---------------------------------------------------------------- chapter 4: tipping point

TIP_PATCHES = 20
TIP_MIN, TIP_MAX = 8, 13          # hidden threshold: number of cleared patches that triggers collapse
SERVICE_DROP_PER_PATCH = 3        # % of services lost per cleared patch
SERVICES_AFTER_COLLAPSE = 10      # % of services left after collapse


def new_tipping_game(rng: random.Random | None = None) -> dict:
    rng = rng or random.Random()
    return {"threshold": rng.randint(TIP_MIN, TIP_MAX), "cleared": 0, "status": "playing"}


def clear_patch(game: dict) -> dict:
    """Clear one more patch. Reaching the hidden threshold collapses the forest."""
    if game["status"] != "playing" or game["cleared"] >= TIP_PATCHES:
        return game
    cleared = game["cleared"] + 1
    status = "collapsed" if cleared >= game["threshold"] else "playing"
    return {**game, "cleared": cleared, "status": status}


def stop_game(game: dict) -> dict:
    if game["status"] != "playing":
        return game
    return {**game, "status": "stopped"}


def money_from_farms(game: dict) -> int:
    return game["cleared"]


def services_left(game: dict) -> int:
    """% of nature's services still working."""
    if game["status"] == "collapsed":
        return SERVICES_AFTER_COLLAPSE
    return 100 - SERVICE_DROP_PER_PATCH * game["cleared"]


def forest_grid(game: dict) -> list[str]:
    """One emoji per patch: cleared 🌾, healthy 🌳, dead 🥀 after collapse."""
    standing = "🥀" if game["status"] == "collapsed" else "🌳"
    return ["🌾"] * game["cleared"] + [standing] * (TIP_PATCHES - game["cleared"])


# ---------------------------------------------------------------- chapter 6: save the forest

def deal_outcome(offer: float, farmer_profit: float, services_value: float) -> str:
    """'reject' if the farmer earns more by clearing, 'overpay' if the offer is above the
    services saved, otherwise 'deal'."""
    if offer < farmer_profit:
        return "reject"
    if offer > services_value:
        return "overpay"
    return "deal"
