# 🌍 Nature Value Explorer

A 5-minute interactive journey through **ecosystem services**, made by Group 9 for our
presentation on *biodiversity ↔ ecosystem functioning/services*.

Guiding question: *From services to contributions: valuing nature in a human world.*

The app is **mobile-first**: during the talk we show a big QR code, classmates scan it and go
through the chapters on their own phones while each presenter leads their chapter. No formulas,
no sliders — just short texts, buttons and mini-games.

| # | Chapter | Presenter | Mini-game |
|---|---------|-----------|-----------|
| 0 | 🏠 Welcome | — | Start button and chapter list |
| 1 | ☕ Nature in your morning | Julie | Tap what you used this morning |
| 2 | 💰 What is nature worth? | Goda | Guess the price · Which is worth more? |
| 3 | 🚜 Build or keep? | Goda | Make the trade |
| 4 | 💥 The tipping point game | Munkhtulga | How much can you take? |
| 5 | 🌉 From services to contributions | Munkhtulga / 2D | Good or bad? · Nature or culture? · Who decides? |
| 6 | 🛠️ Solutions | 2D | Save the forest · Six real solutions · What can you do? |
| 7 | 🏆 Quiz & finish | — | 5 easy questions and a badge |

Extra pages in the menu: 📖 Glossary, 📚 Sources, 📱 Share (big QR code for the projector).

## Run locally

Requires Python 3.11+.

```bash
pip install -r requirements.txt
streamlit run app.py
```

Run the tests:

```bash
pytest
```

## Deploy on Streamlit Community Cloud

1. Push this repository to a **public** GitHub repository.
2. Go to <https://share.streamlit.io>, sign in with GitHub, click **Create app** →
   **Deploy a public app from GitHub**.
3. Pick the repository, branch `main`, main file `app.py`, and optionally a custom URL
   (e.g. `nature-value-explorer.streamlit.app`). Click **Deploy**.
4. Set `APP_URL` in [`config.py`](config.py) to the app address, commit and push.
   The 📱 Share page now shows the QR code. Streamlit redeploys automatically after each push.

## For presenters

- Open the app with **`?presenter=1`** at the end of the address
  (e.g. `https://nature-value-explorer.streamlit.app/?presenter=1`) to see 🎤 speaker notes at
  the top of each chapter. Students never see them.
- Put the 📱 **Share** page on the projector so everyone can scan the QR code.

## Editing texts

All interface texts live in [`content/texts.py`](content/texts.py). Change wording there
without touching the app logic. Numbers come from [`data/biomes.csv`](data/biomes.csv),
[`data/lost_services.csv`](data/lost_services.csv) and [`config.py`](config.py).

## Project structure

```
app.py                  page config, global CSS, navigation, presenter flag
config.py               totals, app URL
.streamlit/config.toml  light theme, minimal toolbar
data/                   Costanza et al. 1997, Table 2 (values per hectare per year, 1994 US$)
content/texts.py        all interface texts (English)
utils/games.py          pure game logic (tested)
utils/ui.py             shared components and mobile CSS
pages/                  one file per chapter + glossary, sources, share
tests/                  pytest: game logic + page smoke tests
```

The games in Chapters 4–6 are models that illustrate ideas from the papers; they are not data.

## Sources

- Costanza, R., d'Arge, R., de Groot, R., Farber, S., Grasso, M., Hannon, B., Limburg, K.,
  Naeem, S., O'Neill, R. V., Paruelo, J., Raskin, R. G., Sutton, P., & van den Belt, M. (1997).
  The value of the world's ecosystem services and natural capital. *Nature*, 387, 253–260.
  <https://doi.org/10.1038/387253a0>
- Díaz, S., Pascual, U., Stenseke, M., Martín-López, B., Watson, R. T., Molnár, Z., et al.
  (2018). Assessing nature's contributions to people. *Science*, 359, 270–272.
  <https://doi.org/10.1126/science.aap8826>

## Group 9

| Section | Presenter |
|---------|-----------|
| Introduction | Julie |
| Calculation of value | Goda |
| Hypothesis | Munkhtulga |
| Solutions | 2D |
