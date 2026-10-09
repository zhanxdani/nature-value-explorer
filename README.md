# 🌍 Nature Value Explorer

A 5-minute mobile game about the value of nature, made by Group 9 for our presentation on
*biodiversity ↔ ecosystem functioning/services*.

Guiding question: *From services to contributions: valuing nature in a human world.*

During the talk we show a QR code; classmates play on their own phones while each presenter
leads their chapter. **Every screen fits on a phone without scrolling.** Each slider shows
**what happens** (the picture changes, consequence bars move) and **who approves** (a row of
characters with approval rings). Longer explanations open in pop-ups (ⓘ, Why?, ☰).

| Chapter | Screens | Presenter |
|---------|---------|-----------|
| 1 · Nature in your morning | What did you use today? · What if bees disappeared? | Julie |
| 2 · What is nature worth? | Guess the price · Which is worth more? | Goda |
| 3 · Build or keep? | Drain the wetland (+ Big storm!) | Goda |
| 4 · The tipping point | How much forest can you clear? | Munkhtulga |
| 5 · From services to contributions | Good or bad? · Nature or culture? · Who decides? | Munkhtulga / 2D |
| 6 · Solutions | Save the forest · Grey vs green · Six real solutions · What can you do? | 2D |
| 7 · Quiz & finish | 5 questions · badge | — |

## Run locally

Requires Python 3.11+.

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open a screen directly with `?s=<id>`, e.g. `http://localhost:8501/?s=6.1`.

## Tests

```bash
pytest
```

- `tests/test_games.py` — game logic (tipping point, deals, wetland, who decides, higher/lower).
- `tests/test_screens.py` — every screen renders (also in presenter mode and with no images).
- `tests/test_no_scroll.py` — opens every screen and game state in headless Chromium at
  375×667 and 390×844 and checks nothing scrolls. It needs a browser once:
  `python -m playwright install chromium` (skipped if Playwright is missing).

## Deploy on Streamlit Community Cloud

1. Push this repository to a **public** GitHub repository.
2. Go to <https://share.streamlit.io>, sign in with GitHub, **Create app** →
   **Deploy a public app from GitHub**, pick the repo, branch `main`, file `app.py`.
3. Set `APP_URL` in [`config.py`](config.py) to the app address, commit and push.
   The ☰ menu → **Share** screen then shows a big QR code for the projector.

## For presenters

Add **`?presenter=1`** to the address (e.g. `https://…streamlit.app/?presenter=1`) to get a 🎤 button
with speaker notes in the top bar. Students never see it.

## Pictures

All pictures live in `static/img/` with the names listed in [`IMAGES.md`](IMAGES.md).
The app works without any picture (it shows emoji instead).

The 27 required pictures plus `hero` and `badge` are currently **drawn stand-ins** made by
[`tools/draw_standins.py`](tools/draw_standins.py) (simple flat vector drawings). To use real
artwork, generate it with the prompts in `IMAGES.md` and save it over the same file name
(WebP, sizes as listed). Redraw the stand-ins with:

```bash
python tools/draw_standins.py
```

## Editing

- Texts: [`content/texts.py`](content/texts.py)
- Approval and consequence tables: [`content/rules.py`](content/rules.py)
- Data: [`data/biomes.csv`](data/biomes.csv), [`data/wetland_services.csv`](data/wetland_services.csv)
  (Costanza et al. 1997, Table 2; US$ 1994 per hectare per year)

Approval levels and game models illustrate ideas from the papers; they are not data.

## Project structure

```
app.py                  page config, CSS, router, presenter flag
config.py               APP_URL and totals
.streamlit/config.toml  light theme, static file serving
static/img/             pictures (see IMAGES.md)
data/                   biomes.csv, wetland_services.csv
content/                texts.py, rules.py
utils/                  games.py (pure logic), img.py (pictures + fallbacks), ui.py (components, CSS)
screens/                one module per screen; order in screens/__init__.py
tools/                  draw_standins.py, measure.py (phone-size screenshots)
tests/                  test_games.py, test_screens.py, test_no_scroll.py
```

## Sources

- Costanza, R. et al. (1997). The value of the world's ecosystem services and natural capital.
  *Nature* 387, 253–260. <https://doi.org/10.1038/387253a0>
- Díaz, S. et al. (2018). Assessing nature's contributions to people. *Science* 359, 270–272.
  <https://doi.org/10.1126/science.aap8826>
- IPBES (2016). Assessment report on pollinators, pollination and food production.
- Ferrario, F. et al. (2014). The effectiveness of coral reefs for coastal hazard risk reduction and
  adaptation. *Nature Communications* 5, 3794. <https://doi.org/10.1038/ncomms4794>
- Menéndez, P. et al. (2020). The global flood protection benefits of mangroves. *Scientific Reports*
  10, 4404. <https://doi.org/10.1038/s41598-020-61136-6>

## Group 9

| Section | Presenter |
|---------|-----------|
| Introduction | Julie |
| Calculation of value | Goda |
| Hypothesis | Munkhtulga |
| Solutions | 2D |
