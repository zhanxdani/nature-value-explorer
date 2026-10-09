"""Nature Value Explorer: entry point with navigation, sidebar, global CSS and QR code."""

from io import BytesIO

import qrcode
import streamlit as st

import config
from utils import ui

st.set_page_config(page_title="Nature Value Explorer", page_icon="🌿", layout="wide")

BASE_CSS = """
<style>
[data-testid="stMetricValue"] { font-size: 2.5rem; font-weight: 700; }
[data-testid="stMetricLabel"], [data-testid="stMetricLabel"] * {
    white-space: normal !important; overflow: visible !important; text-overflow: clip !important;
}
.illustrative-badge {
    display: inline-block; padding: 0.25rem 0.75rem; border-radius: 999px;
    background: #fab219; color: #0b0b0b; font-weight: 700; font-size: 0.9rem;
}
.big-text { font-size: 1.8rem; font-weight: 700; line-height: 1.3; }
</style>
"""

PRESENTER_CSS = """
<style>
html { font-size: 20px; }
[data-testid="stMetricValue"] { font-size: 3.2rem; }
[data-testid="stMetricLabel"] p { font-size: 1.15rem; }
.big-text { font-size: 2.4rem; }
</style>
"""


def qr_png(url: str) -> bytes:
    img = qrcode.make(url, box_size=8, border=2)
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


pages = {
    "1 · Introduction": [
        st.Page("pages/1_guess.py", title="Guess the value", icon="🌍", default=True),
    ],
    "2 · Calculating value": [
        st.Page("pages/2_converter.py", title="Land converter", icon="🚜"),
        st.Page("pages/3_future.py", title="The future", icon="⏳"),
    ],
    "3 · Hypothesis": [
        st.Page("pages/4_tipping_point.py", title="Tipping point", icon="⚠️"),
        st.Page("pages/5_value_lens.py", title="Value lens", icon="🔍"),
    ],
    "4 · Solutions": [
        st.Page("pages/6_deal_builder.py", title="Deal builder", icon="🤝"),
    ],
    "Quiz": [
        st.Page("pages/7_quiz.py", title="Quiz", icon="❓"),
    ],
}
pg = st.navigation(pages)

with st.sidebar:
    st.toggle(
        "Show in today's dollars",
        key="today_dollars",
        help=f"Multiplies every amount by {config.CPI_FACTOR} (CPI-U, 1994 → 2024).",
    )
    st.toggle(
        "Presenter mode",
        key="presenter",
        help="Bigger fonts for the projector; hides speaker notes and source captions.",
    )
    with st.expander("Open on your phone"):
        if config.APP_URL:
            st.image(qr_png(config.APP_URL), caption=config.APP_URL)
        else:
            st.info(
                "No URL yet. After deploying, set `APP_URL` in `config.py` "
                "to your app address (e.g. `https://your-app.streamlit.app`) and push."
            )
    st.divider()
    st.caption("**Sources**")
    st.caption(
        "Costanza, R., d'Arge, R., de Groot, R., Farber, S., Grasso, M., Hannon, B., "
        "Limburg, K., Naeem, S., O'Neill, R. V., Paruelo, J., Raskin, R. G., Sutton, P., "
        "& van den Belt, M. (1997). The value of the world's ecosystem services and "
        "natural capital. *Nature*, 387, 253–260. "
        "[doi:10.1038/387253a0](https://doi.org/10.1038/387253a0)"
    )
    st.caption(
        "Díaz, S., Pascual, U., Stenseke, M., Martín-López, B., Watson, R. T., Molnár, Z., "
        "et al. (2018). Assessing nature's contributions to people. *Science*, 359, 270–272. "
        "[doi:10.1126/science.aap8826](https://doi.org/10.1126/science.aap8826)"
    )

st.markdown(BASE_CSS, unsafe_allow_html=True)
if ui.presenter_mode():
    st.markdown(PRESENTER_CSS, unsafe_allow_html=True)

pg.run()
