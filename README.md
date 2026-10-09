# 🌿 Nature Value Explorer

An interactive Streamlit app for our group presentation on
**biodiversity ↔ ecosystem functioning/services**.

Guiding question: *From services to contributions: valuing nature in a human world.*

Six one-minute interactive pages plus a quiz. Each page has one main control, one big number
or chart, and one takeaway. It is built for the projector and also works on phones (open
it from the QR code in the sidebar).

| # | Page | Section | What it shows |
|---|------|---------|---------------|
| 1 | Guess the value | Introduction | Your guess vs. Costanza's $33T/yr vs. world GNP |
| 2 | Land converter | Calculating value | Services lost when nature becomes cropland or city |
| 3 | The future | Calculating value | How the discount rate changes the value of a hectare |
| 4 | Tipping point | Hypothesis | Marginal value rising sharply near a threshold *(illustrative model)* |
| 5 | Value lens | Hypothesis | Whose values count changes which land use "wins" *(illustrative model)* |
| 6 | Deal builder | Solutions | Payments for Ecosystem Services: is there a win-win deal? |
| 7 | Quiz | — | 6 questions on both papers |

## Screenshots

_Add screenshots here after deploying._

| Guess the value | Tipping point | Deal builder |
|---|---|---|
| ![](docs/screenshot-guess.png) | ![](docs/screenshot-tipping.png) | ![](docs/screenshot-deal.png) |

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
3. Pick the repository, branch `main`, main file `app.py`. Optionally choose a custom
   URL (e.g. `nature-value-explorer.streamlit.app`). Click **Deploy**.
4. Copy the app URL into `APP_URL` in [`config.py`](config.py), commit and push.
   The QR code in the sidebar (**Open on your phone**) now works.

## Settings in the sidebar

- **Show in today's dollars**: all amounts are in 1994 US$, as in the paper. The toggle
  multiplies them by `CPI_FACTOR` (2.12, CPI-U 1994 → 2024). Update it in `config.py`.
- **Presenter mode**: bigger fonts for the projector; hides speaker notes and source lines.

## Project structure

```
app.py              navigation, sidebar, global CSS, QR code
config.py           constants (totals, CPI factor, app URL)
data/biomes.csv     Costanza et al. 1997, Table 2: value per hectare by biome
data/services.csv   Costanza et al. 1997, Table 2: global value by service
utils/calc.py       pure calculation functions (tested)
utils/ui.py         shared UI helpers
pages/              one file per page
tests/              pytest: calculations + page smoke tests
```

Every number on screen comes from `data/*.csv` or `config.py`, or is calculated from them.
Pages 4, 5 and 6 contain illustrative models, and they are labelled in the app.

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
