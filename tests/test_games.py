import random

import pytest

from content import rules as R
from content import texts as T
from utils import games


@pytest.fixture(scope="module")
def biomes():
    return games.load_biomes()


# ---------------------------------------------------------------- tipping point

def test_threshold_always_in_set():
    rng = random.Random(42)
    seen = {games.new_tipping_game(rng)["T"] for _ in range(300)}
    assert seen == set(R.TIPPING["thresholds"])
    assert min(seen) == 55 and max(seen) == 75


def test_collapse_exactly_at_threshold():
    game = games.new_tipping_game(random.Random(1))
    t = game["T"]
    game = games.update_tipping(game, t - 5)
    assert game["state"] == "ok"
    assert games.tipping_services(game) == pytest.approx(100 - 0.6 * (t - 5))
    game = games.update_tipping(game, t)
    assert game["state"] == "collapsed"
    assert games.tipping_services(game) == 10
    assert games.tipping_income(game) == pytest.approx(0.3 * t)
    assert games.tipping_scene(game) == "scenes/forest_3"


def test_sliding_back_stays_collapsed_until_recovery():
    game = games.new_tipping_game(random.Random(2))
    t, r = game["T"], games.recovery_threshold(game)
    assert r == t - 35
    game = games.update_tipping(game, 100)
    game = games.update_tipping(game, r + 5)
    assert game["state"] == "collapsed"
    assert games.sliding_back(game)
    game = games.update_tipping(game, r)
    assert game["state"] == "recovering"
    assert games.tipping_services(game) == 50
    assert games.tipping_scene(game) == "scenes/forest_4"
    assert games.tipping_approval(game) == R.TIPPING["recovering_approval"]


def test_scenes_before_collapse():
    game = {"T": 75, "state": "ok", "cleared": 0}
    assert games.tipping_scene(games.update_tipping(game, 20)) == "scenes/forest_0"
    assert games.tipping_scene(games.update_tipping(game, 25)) == "scenes/forest_1"
    assert games.tipping_scene(games.update_tipping(game, 50)) == "scenes/forest_2"


def test_tipping_approval_before_collapse():
    game = games.update_tipping({"T": 75, "state": "ok", "cleared": 0}, 40)
    assert games.tipping_approval(game) == pytest.approx([58, 60, 60, 48])
    game = games.update_tipping({"T": 75, "state": "ok", "cleared": 0}, 70)
    assert games.tipping_approval(game)[3] == 9  # max(0, 100 - 91)


# ---------------------------------------------------------------- save the forest

VALUE = 1915


@pytest.mark.parametrize(
    "offer, status, gain",
    [(0, "reject", -1915), (300, "cheapest", 1615), (1000, "win-win", 915), (2500, "overpay", -585)],
)
def test_deal_outcome(offer, status, gain):
    out = games.deal_outcome(offer, 300, VALUE)
    assert out["status"] == status
    assert out["gain"] == gain
    assert not out["no_deal_possible"]


def test_forest_value_from_data(biomes):
    assert games.forest_value(biomes, "tropical_forest") == 1915
    assert games.forest_value(biomes, "mangrove") == 9898
    assert games.forest_value(biomes, "boreal_forest") == 210


def test_no_deal_possible_for_northern_forest(biomes):
    value = games.forest_value(biomes, "boreal_forest")
    assert games.deal_outcome(300, 300, value)["no_deal_possible"]


def test_max_offer():
    assert games.max_offer(1915) == 2500
    assert games.max_offer(9898) == 13000  # 12,867 rounded up to 500


def test_deal_approval():
    assert games.deal_approval(0, 300, VALUE) == [10, 40, 10, 0]
    assert games.deal_approval(300, 300, VALUE) == [60, 100, 95, 100]
    assert games.deal_approval(VALUE, 300, VALUE) == pytest.approx([100, 20, 95, 100])
    assert games.deal_approval(2500, 300, VALUE) == [100, 5, 95, 100]


# ---------------------------------------------------------------- wetland

def test_wetland_nature_value(biomes):
    values = [games.wetland_nature_value(biomes, p) for p in R.WETLAND["drained"]]
    assert values == pytest.approx([1_958_000, 1_308_400, 658_800, 9_200])
    incomes = [games.wetland_farm_income(p) for p in R.WETLAND["drained"]]
    assert incomes == pytest.approx([0, 10_000, 20_000, 30_000])


def test_storm_floods_from_two_thirds():
    assert [games.storm_floods(i) for i in range(4)] == [False, False, True, True]


# ---------------------------------------------------------------- who decides

def test_who_decides_best_is_balance():
    assert games.best_compromise() == "Balance"
    averages = [games.average_approval(a) for a in R.WHO_DECIDES["approval"]]
    assert averages == [39, 44, 65, 63, 58]


# ---------------------------------------------------------------- higher or lower

def test_higher_lower_answers_match_data(biomes):
    expected = ["swamp", "coral", "lake", "estuary", "mangrove"]
    rounds = T.HIGHER_LOWER["rounds"]
    assert [games.higher_of(biomes, r["a"], r["b"]) for r in rounds] == expected
    for r, winner in zip(rounds, expected):
        loser = r["a"] if winner == r["b"] else r["b"]
        assert biomes.loc[winner, "value_per_ha"] > biomes.loc[loser, "value_per_ha"]


# ---------------------------------------------------------------- coast and formatting

def test_coast_costs():
    costs = [games.coast_cost_per_km(s) for s in R.COAST["nature_share"]]
    assert [games.money_short(c) for c in costs] == ["$19.8M", "$10.5M", "$1.29M"]
    assert round(games.concrete_vs_nature_ratio()) == 15


@pytest.mark.parametrize(
    "x, short", [(0, "$0"), (9_200, "$9.2k"), (-1_915, "-$1.9k"), (30_000, "$30k"), (658_800, "$0.66M"),
                 (1_958_000, "$1.96M"), (-585, "-$585")],
)
def test_money_short(x, short):
    assert games.money_short(x) == short


def test_money_about():
    assert games.money_about(1915) == "$1,900"
    assert games.money_about(9898) == "$9,900"
