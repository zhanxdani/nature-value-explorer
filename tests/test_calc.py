import pytest

import config
from utils import calc


@pytest.fixture(scope="module")
def biomes():
    return calc.load_biomes()


@pytest.fixture(scope="module")
def services():
    return calc.load_services()


def test_biome_totals(biomes):
    assert biomes["global_flow_bn"].sum() == pytest.approx(33268, abs=5)
    assert biomes["area_mha"].sum() == 51625


def test_services_total(services):
    assert services["global_value_bn"].sum() == pytest.approx(33268, abs=5)


def test_market_share_is_about_seven_percent(services):
    assert round(calc.market_share(services) * 100) == 7


def test_nature_vs_gnp():
    assert calc.nature_vs_gnp(config.TOTAL_AVG_TN, config.WORLD_GNP_1997_TN) == pytest.approx(1.848, abs=1e-3)


def test_per_person():
    assert calc.per_person(config.TOTAL_AVG_TN, config.WORLD_POP_1997) == pytest.approx(5687, abs=1)


def test_converter_tropical_to_cropland(biomes):
    loss = calc.conversion_loss(
        1_000_000, calc.biome_value(biomes, "Tropical forest"), calc.biome_value(biomes, "Cropland")
    )
    assert loss == pytest.approx(1.915e9)
    assert calc.cumulative_loss(loss, 30)[-1] == pytest.approx(1.915e9 * 30)


def test_pv_annuity():
    assert calc.pv_annuity(1.915e9, 0.05, 30) == pytest.approx(29.44e9, rel=1e-3)


def test_perpetuity():
    assert calc.perpetuity(2007, 0.05) == pytest.approx(40140)
    assert calc.perpetuity(2007, 0.01) / calc.perpetuity(2007, 0.10) == pytest.approx(10)


def test_tipping_point():
    v0 = 19580
    assert calc.tipping_value(v0, 100, 20) == pytest.approx(v0)
    assert calc.tipping_value(v0, 30, 20) == pytest.approx(8 * v0)
    assert calc.tipping_status(calc.tipping_multiplier(100, 20)) == "Safe"
    assert calc.tipping_status(calc.tipping_multiplier(30, 20)) == "Danger"
    assert calc.tipping_zone_edges(20) == (60, 36)


@pytest.mark.parametrize(
    "role, winner",
    [
        ("Investor", "Oil palm plantation"),
        ("Farmer", "Community agroforestry"),
        ("Indigenous community", "Sacred grove"),
        ("Ecologist", "Sacred grove"),
        ("Balanced", "Sacred grove"),
    ],
)
def test_value_lens_winners(role, winner):
    assert calc.lens_winner(calc.ROLE_PRESETS[role]) == winner


def test_value_lens_zero_weights():
    assert calc.normalize_weights([0, 0, 0, 0]) == [0.25] * 4


def _saved(biomes, forest):
    return calc.biome_value(biomes, forest) - calc.biome_value(biomes, "Cropland")


def test_pes_farmer_refuses(biomes):
    deal = calc.pes_deal(_saved(biomes, "Tropical forest"), 300, 150, 100)
    assert not deal["farmer_accepts"]
    assert deal["loss"] == pytest.approx(1915 * 100)


def test_pes_farmer_accepts(biomes):
    deal = calc.pes_deal(_saved(biomes, "Tropical forest"), 300, 400, 100)
    assert deal["farmer_accepts"]
    assert deal["society_net_gain"] == pytest.approx((1915 - 400) * 100)


def test_pes_no_deal_zone_for_temperate_forest(biomes):
    deal = calc.pes_deal(_saved(biomes, "Temperate/boreal forest"), 300, 150, 100)
    assert not deal["has_deal_zone"]
    assert deal["deal_zone"] is None
