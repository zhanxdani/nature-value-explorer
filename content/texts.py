"""All interface texts (English). Edit wording here without touching the app logic.

Text may use **bold** markdown. Dollar signs are escaped automatically by utils/ui.py.
"""

# ---------------------------------------------------------------- chapters

CHAPTERS = [
    {"emoji": "🏠", "title": "Welcome", "nav": "Welcome"},
    {"emoji": "☕", "title": "Nature in your morning", "nav": "1 · Your morning", "presenter": "Julie"},
    {"emoji": "💰", "title": "What is nature worth?", "nav": "2 · Nature's worth", "presenter": "Goda"},
    {"emoji": "🚜", "title": "Build or keep?", "nav": "3 · Build or keep?", "presenter": "Goda"},
    {"emoji": "💥", "title": "The tipping point game", "nav": "4 · Tipping point", "presenter": "Munkhtulga"},
    {"emoji": "🌉", "title": "From services to contributions", "nav": "5 · Contributions", "presenter": "Munkhtulga / 2D"},
    {"emoji": "🛠️", "title": "Solutions", "nav": "6 · Solutions", "presenter": "2D"},
    {"emoji": "🏆", "title": "Quiz & finish", "nav": "7 · Quiz"},
]
LAST_CHAPTER = len(CHAPTERS) - 1

SPEAKER_NOTES = {
    1: "**Julie:** Ask the room to scan the QR now. Let everyone tap their breakfast items. "
       "Key word: ecosystem services.",
    2: "**Goda:** Ask for a show of hands on the guess before revealing. Then the higher/lower game. "
       "Mention: $33T is a minimum.",
    3: "**Goda:** Build a farm on a swamp together. Explain externality: the farmer gains, "
       "everyone else pays.",
    4: "**Munkhtulga:** Everyone plays once; ask who collapsed their forest. State the hypothesis.",
    5: "**Munkhtulga / 2D:** Wolf card, root bridge, \"Who decides?\". Contrast old and new view.",
    6: "**2D:** Save the forest — ask what offer people chose. Walk through 2–3 solution cards "
       "linked to earlier chapters.",
    7: "Quiz together; ask who got 5/5.",
}

# ---------------------------------------------------------------- welcome

WELCOME = {
    "title": "🌍 What is nature worth?",
    "subtitle": "A 5-minute journey through ecosystem services — made by Group 9.",
    "start": "Start the journey →",
    "chapters_heading": "Chapters",
    "more_heading": "Extras",
}

# ---------------------------------------------------------------- chapter 1

CH1 = {
    "learn": "Forests, wetlands, oceans and soils quietly work for us every day: they clean water, "
             "build soil, pollinate crops and keep the climate stable. Scientists call these benefits "
             "**ecosystem services**. Most of them are free — so we rarely notice them.",
    "play": "What did you use this morning?",
    "pick": "Tap everything you used today:",
    "counter": "Nature helped you **{n}** times before lunch!",
    "empty": "👆 Tap a few items to see what nature did for you.",
    "remember": "Nature works for you all day — for free. That's exactly why it's easy to forget.",
    "more_intro": "Costanza et al. (1997) grouped nature's benefits into **17 ecosystem services** — "
                  "from gas regulation to cultural values.",
}

MORNING_ITEMS = [
    {"item": "☕ Coffee",
     "text": "Coffee grows in tropical soils, and the harvest is bigger when bees visit its flowers.",
     "services": ["Soil formation", "Pollination"]},
    {"item": "🍞 Bread",
     "text": "Wheat is pollinated by wind, not bees — but it needs fertile soil, rain and nutrients "
             "recycled by tiny soil organisms.",
     "services": ["Soil formation", "Nutrient cycling", "Water supply"]},
    {"item": "🍎 Apple",
     "text": "Apple trees need insects, mostly bees, to carry pollen between flowers. "
             "No pollinators, almost no apples.",
     "services": ["Pollination"]},
    {"item": "💧 Glass of water",
     "text": "Forests and wetlands filter rainwater and store it in rivers and underground before it "
             "reaches your tap.",
     "services": ["Water supply", "Waste treatment"]},
    {"item": "🐟 Fish",
     "text": "Many fish grow up in mangroves, seagrass meadows and coral reefs — nature's nurseries.",
     "services": ["Food production", "Habitat"]},
    {"item": "🌬️ A breath of air",
     "text": "Plants and ocean algae keep the balance of oxygen and CO₂ in the air.",
     "services": ["Gas regulation", "Climate regulation"]},
    {"item": "💊 Medicine",
     "text": "Many medicines come from nature: aspirin was developed from a substance found in willow bark.",
     "services": ["Genetic resources"]},
    {"item": "🥾 Weekend walk",
     "text": "Parks, mountains and lakes give us rest, inspiration and a feeling of home.",
     "services": ["Recreation", "Cultural"]},
]

SEVENTEEN_SERVICES = [
    "🌬️ Gas regulation",
    "🌡️ Climate regulation",
    "🌊 Disturbance regulation (storm and flood protection)",
    "💦 Water regulation",
    "💧 Water supply",
    "⛰️ Erosion control",
    "🪨 Soil formation",
    "♻️ Nutrient cycling",
    "🧪 Waste treatment",
    "🐝 Pollination",
    "🐞 Biological control",
    "🏡 Refugia (habitat)",
    "🍎 Food production",
    "🪵 Raw materials",
    "🧬 Genetic resources",
    "🥾 Recreation",
    "🎨 Cultural",
]

# ---------------------------------------------------------------- chapter 2

CH2 = {
    "learn": "If nature's work is free, how do we show how important it is? In 1997, 13 scientists led "
             "by Robert Costanza tried something bold: they put a **price tag** on the services of all "
             "the world's ecosystems, using more than 100 earlier studies.",
    "play_a": "Guess the price",
    "question": "How much is nature's work worth every year?",
    "options": ["$1 trillion", "$10 trillion", "$33 trillion", "$100 trillion"],
    "correct": "$33 trillion",
    "right": "🎉 You got it!",
    "wrong": "😮 Not quite!",
    "answer": "About **${avg} trillion per year** (somewhere between {low} and {high}). The whole world "
              "economy at that time: about **${gnp} trillion**. Nature's work was worth almost "
              "**2 world economies**!",
    "bar_nature": "🌍 Nature",
    "bar_economy": "💵 World economy",
    "trillion_note": "1 trillion = 1,000,000,000,000.",
    "play_b": "Which is worth more?",
    "play_b_intro": "Tap the one you think is worth more **per hectare** (≈ 1.4 football pitches).",
    "round": "Round {n} of {total} · Score: {score}",
    "per_ha": "per hectare per year",
    "right_b": "✅ Right!",
    "wrong_b": "❌ Not this time!",
    "next_round": "Next round →",
    "see_score": "See my score",
    "final": "You got **{score} of {total}**!",
    "play_again": "🔄 Play again",
    "remember": "Wetlands and coasts are 'small but mighty': little area, huge value.",
    "more": [
        "**How did they calculate it?** For each type of ecosystem they estimated the value of each "
        "service per hectare, multiplied by the ecosystem's total area, and added everything up.",
        "**Why \"at least\"?** The authors call $33 trillion a minimum: many services were missing, "
        "there was no data for deserts, tundra and ice, and they ignored sudden collapses (see Chapter 4).",
        "**Most of this value never passes through markets** — nobody pays for nutrient cycling "
        "(the biggest item, about $17 trillion) or for flood protection.",
        "*Values are in 1994 US dollars — roughly double in today's money.*",
    ],
}

# Higher-or-lower rounds: biome keys from data/biomes.csv. The correct answer comes from the data.
HIGHER_LOWER = [
    {"a": "cropland", "b": "swamp",
     "fact": "Wetlands store water, stop floods and clean pollution — work that would be very "
             "expensive to replace."},
    {"a": "tropical_forest", "b": "coral",
     "fact": "Reefs protect coasts from storms and attract millions of divers and tourists."},
    {"a": "open_ocean", "b": "lake",
     "fact": "Plot twist: the ocean is so huge that, in total, it gives more than any other single "
             "biome — about $8.4 trillion a year!"},
    {"a": "boreal_forest", "b": "estuary",
     "fact": "Estuaries — where rivers meet the sea — had the highest value per hectare of all biomes."},
    {"a": "grassland", "b": "mangrove",
     "fact": "Mangroves break waves, clean water, and many fish grow up between their roots."},
]

# Short names for the higher-or-lower buttons (fall back to the name in biomes.csv)
SHORT_NAMES = {"boreal_forest": "Northern forest", "mangrove": "Mangroves"}

# ---------------------------------------------------------------- chapter 3

CH3 = {
    "learn": "When we turn a forest into a farm, we get something we can sell. But we also lose "
             "services that nobody pays for. Let's look at the trade.",
    "play": "Make the trade",
    "choose_nature": "Choose a piece of nature",
    "choose_build": "What do you build?",
    "build": "🚜 Build it!",
    "pick_first": "👆 Pick a piece of nature and what to build, then press the button.",
    "result_title": "Your trade, for **1 hectare** every year:",
    "gain_farm": "✅ **You gain:** a farm worth about **{value}**",
    "gain_city": "✅ **You gain:** a city — its nature value was *not estimated in the study*",
    "lose": "❌ **You lose:** about **{value}** of nature's work",
    "lost_heading": "Services you just lost:",
    "how_big": "How big?",
    "how_big_text": "That's about **{pitches}** football pitches — and about **{value}** of free "
                    "nature's work lost every year.",
    "undo": "🌱 Undo?",
    "undo_text": "Not so fast: a forest needs decades to grow back, and a drained wetland may never "
                 "work the same way again.",
    "remember": "A farm can earn money in a market — but the free services we lose are often worth "
                "far more.",
    "more": "So why do people still clear forests? Because the farmer gets the money, while the lost "
            "services are spread over everyone — towns downstream, the climate, future generations. "
            "Economists call this an **externality**: a cost that someone else pays.",
}

TRADE_NATURE = {"tropical_forest": "🌳 Tropical forest", "swamp": "🌿 Swamp", "mangrove": "🌴 Mangroves"}
TRADE_BUILD = {"cropland": "🌾 Farm", "urban": "🏙️ City"}
TRADE_AREAS = {1: "1 ha", 100: "100 ha", 10_000: "10,000 ha"}

# ---------------------------------------------------------------- chapter 4

CH4 = {
    "badge": "🎮 Game model — shows an idea, not real data.",
    "learn": "Ecosystems are like a Jenga tower: you can remove some pieces and it still stands… "
             "until suddenly it falls. This sudden change is called a **tipping point**. Costanza's team "
             "assumed nature changes smoothly — and they wrote that this makes their estimate too low.",
    "play": "How much can you take?",
    "intro": "Each 🌳 is a patch of forest. Clearing one gives you a farm and money — but somewhere "
             "there is a hidden edge.",
    "money": "💵 Money from farms",
    "services": "💧 Nature's services",
    "clear": "🪓 Clear one patch",
    "stop": "✋ Stop and keep the rest",
    "collapse": "💥 Collapse!",
    "collapse_text": "The forest became too small to hold water and soil. Even the trees you kept "
                     "stopped working. And clearing more won't bring it back.",
    "win": "🎉 Smart! You kept the forest working. But notice: you never knew where the edge was.",
    "edge": "The edge was at patch **{threshold}** — you cleared **{cleared}**.",
    "play_again": "🔄 Play again",
    "play_again_hint": "The edge is in a different place every time!",
    "remember": "We don't know exactly where the edge is — so it's wise to stop early. This is called "
                "the **precautionary principle**.",
    "more": [
        "**Real tipping points:** coral reefs bleaching after heatwaves; clear lakes suddenly turning "
        "green with algae when too many nutrients flow in; scientists warn parts of the Amazon could "
        "turn into savanna.",
        "**Our hypothesis:** the closer an ecosystem is to its tipping point, the more every lost piece "
        "is worth — near the edge, its value shoots up (Costanza et al. 1997, Fig. 1b).",
        "**Restoring is harder than destroying:** bringing a collapsed ecosystem back usually takes far "
        "more time and money than it took to break it.",
    ],
}

# ---------------------------------------------------------------- chapter 5

CH5 = {
    "learn": "In 2018, Sandra Díaz and 29 colleagues from **IPBES** — often called 'the IPCC for "
             "biodiversity' — said the 'services with a price tag' view is useful but too narrow. They "
             "proposed a wider idea: **nature's contributions to people (NCP)**.",
    "play_a": "Good or bad?",
    "card_of": "Card {n} of {total}",
    "vote": "Is it good or bad for people?",
    "votes": ["👍 Good", "👎 Bad", "🤷 It depends"],
    "heres_the_thing": "**Here's the thing…** {text}",
    "next_card": "Next card →",
    "cards_done": "That's all the cards! Nature can help us, hurt us — or both.",
    "play_again": "🔄 Play again",
    "play_b": "Nature or culture?",
    "bridge": "In Meghalaya, India, the Khasi people guide the roots of rubber fig trees across rivers. "
              "Over many years the roots grow into **living bridges** strong enough to walk on. "
              "Is this bridge nature or culture?",
    "bridge_options": ["🌳 Nature", "🧑‍🤝‍🧑 Culture", "🤝 Both"],
    "bridge_answer": "**Both!** In the NCP view, people and nature create these benefits together. "
                     "(This bridge is on the first page of Díaz et al. 2018.)",
    "play_c": "Who decides?",
    "who_intro": "One forest. Who decides what happens to it?",
    "you_choose": "And you? What would you choose?",
    "you_answer": "There's no single right answer. That's why decisions about nature need many voices "
                  "at the table.",
    "compare_heading": "Old view vs. new view",
    "ncp_groups": "Díaz et al. sort nature's contributions into three groups — 🍎 **Material** (food, "
                  "energy, materials), 🎨 **Non-material** (learning, inspiration, identity) and "
                  "🌦️ **Regulating** (climate, water, pollination) — **18 categories** in total.",
    "remember": "Nature isn't just a factory with a price tag. What it means depends on who you ask.",
    "more": "Why the change? The 'services' approach was dominated by ecology and economics. Many social "
            "scientists and indigenous communities felt left out and worried about turning nature into a "
            "product to buy and sell. The NCP approach keeps the useful parts of the old idea but welcomes "
            "more voices — which also makes its findings more likely to be accepted by governments.",
}

GOOD_BAD_CARDS = [
    {"card": "🐺 Wolf",
     "text": "It depends! Wolves keep deer numbers in check, which helps forests — but they may attack "
             "sheep, which hurts shepherds. Díaz et al. use exactly this kind of example."},
    {"card": "🦟 Mosquito",
     "text": "Mostly bad for people: mosquitoes can spread diseases like malaria. NCP counts harmful "
             "contributions too — the old \"services\" view only counted the good ones."},
    {"card": "🌊 River flood",
     "text": "It depends! Floods damage homes, but they also bring fertile soil to fields — farming along "
             "the Nile relied on this for thousands of years."},
    {"card": "🐝 Bee",
     "text": "Mostly good: bees pollinate crops and wild plants. (Unless you're allergic!)"},
    {"card": "🌲 Sacred tree",
     "text": "Good — but not in dollars. For many communities a sacred tree or grove is part of who "
             "they are. That's a \"non-material\" contribution."},
]

PERSONAS = [
    {"who": "💼 Investor", "choice": "🌴 Oil palm plantation", "why": "It makes the most money, fast."},
    {"who": "👩‍🌾 Local farmer", "choice": "🌳🌾 Trees + crops together (agroforestry)",
     "why": "Food and income, while keeping the soil and water healthy."},
    {"who": "🏘️ Indigenous community", "choice": "🌲 Sacred forest",
     "why": "Our ancestors, our medicine and our identity live here."},
    {"who": "🔬 Ecologist", "choice": "🛡️ Protected forest", "why": "Most species, best climate protection."},
]

OLD_VIEW = {
    "title": "🏭 Ecosystem services (Costanza 1997)",
    "points": [
        "Nature as a factory that delivers services",
        "Value mostly in money",
        "Only benefits",
        "Culture is one box out of 17",
        "Mainly scientists and economists",
    ],
}
NEW_VIEW = {
    "title": "🤝 Nature's contributions to people (Díaz 2018)",
    "points": [
        "People and nature create benefits together",
        "Many kinds of value: money, identity, spirituality, nature for its own sake",
        "Good *and* bad contributions",
        "Culture runs through everything",
        "Science **and** indigenous & local knowledge",
    ],
}

# ---------------------------------------------------------------- chapter 6

CH6 = {
    "learn": "We've seen three problems: nature's value is invisible in prices, ecosystems can collapse "
             "suddenly, and people value nature in different ways. Here's what the world is doing about it.",
    "badge": "🎮 Game model — shows an idea, not real data.",
    "play_a": "Save the forest",
    "story": "Ana owns 1 hectare of tropical forest. If she clears it for a farm, she earns "
             "**$300 a year**. The forest's services — clean water, climate, soil — are worth about "
             "**$2,000 a year** to everyone. You're the government. How much do you offer Ana each "
             "year to keep the forest?",
    "offer": "Your offer per year:",
    "zone_no": "🔴 **Ana says no** ($0–300)",
    "zone_win": "🟢 **Win-win zone** ($300–1,900)",
    "zone_over": "⚪ **Overpaying** (more than $1,900)",
    "sweet_spot": "The sweet spot lies between what the farmer earns and what the forest gives everyone. "
                  "This is how **Payments for Ecosystem Services (PES)** work. Costa Rica has run a "
                  "national PES program since 1997.",
    "play_b": "Six real solutions",
    "what": "**What it is:**",
    "example": "**Real example:**",
    "limits": "**Limits:**",
    "fixes": "Fixes: Chapter {n} — {problem}",
    "prev": "← Previous",
    "next": "Next →",
    "play_c": "What can you do?",
    "pick_actions": "Pick the ones you could try:",
    "ally": "You're a nature ally! 🌍",
    "pick_more": "Pick at least 3 to become a nature ally.",
    "remember": "No single solution is enough. The best results combine money, rules, nature itself — "
                "and local people.",
    "more": "Payments, accounts and protected areas build on Costanza's idea that nature's value must be "
            "made visible. Shared decisions and local knowledge come from Díaz et al.: who decides matters "
            "as much as how much nature is worth.",
}

ANA_OFFERS = [0, 100, 300, 1_000, 2_500]
ANA_REACTIONS = {
    0: "😠 Ana clears the forest. Everyone loses about $1,900 of nature's work every year.",
    100: "😠 Not enough — she earns more from farming. The forest is gone.",
    300: "🙂 Deal! Ana is no worse off, and society keeps about $1,600 of value every year.",
    1_000: "😃 Deal! Ana is happy, and society still gains about $900 every year.",
    2_500: "🤨 Ana is thrilled — but you pay more than the forest's services are worth. "
           "Bad deal for taxpayers.",
}

SOLUTIONS = [
    {"title": "💰 Pay to protect (PES)",
     "what": "Pay landowners to keep ecosystems.",
     "example": "Costa Rica, since 1997.",
     "chapter": 3, "problem": "the lost services had no price",
     "limits": "Needs stable funding, and payments must reach the right people."},
    {"title": "📒 Count nature in the economy",
     "what": "Countries track their ecosystems like a bank account, not just GDP.",
     "example": "The UN standard SEEA Ecosystem Accounting (2021).",
     "chapter": 2, "problem": "nature's value is invisible",
     "limits": "Hard to measure, takes years."},
    {"title": "🛡️ Protect enough nature",
     "what": "Keep ecosystems far from their tipping points.",
     "example": "The Kunming-Montreal Global Biodiversity Framework (2022) aims to protect 30% of land "
                "and sea by 2030.",
     "chapter": 4, "problem": "sudden collapse",
     "limits": "Protected on paper doesn't always mean protected on the ground."},
    {"title": "🌿 Nature-based solutions",
     "what": "Use nature instead of concrete.",
     "example": "Restoring mangroves to protect coasts from storms; New York protects the forests around "
                "its water sources instead of building a giant water-filtration plant.",
     "chapter": 3, "problem": "what we lose when we build",
     "limits": "Needs space and time to work."},
    {"title": "🤝 Share the decisions",
     "what": "Manage nature together with indigenous and local communities, who look after much of the "
             "world's biodiversity.",
     "example": "IPBES assessments now include indigenous and local knowledge (Díaz et al. 2018).",
     "chapter": 5, "problem": "people value nature in different ways",
     "limits": "Needs trust, fair rules and land rights."},
    {"title": "🏢 Make business count nature",
     "what": "Companies report how they depend on and affect nature.",
     "example": "The TNFD framework (2023).",
     "chapter": 2, "problem": "nature's value is invisible",
     "limits": "Still voluntary for most companies."},
]

YOUR_ACTIONS = [
    "🥗 Eat more plants, waste less food",
    "🚲 Walk, bike, take transit",
    "🛍️ Buy less, reuse more",
    "🌼 Plant flowers for bees",
    "🗳️ Support nature-friendly policies",
    "🔬 Join citizen science (e.g., iNaturalist)",
]
ALLY_MIN = 3

# ---------------------------------------------------------------- chapter 7

CH7 = {
    "intro": "5 easy questions, one at a time.",
    "question_of": "Question {n} of {total} · Score: {score}",
    "check": "Check",
    "next": "Next →",
    "finish": "See my score",
    "right": "✅ Correct!",
    "wrong": "❌ Not quite — the answer is: **{answer}**.",
    "score": "Your score: {score} / {total}",
    "badge": "🌍 Nature Value Explorer — completed!",
    "great": "Amazing — you're a nature value expert!",
    "ok": "Nice try! Every chapter is still there if you want another look.",
    "share": "📱 Share with a friend",
    "sources": "📚 Sources & further reading",
    "restart": "🔄 Start again",
}
QUIZ_BALLOONS_MIN = 4

QUIZ = [
    {"q": "What are ecosystem services?",
     "options": ["Services companies sell to protect nature", "Benefits people get from nature",
                 "Government environmental offices", "Weather forecasts"],
     "answer": "Benefits people get from nature",
     "why": "Clean water, pollination, fertile soil and a stable climate are all ecosystem services."},
    {"q": "Costanza et al. (1997) estimated nature's services at about…",
     "options": ["$33 billion a year", "$1 trillion a year",
                 "$33 trillion a year — almost 2× the world economy",
                 "Nothing — they said it can't be measured"],
     "answer": "$33 trillion a year — almost 2× the world economy",
     "why": "The world economy at that time was about $18 trillion a year."},
    {"q": "Which ecosystems are worth the most per hectare?",
     "options": ["Estuaries and wetlands", "Farm fields", "Deserts", "Cities"],
     "answer": "Estuaries and wetlands",
     "why": "Wetlands and coasts are 'small but mighty': little area, huge value."},
    {"q": "What is a tipping point?",
     "options": ["The highest mountain in a region", "The moment prices go up", "A tip for a park ranger",
                 "A point after which an ecosystem changes suddenly and may not come back"],
     "answer": "A point after which an ecosystem changes suddenly and may not come back",
     "why": "Like a Jenga tower: it stands… until suddenly it falls."},
    {"q": "What new idea did Díaz et al. (2018) bring?",
     "options": ["Nature should only be valued in money",
                 "Nature's contributions can be good or bad, and culture and local knowledge matter",
                 "Only scientists should decide", "Ecosystems never change"],
     "answer": "Nature's contributions can be good or bad, and culture and local knowledge matter",
     "why": "Nature isn't just a factory with a price tag — what it means depends on who you ask."},
]

# ---------------------------------------------------------------- extra pages

GLOSSARY = [
    ("Ecosystem", "A community of living things — plants, animals, microbes — together with the water, "
                  "soil and air around them, all working as one system."),
    ("Biodiversity", "The variety of life on Earth: the differences within species, between species, "
                     "and between ecosystems."),
    ("Biome", "A large type of ecosystem found in many places around the world, such as tropical forest, "
              "coral reef or grassland."),
    ("Ecosystem services", "The benefits people get from ecosystems, such as clean water, pollination "
                           "and a stable climate."),
    ("Natural capital", "The world's stock of nature — soils, forests, water, living things. Like money "
                        "in the bank, it produces a flow of benefits: ecosystem services."),
    ("Hectare", "An area of 100 × 100 metres (10,000 m²) — about 1.4 football pitches."),
    ("Market value vs. outside the market", "Some benefits have a price because they are bought and sold, "
                                            "like timber or fish. Most ecosystem services, like flood "
                                            "protection, are outside the market — nobody pays for them, "
                                            "so their value stays invisible."),
    ("Externality", "A cost (or benefit) of someone's action that falls on other people — for example, "
                    "floods downstream after a forest upstream is cleared."),
    ("Tipping point", "A threshold after which an ecosystem changes suddenly into a different state and "
                      "may not come back."),
    ("Precautionary principle", "When serious harm is possible but uncertain, act carefully early instead "
                                "of waiting for full proof."),
    ("IPBES", "The Intergovernmental Science-Policy Platform on Biodiversity and Ecosystem Services — the "
              "global body that assesses the state of nature for governments, often called 'the IPCC for "
              "biodiversity'."),
    ("Nature's contributions to people (NCP)", "All the contributions, good and bad, that people get from "
                                               "nature — material, non-material and regulating — seen "
                                               "through many kinds of knowledge and values."),
    ("Payments for ecosystem services (PES)", "Paying landowners or communities to keep ecosystems that "
                                              "benefit others, for example forests that protect a city's "
                                              "water."),
]

SOURCES = {
    "title": "📚 Sources",
    "refs": [
        "Costanza, R., d'Arge, R., de Groot, R., Farber, S., Grasso, M., Hannon, B., Limburg, K., "
        "Naeem, S., O'Neill, R. V., Paruelo, J., Raskin, R. G., Sutton, P., & van den Belt, M. (1997). "
        "The value of the world's ecosystem services and natural capital. *Nature*, 387, 253–260. "
        "[doi:10.1038/387253a0](https://doi.org/10.1038/387253a0)",
        "Díaz, S., Pascual, U., Stenseke, M., Martín-López, B., Watson, R. T., Molnár, Z., et al. (2018). "
        "Assessing nature's contributions to people. *Science*, 359, 270–272. "
        "[doi:10.1126/science.aap8826](https://doi.org/10.1126/science.aap8826)",
    ],
    "note": "Game models in Chapters 4–6 illustrate ideas from the papers; they are not data.",
    "values": "Values in 1994 US dollars — roughly double in today's money.",
}

SHARE = {
    "title": "📱 Scan to join",
    "no_url": "No app address yet. After deploying, set `APP_URL` in `config.py` to your app address "
              "(for example `https://your-app.streamlit.app`) and push.",
}

COMMON = {
    "learn": "📖 Learn",
    "play": "🎮 Play: {title}",
    "remember": "💡 **Remember:** {text}",
    "more": "📚 Want to know more?",
    "back": "← Back",
    "next": "Next →",
    "chapter_of": "Chapter {n} of {total}",
    "speaker_notes": "🎤 Speaker notes",
}
