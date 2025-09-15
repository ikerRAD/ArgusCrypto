import streamlit as st
from app.components.sidebar import render_sidebar

from app.components.static_chart import render_static_chart

from app.components.live_chart import render_live_chart

st.set_page_config(
    page_title="Argus Crypto",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.title("Crypto Dashboard")

render_sidebar()

start_char: bool = st.session_state.start_chart
streaming: bool = st.session_state.streaming_active
if start_char:
    if streaming:
        render_live_chart()
    else:
        render_static_chart()
