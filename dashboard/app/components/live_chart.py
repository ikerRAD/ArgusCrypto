import threading
import time
import json
from datetime import datetime, timedelta, timezone
import plotly.express as px

import streamlit as st
import pandas as pd
from requests import HTTPError
from websocket import create_connection

from app.data.schemas.price import Price

from app.data.backend_rest_client import BackendRestClient

from app.data.schemas.ticker import Ticker

from app.data.schemas.exchange import Exchange
from app.settings import (
    BACKEND_WEBSOCKET_URL,
    REAL_TIME_CHART_REFRESH_INTERVAL,
    DEFAULT_LAST_MINUTES,
    BACKEND_URL,
)
from queue import Queue


data_queue = Queue()


def render_live_chart() -> None:
    rest_client = BackendRestClient(BACKEND_URL)

    ticker_id = st.session_state.selected_ticker_id
    if ticker_id is None:
        st.error("Cannot load chart as there is no ticker selected")
        return

    ticker: Ticker | None = None
    exchange: Exchange | None = None
    try:
        ticker = rest_client.get_ticker_by_id(ticker_id)
        exchange = rest_client.get_exchange_by_id(ticker.exchange_id)
    except HTTPError:
        st.warning("Cannot load ticker information from server")

    if (
        "websocket_thread" not in st.session_state
        or not st.session_state.websocket_thread.is_alive()
    ):
        st.session_state.websocket_thread = threading.Thread(
            target=__websocket_data,
            args=(ticker_id, st.session_state.last_minutes),
            daemon=True,
        )
        st.session_state.websocket_thread.start()

    last_minutes = st.session_state.last_minutes or DEFAULT_LAST_MINUTES

    if "data" not in st.session_state:
        st.session_state.data = pd.DataFrame(
            columns=["id", "ticker_id", "price", "timestamp"]
        )

    try:
        while not data_queue.empty():
            new_price = Price(**data_queue.get(block=False))
            new_rof_df = pd.DataFrame([new_price])
            new_rof_df["timestamp"] = pd.to_datetime(
                new_rof_df["timestamp"]
            ).dt.tz_localize(timezone.utc)
            st.session_state.data = pd.concat([st.session_state.data, new_rof_df])
            data_queue.task_done()
    except Exception:
        st.error("Error processing live data")

    if not st.session_state.data.empty:
        instant = datetime.now(timezone.utc)
        time_difference = instant - st.session_state.data["timestamp"]
        st.session_state.data = st.session_state.data[
            time_difference < timedelta(minutes=last_minutes)
        ]
        st.session_state.data = st.session_state.data.reset_index(drop=True)

    fig = px.line(
        st.session_state.data,
        x="timestamp",
        y="price",
        title=f"Real-Time Prices of {ticker.ticker if ticker else 'UNKNOWN'} in {exchange.name if exchange else 'UNKNOWN'}",
        labels={"timestamp": "Date and Time", "price": "Price"},
    )

    fig.update_layout(
        xaxis_title="Date and Time - UTC",
        yaxis_title=f"{ticker.ticker if ticker else 'UNKNOWN'}",
    )
    st.plotly_chart(fig, use_container_width=True)

    time.sleep(REAL_TIME_CHART_REFRESH_INTERVAL)
    st.rerun()


def __websocket_data(ticker_id: None | int, last_minutes: None | int) -> None:
    ws_url_template = BACKEND_WEBSOCKET_URL + "/v1/tickers/{ticker_id}/prices/ws"
    url = ws_url_template.format(ticker_id=ticker_id)

    if last_minutes is not None:
        url = f"{url}?last_minutes={last_minutes}"

    try:
        ws = create_connection(url)
        while True:
            message = ws.recv()
            if not message:
                time.sleep(REAL_TIME_CHART_REFRESH_INTERVAL)
                continue

            data_queue.put(json.loads(message))
    except Exception:
        print("Websocket error!")
