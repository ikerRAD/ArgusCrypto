import streamlit as st
import pandas as pd
import plotly.express as px

from app.data.backend_rest_client import BackendRestClient

from app.data.schemas.ticker import Ticker
from requests import HTTPError

from app.data.schemas.exchange import Exchange
from app.settings import BACKEND_URL


def render_static_chart() -> None:
    rest_client = BackendRestClient(BACKEND_URL)

    if st.session_state.selected_ticker_id is None:
        st.error("Cannot load chart as there is no ticker selected")
        return

    ticker_id = st.session_state.selected_ticker_id
    start_date = st.session_state.start_date
    end_date = st.session_state.end_date
    price_df: pd.DataFrame
    try:
        price_df = pd.DataFrame(
            rest_client.get_all_prices_by_ticker_id(
                ticker_id, start_date=start_date, end_date=end_date
            )
        )
        if price_df.empty:
            st.warning("No price data available for the selected dates or ticker")
            return

        price_df["timestamp"] = pd.to_datetime(price_df["timestamp"])
    except HTTPError as e:
        if e.response.status_code == 400:
            st.error(e.response.json()["detail"])
        else:
            st.error(
                "Cannot load chart as there is an error fetching prices for ticker"
            )
        return

    ticker: Ticker | None = None
    exchange: Exchange | None = None
    try:
        ticker = rest_client.get_ticker_by_id(ticker_id)
        exchange = rest_client.get_exchange_by_id(ticker.exchange_id)
    except HTTPError:
        st.warning("Cannot load ticker information from server")

    fig = px.line(
        price_df,
        x="timestamp",
        y="price",
        title=f"Historic Prices of {ticker.ticker if ticker else 'UNKNOWN'} in {exchange.name if exchange else 'UNKNOWN'}",
        labels={"timestamp": "Date and Time - UTC", "price": "Price"},
    )

    fig.update_layout(
        xaxis_title="Date and Time",
        yaxis_title=f"{ticker.ticker if ticker else 'UNKNOWN'}",
    )

    st.plotly_chart(fig, use_container_width=True)
