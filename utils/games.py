"""Pure game logic. No Streamlit imports here, so everything is easy to test."""

from __future__ import annotations

import math
import random
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

import pandas as pd

from content import rules as R

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


# ---------------------------------------------------------------- data

def load_biomes() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "biomes.csv").set_index("key")


def load_wetland_services() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "wetland_services.csv")


def value_per_ha(biomes: pd.DataFrame, key: str) -> float:
    return float(biomes.loc[key, "value_per_ha"])


# ---------------------------------------------------------------- rounding and money

def round_half_up(x: float, step: float = 1) -> float:
    q = (Decimal(str(x)) / Decimal(str(step))).quantize(Decimal(1), ROUND_HALF_UP)
    return float(q * Decimal(str(step)))


def nice_round(x: float) -> float:
    """Round for "about" numbers: 92 -> 92, 252 -> 250, 1915 -> 1900, 19580 -> 20000."""
    a = abs(x)
    if a < 100:
        return round_half_up(x)
    if a < 1_000:
        return round_half_up(x, 10)
    digits = len(str(int(a)))
    return round_half_up(x, 10 ** (digits - 2))


def money_about(x: float) -> str:
    """$92, $1,900, $20,000."""
    v = nice_round(x)
    return f"{'-' if v < 0 else ''}${abs(v):,.0f}"


def money_short(x: float) -> str:
    """Compact money: $0, $915, $9k, $30k, $0.66M, $1.96M, $19.8M."""
    sign = "-" if x < 0 else ""
    a = abs(x)
    if a >= 10e6:
        return f"{sign}${a / 1e6:.1f}M"
    if a >= 500_000:
        return f"{sign}${a / 1e6:.2f}M"
    if a >= 1_000:
        return f"{sign}${round_half_up(a / 1e3):.0f}k"
    return f"{sign}${round_half_up(a):.0f}"


# ---------------------------------------------------------------- 2.2 which is worth more?

def higher_of(biomes: pd.DataFrame, a: str, b: str) -> str:
    """Key of the biome with the higher value per hectare."""
    return a if value_per_ha(biomes, a) > value_per_ha(biomes, b) else b


def guess_is_right(biomes: pd.DataFrame, a: str, b: str, pick: str) -> bool:
    return pick == higher_of(biomes, a, b)


# ---------------------------------------------------------------- 3.1 drain the wetland

def wetland_nature_value(biomes: pd.DataFrame, drained: float) -> float:
    """Nature's work per year for everyone: area x ((1-p) x swamp + p x farm field)."""
    w = R.WETLAND
    swamp, farm = value_per_ha(biomes, "swamp"), value_per_ha(biomes, "cropland")
    return w["area_ha"] * ((1 - drained) * swamp + drained * farm)


def wetland_farm_income(drained: float) -> float:
    w = R.WETLAND
    return w["area_ha"] * drained * w["farm_income_per_ha"]


def storm_floods(stop: int) -> bool:
    return stop >= R.WETLAND["storm_floods_from"]


# ---------------------------------------------------------------- 4.1 tipping point

def new_tipping_game(rng: random.Random | None = None) -> dict:
    rng = rng or random.Random()
    return {"T": rng.choice(R.TIPPING["thresholds"]), "state": "ok", "cleared": 0}


def recovery_threshold(game: dict) -> int:
    return game["T"] - R.TIPPING["recovery_gap"]


def update_tipping(game: dict, cleared: int) -> dict:
    """Move the slider to `cleared` %. Collapse at T; after a collapse only going down to
    R = T - 35 brings recovery (hysteresis)."""
    state = game["state"]
    if state in ("ok", "recovering") and cleared >= game["T"]:
        state = "collapsed"
    elif state == "collapsed" and cleared <= recovery_threshold(game):
        state = "recovering"
    return {**game, "state": state, "cleared": cleared}


def tipping_services(game: dict) -> float:
    t = R.TIPPING
    if game["state"] == "collapsed":
        return t["collapsed_services"]
    if game["state"] == "recovering":
        return t["recovering_services"]
    return 100 - t["services_slope"] * game["cleared"]


def tipping_income(game: dict) -> float:
    if game["state"] == "collapsed":
        return R.TIPPING["collapsed_income_factor"] * game["cleared"]
    return game["cleared"]


def tipping_scene(game: dict) -> str:
    t = R.TIPPING
    if game["state"] == "collapsed":
        return t["collapse_scene"]
    if game["state"] == "recovering":
        return t["recovery_scene"]
    return next(scene for limit, scene in t["scene_steps"] if game["cleared"] < limit)


def tipping_approval(game: dict) -> list[float]:
    t = R.TIPPING
    if game["state"] == "collapsed":
        return list(t["collapsed_approval"])
    if game["state"] == "recovering":
        return list(t["recovering_approval"])
    c = game["cleared"]
    return [30 + 0.7 * c, 40 + 0.5 * c, 100 - c, max(0, 100 - 1.3 * c)]


def sliding_back(game: dict) -> bool:
    """Collapsed, and the player has moved back below the threshold (but not far enough)."""
    return game["state"] == "collapsed" and game["cleared"] < game["T"]


# ---------------------------------------------------------------- 5.3 who decides?

def average_approval(approvals: list[float]) -> int:
    return int(round_half_up(sum(approvals) / len(approvals)))


def best_compromise() -> str:
    w = R.WHO_DECIDES
    averages = [average_approval(a) for a in w["approval"]]
    return w["stops"][averages.index(max(averages))]


# ---------------------------------------------------------------- 6.1 save the forest

def forest_value(biomes: pd.DataFrame, story: str) -> float:
    """Services the forest gives everyone compared with a farm field, per ha per year."""
    return value_per_ha(biomes, story) - value_per_ha(biomes, R.SAVE_FOREST["farm_key"])


def max_offer(value: float) -> int:
    s = R.SAVE_FOREST
    top = max(s["min_max_offer"], value * s["max_offer_factor"])
    return int(math.ceil(top / s["max_offer_round"]) * s["max_offer_round"])


def deal_outcome(offer: float, profit: float, value: float) -> dict:
    """What happens to Ana's forest for a yearly `offer`.

    status: reject (forest cleared), cheapest (offer = profit), win-win, overpay (offer > value).
    gain: society's net gain per year (negative = loss).
    """
    if offer < profit:
        status, gain = "reject", -value
    elif offer > value:
        status, gain = "overpay", value - offer
    elif offer == profit:
        status, gain = "cheapest", value - offer
    else:
        status, gain = "win-win", value - offer
    return {
        "status": status,
        "gain": gain,
        "forest_saved": status != "reject",
        "no_deal_possible": profit > value,
    }


def deal_approval(offer: float, profit: float, value: float) -> list[float]:
    """Approval of Ana, Taxpayer, Villagers and Ecologist (illustrative model)."""
    s = R.SAVE_FOREST
    status = deal_outcome(offer, profit, value)["status"]
    share = (offer - profit) / (value - profit) if value > profit else 0.0

    if status == "reject":
        ana = s["ana"]["reject"]
    elif status == "overpay":
        ana = s["ana"]["overpay"]
    elif status == "cheapest":
        ana = s["ana"]["cheapest"]
    else:
        ana = s["ana"]["cheapest"] + s["ana"]["deal_bonus"] * share

    if status == "reject":
        taxpayer = s["taxpayer"]["cleared"]
    elif status == "overpay":
        taxpayer = s["taxpayer"]["overpay"]
    else:
        taxpayer = s["taxpayer"]["deal_max"] - s["taxpayer"]["deal_drop"] * share

    saved = status != "reject"
    villagers = s["villagers"]["saved" if saved else "cleared"]
    ecologist = s["ecologist"]["saved" if saved else "cleared"]
    return [ana, taxpayer, villagers, ecologist]


# ---------------------------------------------------------------- 6.2 grey vs green

def coast_cost_per_km(nature_share: float) -> float:
    cost = R.COAST["cost_per_m"]
    return 1000 * ((1 - nature_share) * cost["concrete"] + nature_share * cost["nature"])


def concrete_vs_nature_ratio() -> float:
    cost = R.COAST["cost_per_m"]
    return cost["concrete"] / cost["nature"]
