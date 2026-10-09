"""Game rules: approval and consequence tables. Edit numbers here without touching the logic.

All approval levels are an illustrative model, not survey data.
"""

# ---------------------------------------------------------------- characters

PEOPLE = {
    "ana": {"name": "Ana", "role": "farmer", "cares": "her income from the land",
            "image": "people/ana_neutral", "fallback": "👩‍🌾"},
    "villagers": {"name": "Villagers", "role": "downstream village",
                  "cares": "safety from floods and clean water",
                  "image": "people/villagers", "fallback": "🏘️"},
    "ecologist": {"name": "Ecologist", "role": "scientist", "cares": "species and healthy ecosystems",
                  "image": "people/ecologist", "fallback": "🔬"},
    "taxpayer": {"name": "Taxpayer", "role": "city worker", "cares": "not wasting public money",
                 "image": "people/taxpayer", "fallback": "💼"},
    "investor": {"name": "Investor", "role": "business", "cares": "profit",
                 "image": "people/investor", "fallback": "📈"},
    "elder": {"name": "Elder", "role": "community elder",
              "cares": "the land, the ancestors and the community's identity",
              "image": "people/elder", "fallback": "🧓"},
    "fisher": {"name": "Fisher", "role": "coastal fisher", "cares": "healthy reefs and plenty of fish",
               "image": "people/fisher", "fallback": "🎣"},
}

# Approval ring colours: red below LOW, yellow up to HIGH, green above
APPROVAL_LOW = 35
APPROVAL_HIGH = 65

# ---------------------------------------------------------------- 1.2 bees

BEES = {
    "stops": ["100%", "50%", "0%"],
    "scenes": ["scenes/breakfast_full", "scenes/breakfast_half", "scenes/breakfast_bare"],
    "food_variety": [100, 60, 25],
    "prices": ["normal", "higher", "very high"],
    "prices_pct": [20, 60, 100],       # bar length for the price meter (higher is worse)
    "people": ["ana", "villagers", "taxpayer", "ecologist"],
    "approval": [[90, 90, 85, 95], [50, 55, 50, 40], [10, 15, 15, 5]],
}

# ---------------------------------------------------------------- 3.1 drain the wetland

WETLAND = {
    "area_ha": 100,
    "farm_income_per_ha": 300,          # illustrative
    "stops": ["Keep it", "A third", "Two thirds", "All"],
    "drained": [0, 1 / 3, 2 / 3, 1],
    "scenes": ["scenes/wetland_0", "scenes/wetland_1", "scenes/wetland_2", "scenes/wetland_2"],
    "flood_scene": "scenes/wetland_flood",
    "flood_safety": [100, 65, 35, 10],
    "storm_floods_from": 2,             # index of "Two thirds"
    "people": ["ana", "villagers", "ecologist", "taxpayer"],
    "approval": [[30, 95, 100, 70], [55, 65, 50, 60], [75, 35, 20, 50], [90, 10, 5, 40]],
    "storm_approval": [40, 0, 0, 10],
}

# ---------------------------------------------------------------- 4.1 tipping point

TIPPING = {
    "thresholds": [55, 60, 65, 70, 75],
    "recovery_gap": 35,                 # recovery threshold R = T - 35
    "services_slope": 0.6,              # services = 100 - 0.6 x cleared
    "collapsed_services": 10,
    "collapsed_income_factor": 0.3,     # farm income = 0.3 x cleared after collapse
    "recovering_services": 50,
    "scene_steps": [(25, "scenes/forest_0"), (50, "scenes/forest_1"), (101, "scenes/forest_2")],
    "collapse_scene": "scenes/forest_3",
    "recovery_scene": "scenes/forest_4",
    "people": ["investor", "ana", "villagers", "ecologist"],
    "collapsed_approval": [5, 5, 0, 0],
    "recovering_approval": [20, 40, 50, 45],
}

# ---------------------------------------------------------------- 5.3 who decides?

WHO_DECIDES = {
    "stops": ["Money", "Mostly money", "Balance", "Mostly nature & culture", "Nature & culture"],
    "futures": ["plantation", "plantation", "agro", "sacred", "sacred"],
    "scenes": {"plantation": "scenes/future_plantation", "agro": "scenes/future_agro",
               "sacred": "scenes/future_sacred"},
    "people": ["investor", "ana", "elder", "ecologist"],
    "approval": [[95, 50, 5, 5], [75, 65, 20, 15], [45, 90, 60, 65], [20, 60, 85, 85], [5, 35, 95, 95]],
}

# ---------------------------------------------------------------- 6.1 save the forest

SAVE_FOREST = {
    "default_story": "tropical_forest",
    "default_profit": 300,
    "stories": {"tropical_forest": "Tropical forest", "mangrove": "Mangroves", "boreal_forest": "Northern forest"},
    "farm_key": "cropland",             # forest value = value_per_ha - farm field value
    "profit_max": 2000,
    "step": 50,
    "min_max_offer": 2500,
    "max_offer_factor": 1.3,
    "max_offer_round": 500,
    "people": ["ana", "taxpayer", "villagers", "ecologist"],
    "ana": {"reject": 10, "cheapest": 60, "overpay": 100, "deal_bonus": 40},
    "taxpayer": {"cleared": 40, "deal_max": 100, "deal_drop": 80, "overpay": 5},
    "villagers": {"saved": 95, "cleared": 10},
    "ecologist": {"saved": 100, "cleared": 0},
    "ana_faces": {"reject": "people/ana_angry", "cheapest": "people/ana_neutral",
                  "win-win": "people/ana_happy", "overpay": "people/ana_happy"},
}

# ---------------------------------------------------------------- 6.2 grey vs green

COAST = {
    "stops": ["All concrete", "Half & half", "All nature"],
    "nature_share": [0, 0.5, 1],
    "scenes": ["scenes/coast_grey", "scenes/coast_mix", "scenes/coast_green"],
    # Ferrario et al. 2014: median cost per metre of an artificial breakwater vs. reef restoration
    "cost_per_m": {"concrete": 19791, "nature": 1290},
    "ready_pct": [100, 70, 40],
    "ready_text": ["Immediately", "Partly now", "Takes years to grow"],
    "fish_pct": [10, 55, 95],
    "people": ["taxpayer", "fisher", "villagers", "ecologist"],
    "approval": [[20, 10, 90, 5], [60, 60, 85, 60], [95, 95, 55, 100]],
}
