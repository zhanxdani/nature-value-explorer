"""All interface texts (English). Edit wording here without touching the app logic.

Text may use **bold** markdown. Dollar signs are escaped automatically by utils/ui.py.
"""

# ---------------------------------------------------------------- chapters and screens

CHAPTERS = {
    1: {"title": "Nature in your morning", "presenter": "Julie"},
    2: {"title": "What is nature worth?", "presenter": "Goda"},
    3: {"title": "Build or keep?", "presenter": "Goda"},
    4: {"title": "The tipping point", "presenter": "Munkhtulga"},
    5: {"title": "From services to contributions", "presenter": "Munkhtulga / 2D"},
    6: {"title": "Solutions", "presenter": "2D"},
    7: {"title": "Quiz & finish", "presenter": ""},
}

SCREEN_TITLES = {
    "1.1": "What did you use today?",
    "1.2": "What if bees disappeared?",
    "2.1": "Guess the price",
    "2.2": "Which is worth more?",
    "3.1": "Drain the wetland",
    "4.1": "How much forest can you clear?",
    "5.1": "Good or bad?",
    "5.2": "Nature or culture?",
    "5.3": "Who decides?",
    "6.1": "Save the forest",
    "6.2": "Grey vs green",
    "6.3": "Six real solutions",
    "6.4": "What can you do?",
    "7.1": "Quiz",
    "7.2": "Finish",
}

COMMON = {
    "back": "Back",
    "next": "Next",
    "start": "Start",
    "who_approves": "Who approves?",
    "why": "Why?",
    "why_title": "Why do they approve?",
    "cares": "cares about {cares}",
    "approval_note": "Approval levels are an illustrative model, not survey data.",
    "model_badge": "Game model — shows an idea, not real data.",
    "learn_title": "Learn",
    "menu_title": "Menu",
    "notes_title": "Speaker notes",
    "play_again": "Play again",
    "per_ha": "per hectare per year",
}

# ---------------------------------------------------------------- 0 welcome

WELCOME = {
    "title": "What is nature worth?",
    "subtitle": "A 5-minute game about nature's value — by Group 9.",
    "start": "Start →",
}

# ---------------------------------------------------------------- 1.1 morning

MORNING = {
    "hint": "Tap everything you used today.",
    "counter": "Nature helped you **{n}** times before lunch.",
    "learn": "Forests, wetlands, oceans and soils work for us every day. Scientists call these benefits "
             "**ecosystem services**. Costanza et al. (1997) listed 17 of them. Most are free — so we "
             "rarely notice them.",
}

MORNING_ITEMS = [
    {"key": "coffee", "name": "Coffee", "fallback": "☕", "icon": ":material/coffee:",
     "line": "Bigger harvests when bees visit coffee flowers.", "services": ["Pollination", "Soil"]},
    {"key": "bread", "name": "Bread", "fallback": "🍞", "icon": ":material/bakery_dining:",
     "line": "Wheat is wind-pollinated, but needs fertile soil and rain.",
     "services": ["Soil", "Nutrient cycling"]},
    {"key": "apple", "name": "Apple", "fallback": "🍎", "icon": ":material/nutrition:",
     "line": "No pollinators, almost no apples.", "services": ["Pollination"]},
    {"key": "water", "name": "Water", "fallback": "💧", "icon": ":material/water_drop:",
     "line": "Forests and wetlands filter it before your tap.",
     "services": ["Water supply", "Water cleaning"]},
    {"key": "fish", "name": "Fish", "fallback": "🐟", "icon": ":material/set_meal:",
     "line": "Many fish grow up in mangroves and reefs.", "services": ["Food", "Habitat"]},
    {"key": "air", "name": "Air", "fallback": "🌬️", "icon": ":material/air:",
     "line": "Plants and ocean algae balance oxygen and CO₂.", "services": ["Gas regulation"]},
    {"key": "medicine", "name": "Medicine", "fallback": "💊", "icon": ":material/medication:",
     "line": "Aspirin was developed from a substance in willow bark.", "services": ["Genetic resources"]},
    {"key": "hike", "name": "Hike", "fallback": "🥾", "icon": ":material/hiking:",
     "line": "Nature gives rest, inspiration, a sense of home.", "services": ["Recreation", "Culture"]},
]

# ---------------------------------------------------------------- 1.2 bees

BEES = {
    "slider": "Pollinators left",
    "food": "Food variety",
    "prices": "Fruit & nut prices",
    "results": [
        "A full table: coffee, fruit, nuts, honey.",
        "Fewer fruits and nuts, pricier coffee.",
        "Bread and water survive — wheat is wind-pollinated. Most fruit, nuts and coffee are gone.",
    ],
    "fact": "75% of the world's food crops depend at least partly on pollinators (IPBES 2016).",
    "learn": "The IPBES 2016 assessment found that crops worth $235–577 billion a year are directly "
             "affected by pollinators, and almost 90% of wild flowering plants depend on animals for "
             "pollination.",
    "source": "IPBES (2016). Assessment report on pollinators, pollination and food production.",
}

# ---------------------------------------------------------------- 2.1 guess

GUESS = {
    "slider": "Your guess: nature's work per year (trillion $)",
    "reveal": "Reveal",
    "your_guess": "Your guess",
    "nature": "Nature ({low}–{high})",
    "economy": "World economy",
    "result": "Nature's work was worth almost 2 world economies!",
    "learn": "In 1997, 13 scientists led by Robert Costanza put a price on the services of all the world's "
             "ecosystems, using more than 100 earlier studies. They called $33 trillion a minimum: many "
             "services were missing, and they ignored sudden collapses. Most of this value never passes "
             "through markets. Values are in 1994 dollars — roughly double today.",
}

# ---------------------------------------------------------------- 2.2 which is worth more?

HIGHER_LOWER = {
    "hint": "Which is worth more per hectare?",
    "right": "✅ Right!",
    "wrong": "❌ Not this time!",
    "next": "Next round",
    "score": "See my score",
    "final": "You got **{score} of {total}**",
    "rounds": [
        {"a": "cropland", "b": "swamp",
         "fact": "Wetlands store water, stop floods and clean pollution."},
        {"a": "tropical_forest", "b": "coral",
         "fact": "Reefs shield coasts from storms and attract tourists."},
        {"a": "open_ocean", "b": "lake",
         "fact": "But the ocean is so huge that in total it gives more than any single biome: $8.4T a year!"},
        {"a": "boreal_forest", "b": "estuary",
         "fact": "Estuaries had the highest value per hectare of all."},
        {"a": "grassland", "b": "mangrove",
         "fact": "Mangroves break waves; fish grow up among their roots."},
    ],
    "learn": "Costanza et al. estimated the value of each ecosystem **per hectare per year** (a hectare is "
             "about 1.4 football pitches). Wetlands and coasts are 'small but mighty': little area, huge value.",
}

# ---------------------------------------------------------------- 3.1 wetland

WETLAND = {
    "story": "A 100-hectare wetland. The owner wants farmland.",
    "slider": "How much do you drain?",
    "income": "Owner's farm income",
    "nature": "Nature's work for everyone",
    "flood": "Flood safety",
    "result": "Owner +{gain}/yr · Everyone −{loss}/yr",
    "kept": "Kept: the wetland keeps working for everyone.",
    "storm": "Big storm!",
    "flooded": "The village floods. The wetland used to hold this water like a sponge.",
    "dry": "The wetland soaks up the rain — the village stays dry.",
    "learn": "Why do people still drain wetlands? The owner gets the money, while the lost services are "
             "spread over everyone — towns downstream, the climate, future generations. Economists call "
             "this an **externality**.",
    "services_heading": "What one hectare of wetland does every year:",
    "note": "Owner's income ($300/ha) is illustrative; nature's work is from Costanza et al. 1997.",
}

# ---------------------------------------------------------------- 4.1 tipping point

TIPPING = {
    "slider": "Forest cleared",
    "services": "Nature's services",
    "income": "Farm income",
    "ok": "So far, so good… nature declines slowly.",
    "collapse": "Collapse at {T}%! The forest can't hold water and soil anymore. Even the farms fail. "
                "Nobody wins.",
    "sliding_back": "Sliding back doesn't fix it — you must restore far more than you destroyed.",
    "recovering": "Recovering… but it will take decades.",
    "hint": "The edge is somewhere else every time!",
    "learn": "Ecosystems are like a Jenga tower: they stand… until they suddenly fall. This is a **tipping "
             "point**. Coming back is much harder than falling — scientists call this **hysteresis**. "
             "Costanza's team assumed nature changes smoothly and wrote that this makes their $33T too low. "
             "Because we never know exactly where the edge is, it's wise to stop early — the **precautionary "
             "principle**. **Our hypothesis:** the closer an ecosystem is to its tipping point, the more "
             "each lost piece is worth.",
}

# ---------------------------------------------------------------- 5.1 good or bad?

GOOD_BAD = {
    "buttons": ["Good", "Bad", "It depends"],
    "next": "Next card",
    "done": "Nature can help us, hurt us — or both.",
    "cards": [
        {"key": "wolf", "name": "Wolf", "fallback": "🐺",
         "text": "It depends! Wolves keep deer in check (good for forests) but may attack sheep. "
                 "Díaz et al. use exactly this example."},
        {"key": "mosquito", "name": "Mosquito", "fallback": "🦟",
         "text": "Mostly bad: mosquitoes spread diseases like malaria. NCP counts harmful contributions too."},
        {"key": "river_flood", "name": "River flood", "fallback": "🌊",
         "text": "It depends! Floods damage homes but bring fertile soil — Nile farming relied on it for "
                 "millennia."},
        {"key": "bee", "name": "Bee", "fallback": "🐝",
         "text": "Mostly good: bees pollinate crops and wild plants."},
    ],
    "learn": "Díaz et al. (2018) count **all** of nature's contributions to people — the good and the bad. "
             "The old 'services' view only counted the good ones.",
}

# ---------------------------------------------------------------- 5.2 nature or culture?

BRIDGE = {
    "line": "In Meghalaya, India, the Khasi people guide fig-tree roots across rivers until they become "
            "living bridges.",
    "question": "Nature or culture?",
    "buttons": ["Nature", "Culture", "Both"],
    "answer": "Both! In the NCP view, people and nature create these benefits together.",
    "learn": "This living root bridge is on the first page of Díaz et al. (2018): a benefit that nature and "
             "people create together over many years.",
}

# ---------------------------------------------------------------- 5.3 who decides?

WHO_DECIDES = {
    "slider": "What should matter most?",
    "average": "Average approval",
    "results": {
        "plantation": "Fast money — but the forest, its species and the sacred places are gone.",
        "agro": "Trees and crops together: some income, healthy soil, culture kept.",
        "sacred": "Forest, species and identity survive — but little cash income.",
    },
    "always": "Someone is always unhappy. That's why decisions need all voices at the table.",
    "learn": "In 2018, Sandra Díaz and 29 colleagues from IPBES ('the IPCC for biodiversity') proposed "
             "**nature's contributions to people (NCP)**. Compared with 'ecosystem services', NCP: counts "
             "good and bad contributions; sees culture in everything, not as one box out of 17; values "
             "money, identity, spirituality and nature itself; and listens to indigenous and local "
             "knowledge, not only scientists. NCP has three groups: **material**, **non-material** and "
             "**regulating**.",
}

# ---------------------------------------------------------------- 6.1 save the forest

SAVE_FOREST = {
    "story": "Ana earns ${profit}/yr if she clears 1 ha of {forest}. Everyone would lose ~{value}/yr of "
             "nature's work. Make her an offer!",
    "slider": "Your yearly offer to Ana",
    "change": "Change the story",
    "change_title": "Change the story",
    "forest_pick": "Which forest?",
    "profit_slider": "Ana's farm income ($/yr)",
    "apply": "Apply",
    "zone_no": "Ana says no",
    "zone_win": "Win-win",
    "zone_over": "Overpaying",
    "forest": "Forest",
    "saved": "Saved",
    "cleared": "Cleared",
    "gain": "Society",
    "results": {
        "reject": "No deal. The forest is cleared — everyone loses ~{value} a year.",
        "cheapest": "Perfect — the cheapest deal that saves the forest!",
        "win-win": "Deal! Society pays {offer} and keeps ~{value} → {gain} better off a year.",
        "overpay": "Ana is thrilled, but you pay more than the forest is worth.",
    },
    "no_win_win": "No win-win possible: farming earns Ana more than the forest gives everyone. "
                  "Payments alone can't save every ecosystem.",
    "learn": "This is how **Payments for Ecosystem Services (PES)** work: the sweet spot lies between what "
             "the farmer earns and what the forest gives everyone. Costa Rica has run a national PES "
             "program since 1997.",
}

# ---------------------------------------------------------------- 6.2 grey vs green

COAST = {
    "slider": "How do you protect the coast?",
    "cost": "Cost per km",
    "ready": "Ready to protect",
    "fish": "Fish & nature",
    "results": [
        "Safe right away, but {ratio}× more expensive and empty of fish.",
        "A common real-world choice: concrete where needed, nature where possible.",
        "{ratio}× cheaper and full of life — but villagers must wait for it to grow.",
    ],
    "fact": "Healthy reefs absorb on average 97% of wave energy.",
    "learn": "**Nature-based solutions** use ecosystems instead of concrete. Mangroves prevent more than "
             "$65 billion of flood damage a year and protect over 15 million people (Menéndez et al. 2020). "
             "New York City spent about $2.5 billion protecting the forests around its water sources "
             "instead of building a filtration plant estimated at up to $10 billion.",
    "source": "Costs: Ferrario et al. (2014), median $19,791 per metre for an artificial breakwater vs. "
              "$1,290 per metre for reef restoration.",
}

# ---------------------------------------------------------------- 6.3 six solutions

SOLUTIONS = {
    "fixes": "Fixes Chapter {n}",
    "cards": [
        {"key": "pes", "title": "Pay to protect", "fallback": "💰", "chapter": 6,
         "what": "Pay landowners to keep ecosystems.", "example": "Costa Rica, since 1997."},
        {"key": "accounting", "title": "Count nature in the economy", "fallback": "📒", "chapter": 2,
         "what": "Track ecosystems like a bank account.", "example": "UN SEEA Ecosystem Accounting (2021)."},
        {"key": "protected_area", "title": "Protect enough nature", "fallback": "🛡️", "chapter": 4,
         "what": "Stay far from tipping points.",
         "example": "30% of land and sea by 2030 (Kunming-Montreal, 2022)."},
        {"key": "nbs", "title": "Nature-based solutions", "fallback": "🌿", "chapter": 3,
         "what": "Use nature instead of concrete.",
         "example": "Mangrove restoration; New York's forested watersheds."},
        {"key": "comanagement", "title": "Share the decisions", "fallback": "🤝", "chapter": 5,
         "what": "Manage nature with local and indigenous communities.",
         "example": "IPBES assessments include local knowledge."},
        {"key": "business", "title": "Make business count nature", "fallback": "🏢", "chapter": 2,
         "what": "Companies report nature risks.", "example": "TNFD framework (2023)."},
    ],
    "learn": "No single solution is enough. The best results combine money, rules, nature itself — and "
             "local people.",
}

# ---------------------------------------------------------------- 6.4 what can you do?

ACTIONS = {
    "hint": "Tap what you could do:",
    "ally": "You're a nature ally!",
    "min": 3,
    "tiles": [
        {"key": "plants", "label": "Eat more plants, waste less food", "icon": ":material/restaurant:"},
        {"key": "bike", "label": "Walk, bike, take transit", "icon": ":material/directions_bike:"},
        {"key": "reuse", "label": "Buy less, reuse more", "icon": ":material/recycling:"},
        {"key": "flowers", "label": "Plant flowers for bees", "icon": ":material/local_florist:"},
        {"key": "policy", "label": "Support nature-friendly policies", "icon": ":material/how_to_vote:"},
        {"key": "science", "label": "Join citizen science (iNaturalist)", "icon": ":material/travel_explore:"},
    ],
    "learn": "Small actions add up — and they also show leaders that people care about nature.",
}

# ---------------------------------------------------------------- 7 quiz and finish

QUIZ = {
    "check": "Check",
    "next": "Next question",
    "finish": "See my score",
    "progress": "Question {n} of {total}",
    "right": "✅ Correct!",
    "wrong": "❌ The answer is: **{answer}**.",
    "questions": [
        {"q": "What are ecosystem services?",
         "options": ["Services companies sell", "Benefits people get from nature", "Government offices",
                     "Weather forecasts"],
         "answer": "Benefits people get from nature",
         "why": "Clean water, pollination and a stable climate are all ecosystem services."},
        {"q": "Costanza et al. (1997) estimated nature's services at about…",
         "options": ["$33 billion", "$1 trillion", "$33 trillion a year", "Nothing — impossible"],
         "answer": "$33 trillion a year",
         "why": "Almost 2 world economies — and the authors called it a minimum."},
        {"q": "Which ecosystems are worth the most per hectare?",
         "options": ["Estuaries and wetlands", "Farm fields", "Deserts", "Cities"],
         "answer": "Estuaries and wetlands",
         "why": "Wetlands and coasts are small but mighty."},
        {"q": "What is a tipping point?",
         "options": ["The highest mountain", "When prices rise", "A tip for a ranger",
                     "A point after which an ecosystem changes suddenly and may not come back"],
         "answer": "A point after which an ecosystem changes suddenly and may not come back",
         "why": "And coming back is much harder than falling."},
        {"q": "What new idea did Díaz et al. (2018) bring?",
         "options": ["Value nature only in money",
                     "Contributions can be good or bad, and culture and local knowledge matter",
                     "Only scientists decide", "Ecosystems never change"],
         "answer": "Contributions can be good or bad, and culture and local knowledge matter",
         "why": "Nature's value depends on who you ask."},
    ],
}

FINISH = {
    "score": "{score} / {total}",
    "completed": "Nature Value Explorer — completed!",
    "share": "Share",
    "sources": "Sources",
    "restart": "Start again",
}

# ---------------------------------------------------------------- menu, glossary, sources, share

MENU = {
    "chapters": "Chapters",
    "glossary": "Glossary",
    "sources": "Sources",
    "share": "Share (QR code)",
    "start": "Start screen",
}

GLOSSARY = [
    ("Ecosystem", "Living things — plants, animals, microbes — together with the water, soil and air "
                  "around them, working as one system."),
    ("Biodiversity", "The variety of life: within species, between species and between ecosystems."),
    ("Ecosystem services", "The benefits people get from nature, such as clean water, pollination and a "
                           "stable climate."),
    ("Natural capital", "Nature's stock — soils, forests, water, living things. Like money in the bank, "
                        "it produces a flow of benefits."),
    ("Hectare", "100 × 100 metres — about 1.4 football pitches."),
    ("Externality", "A cost of someone's action that other people pay — like floods downstream after a "
                    "wetland is drained."),
    ("Tipping point", "A threshold after which an ecosystem changes suddenly and may not come back."),
    ("Hysteresis", "Coming back is harder than falling: after a collapse, you must restore far more than "
                   "you destroyed."),
    ("Precautionary principle", "When serious harm is possible but uncertain, act carefully early "
                                "instead of waiting for proof."),
    ("IPBES", "The global science body that assesses nature for governments — 'the IPCC for "
              "biodiversity'."),
    ("NCP", "Nature's contributions to people: all the good and bad things people get from nature, seen "
            "through many kinds of knowledge and values."),
    ("PES", "Payments for ecosystem services: paying landowners to keep ecosystems that help everyone."),
    ("Nature-based solutions", "Using ecosystems, like mangroves or forests, instead of concrete to solve "
                               "problems."),
]

SOURCES = {
    "refs": [
        "Costanza, R. et al. (1997). The value of the world's ecosystem services and natural capital. "
        "*Nature* 387, 253–260. [doi:10.1038/387253a0](https://doi.org/10.1038/387253a0)",
        "Díaz, S. et al. (2018). Assessing nature's contributions to people. *Science* 359, 270–272. "
        "[doi:10.1126/science.aap8826](https://doi.org/10.1126/science.aap8826)",
        "IPBES (2016). Assessment report on pollinators, pollination and food production. "
        "[doi:10.5281/zenodo.3402856](https://doi.org/10.5281/zenodo.3402856)",
        "Ferrario, F. et al. (2014). The effectiveness of coral reefs for coastal hazard risk reduction and "
        "adaptation. *Nature Communications* 5, 3794. "
        "[doi:10.1038/ncomms4794](https://doi.org/10.1038/ncomms4794)",
        "Menéndez, P. et al. (2020). The global flood protection benefits of mangroves. *Scientific "
        "Reports* 10, 4404. [doi:10.1038/s41598-020-61136-6](https://doi.org/10.1038/s41598-020-61136-6)",
    ],
    "note": "Approval levels and game models illustrate ideas from the papers; they are not data.",
}

SHARE = {
    "title": "Scan to play",
    "no_url": "No app address yet. Set `APP_URL` in `config.py` after deploying, then push.",
    "back": "Back to the game",
}

# ---------------------------------------------------------------- speaker notes (?presenter=1)

SPEAKER_NOTES = {
    1: "**Julie:** Ask everyone to scan the QR. Tap breakfast items. Then drag pollinators to 0%.",
    2: "**Goda:** Hands up for guesses before Reveal. Then the higher/lower game.",
    3: "**Goda:** Drain everything, then press \"Big storm!\". Look at who approves — and who doesn't.",
    4: "**Munkhtulga:** Everyone clears the forest. Who collapsed it? Now try sliding back. "
       "State the hypothesis.",
    5: "**Munkhtulga / 2D:** Wolf card, root bridge. In \"Who decides?\" — find the position with the "
       "highest average approval.",
    6: "**2D:** Who found the cheapest deal? Then Grey vs green. Then 2–3 solution cards.",
    7: "Quiz together; who got 5/5?",
}
