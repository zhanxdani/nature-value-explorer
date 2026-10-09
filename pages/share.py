import streamlit as st

import config
from content import texts as T
from utils import ui

st.title(T.SHARE["title"])
if config.APP_URL:
    st.image(ui.qr_png(config.APP_URL), **ui.stretch(st.image))
    st.markdown(f'<div class="qr-url">{ui.html_text(config.APP_URL)}</div>', unsafe_allow_html=True)
else:
    st.info(T.SHARE["no_url"])

ui.page_link(ui.PAGES[0], "🏠 Back to the start")
