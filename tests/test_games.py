import random

import pytest

import config
from content import texts
from utils import games


@pytest.fixture(scope="module")
def biomes():
    return games.load_biomes()


@pytest.fixture(scope="module")
def lost():
    return games.load_lost_services()


# ---------------------------------------------------------------- higher or lower

EXPECTED_WINNERS = ["swamp", "coral", "lake", "estuary", "mangrove"]


def test_higher_lower_answers_match_data(biomes):
    winners = [games.higher_of(biomes, r["a"], r["b"]) for r in texts.HIGHER_LOWER]
    assert winners == EXPECTED_WINNERS
    for r in texts.HIGHER_LOWER:
        w = games.higher_of(biomes, r["a"], r["b"])
        loser = r["b"] if w == r["a"] else r["a"]
        assert biomes.loc[w, "value_per_ha"] > biomes.loc[loser, "value_per_ha"]
        assert games.guess_is_right(biomes, r["a"], r["b"], w)
        assert not games.guess_is_right(biomes, r["a"], r["b"], loser)


def test_all_round_keys_exist(biomes):
    for r in texts.HIGHER_LOWER:
        assert r["a"] in biomes.index and r["b"] in biomes.index


# ---------------------------------------------------------------- tipping point

def play_until_end(game):
    while game["status"] == "playing":
        game = games.clear_patch(game)
    return game


def test_threshold_always_in_range():
    rng = random.Random(42)
    thresholds = {games.new_tipping_game(rng)["threshold"] for _ in range(500)}
    assert thresholds == set(range(games.TIP_MIN, games.TIP_MAX + 1))


def test_collapse_happens_exactly_at_threshold():
    game = games.new_tipping_game(random.Random(7))
    t = game["threshold"]
    for _ in range(t - 1):
        game = games.clear_patch(game)
        assert game["status"] == "playing"
    game = games.clear_patch(game)
    assert game["status"] == "collapsed"
    assert game["cleared"] == t
    assert games.services_left(game) == games.SERVICES_AFTER_COLLAPSE
    assert games.forest_grid(game).count("🥀") == games.TIP_PATCHES - t
    # Clearing after collapse does nothing
    assert games.clear_patch(game) == game


def test_stopping_before_threshold_wins():
    game = games.new_tipping_game(random.Random(3))
    for _ in range(game["threshold"] - 1):
        game = games.clear_patch(game)
    game = games.stop_game(game)
    assert game["status"] == "stopped"
    assert games.services_left(game) == 100 - games.SERVICE_DROP_PER_PATCH * (game["threshold"] - 1)
    assert games.forest_grid(game).count("🌳") == games.TIP_PATCHES - game["cleared"]


def test_money_grows_by_one_per_patch():
    game = games.new_tipping_game(random.Random(1))
    game = games.clear_patch(games.clear_patch(game))
    assert games.money_from_farms(game) == 2
    assert games.services_left(game) == 94


# ---------------------------------------------------------------- save the forest

@pytest.mark.parametrize(
    "offer, expected",
    [(0, "reject"), (100, "reject"), (300, "deal"), (1_000, "deal"), (2_500, "overpay")],
)
def test_save_the_forest_outcomes(biomes, offer, expected):
    services = games.value_per_ha(biomes, "tropical_forest") - games.value_per_ha(biomes, "cropland")
    assert games.deal_outcome(offer, config.ANA_FARM_PROFIT, services) == expected


def test_every_offer_has_a_reaction():
    assert set(texts.ANA_OFFERS) == set(texts.ANA_REACTIONS)


# ---------------------------------------------------------------- build or keep

def test_tropical_forest_to_farm(biomes, lost):
    result = games.trade(biomes, lost, "tropical_forest", "cropland", area_ha=1)
    assert result["loss"] == 2007
    assert result["gain"] == 92
    assert result["gain_estimated"]
    assert len(result["lost_services"]) == 5


def test_city_is_not_estimated(biomes, lost):
    assert not games.trade(biomes, lost, "swamp", "urban")["gain_estimated"]


def test_lost_services_do_not_exceed_biome_value(biomes, lost):
    for key, total in lost.groupby("biome_key")["value_per_ha"].sum().items():
        assert total <= biomes.loc[key, "value_per_ha"], key


# ---------------------------------------------------------------- rounding

@pytest.mark.parametrize(
    "x, expected",
    [(92, 92), (252, 250), (245, 250), (2007, 2000), (1915, 1900), (19580, 20000),
     (22832, 23000), (9990, 10000), (200_700, 200_000), (20_070_000, 20_000_000)],
)
def test_nice_round(x, expected):
    assert games.nice_round(x) == expected
