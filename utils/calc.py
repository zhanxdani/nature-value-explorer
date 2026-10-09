"""Pure calculation functions. No Streamlit imports here, so everything is easy to test."""

from __future__ import annotations

import math
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

MARKET_GROUP = "Goods we buy and sell"


# ---------------------------------------------------------------- data loading

def load_biomes() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "biomes.csv")
    df["has_data"] = df["has_data"].astype(str).str.lower().eq("true")
    df["note"] = df["note"].fillna("")
    return df


def load_services() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "services.csv")


def biome_value(biomes: pd.DataFrame, name: str) -> float:
    """Value per hectare per year (1994 US$) for one biome."""
    return float(biomes.loc[biomes["biome"] == name, "value_per_ha"].iloc[0])


def biome_note(biomes: pd.DataFrame, name: str) -> str:
    return str(biomes.loc[biomes["biome"] == name, "note"].iloc[0])


# ---------------------------------------------------------------- page 1: guess

def nature_vs_gnp(total_tn: float, gnp_tn: float) -> float:
    return total_tn / gnp_tn


def per_person(total_tn: float, population: float) -> float:
    """Yearly value of ecosystem services per person, US$."""
    return total_tn * 1e12 / population


def market_share(services: pd.DataFrame) -> float:
    """Share of the total value that is goods traded in markets."""
    total = services["global_value_bn"].sum()
    market = services.loc[services["simple_group"] == MARKET_GROUP, "global_value_bn"].sum()
    return market / total


# ---------------------------------------------------------------- page 2: converter

def conversion_loss(area_ha: float, value_from: float, value_to: float) -> float:
    """Yearly loss of services when `area_ha` of one biome is turned into another."""
    return area_ha * (value_from - value_to)


def cumulative_loss(loss_per_year: float, years: int) -> list[float]:
    """Undiscounted accumulated loss after year 1, 2, ..., `years`."""
    return [loss_per_year * y for y in range(1, years + 1)]


# ---------------------------------------------------------------- page 3: discounting

def pv_annuity(a: float, r: float, t: float) -> float:
    """Present value of `a` per year for `t` years at discount rate `r`."""
    if r == 0:
        return a * t
    return a * (1 - (1 + r) ** -t) / r


def perpetuity(a: float, r: float) -> float:
    """Present value of `a` per year forever at discount rate `r`."""
    if r <= 0:
        return math.inf
    return a / r


# ---------------------------------------------------------------- page 4: tipping point

def tipping_multiplier(q: float, q_min: float) -> float:
    """How many times more the next hectare is worth compared with an intact system."""
    if q <= q_min:
        return math.inf
    return (100 - q_min) / (q - q_min)


def tipping_value(v0: float, q: float, q_min: float) -> float:
    """Marginal value V(q) = V0 * (100 - q_min) / (q - q_min); V(100) = V0."""
    return v0 * tipping_multiplier(q, q_min)


def tipping_zone_edges(q_min: float) -> tuple[float, float]:
    """Remaining-area levels where the multiplier crosses x2 and x5."""
    span = 100 - q_min
    return q_min + span / 2, q_min + span / 5


def tipping_status(multiplier: float) -> str:
    if multiplier < 2:
        return "Safe"
    if multiplier <= 5:
        return "Warning"
    return "Danger"


# ---------------------------------------------------------------- page 5: value lens

LENS_CRITERIA = ["Material", "Regulating", "Non-material", "Intrinsic"]

LENS_SCORES = pd.DataFrame(
    {
        "Material": [9, 2, 6],
        "Regulating": [3, 7, 6],
        "Non-material": [1, 10, 6],
        "Intrinsic": [1, 8, 5],
    },
    index=pd.Index(
        ["Oil palm plantation", "Sacred grove", "Community agroforestry"], name="Option"
    ),
)

ROLE_PRESETS = {
    "Investor": (7, 1, 1, 1),
    "Farmer": (4, 3, 2, 1),
    "Indigenous community": (2.5, 2, 4, 1.5),
    "Ecologist": (1, 4, 1, 4),
    "Balanced": (1, 1, 1, 1),
}


def normalize_weights(weights) -> list[float]:
    """Weights summing to 1. All-zero weights fall back to equal weights."""
    total = sum(weights)
    if total <= 0:
        return [1 / len(weights)] * len(weights)
    return [w / total for w in weights]


def lens_scores(weights, scores: pd.DataFrame = LENS_SCORES) -> pd.Series:
    """Weighted score per option, highest first."""
    w = normalize_weights(weights)
    result = sum(scores[c] * wi for c, wi in zip(LENS_CRITERIA, w))
    return result.sort_values(ascending=False)


def lens_winner(weights, scores: pd.DataFrame = LENS_SCORES) -> str:
    return lens_scores(weights, scores).index[0]


# ---------------------------------------------------------------- page 6: PES deal

def pes_deal(services_saved: float, opportunity_cost: float, payment: float, area: float) -> dict:
    """Outcome of a Payment for Ecosystem Services offer (all values per ha per yr)."""
    accepts = payment >= opportunity_cost
    has_zone = opportunity_cost <= services_saved
    return {
        "farmer_accepts": accepts,
        "forest_kept": accepts,
        "has_deal_zone": has_zone,
        "deal_zone": (opportunity_cost, services_saved) if has_zone else None,
        "society_net_gain": (services_saved - payment) * area if accepts else None,
        "loss": 0.0 if accepts else services_saved * area,
    }
