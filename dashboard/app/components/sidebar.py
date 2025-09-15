from datetime import datetime, time, date
import streamlit as st
from app.data.backend_rest_client import BackendRestClient
from requests import HTTPError

from app.data.schemas.ticker import Ticker
from app.settings import BACKEND_URL


def render_sidebar() -> None:
    st.sidebar.header("Chart Options")
    st.sidebar.subheader("Price Options")

    __initialize_states()
    __initialize_sidebar()

    # DEBUG
    '''st.text(
        f"""
    selected_exchange_id->{st.session_state.selected_exchange_id}
    selected_symbol_id->{st.session_state.selected_symbol_id}
    selected_ticker_id->{st.session_state.selected_ticker_id}
    streaming_active->{st.session_state.streaming_active}
    start_chart->{st.session_state.start_chart}
    start_date->{st.session_state.start_date}
    end_date->{st.session_state.end_date}
    last_minutes->{st.session_state.last_minutes}
    """
    )'''


def __initialize_states() -> None:
    if "selected_exchange_id" not in st.session_state:
        st.session_state.selected_exchange_id = None
    if "selected_symbol_id" not in st.session_state:
        st.session_state.selected_symbol_id = None
    if "selected_ticker_id" not in st.session_state:
        st.session_state.selected_ticker_id = None
    if "streaming_active" not in st.session_state:
        st.session_state.streaming_active = False
    if "start_chart" not in st.session_state:
        st.session_state.start_chart = False
    if "start_date" not in st.session_state:
        st.session_state.start_date = None
    if "end_date" not in st.session_state:
        st.session_state.end_date = None
    if "last_minutes" not in st.session_state:
        st.session_state.last_minutes = None


def __initialize_sidebar() -> None:
    rest_client = BackendRestClient(BACKEND_URL)

    try:
        exchanges = rest_client.get_all_exchanges()
        symbols = rest_client.get_all_symbols()
    except HTTPError:
        st.sidebar.error("Failed connecting to the server. Try again later.")
        return

    if not exchanges or not symbols:
        st.sidebar.warning("There are no Exchanges or Symbols yet.")
        return

    exchanges_map = {exchange.id: exchange for exchange in exchanges}
    exchange_ids = [None] + list(exchanges_map.keys())

    symbols_map = {symbol.id: symbol for symbol in symbols}
    symbol_ids = [None] + list(symbols_map.keys())

    selected_exchange_id = st.sidebar.selectbox(
        "Select an Exchange",
        options=exchange_ids,
        format_func=lambda exchange_id: exchanges_map[exchange_id].name
        if exchange_id
        else "",
    )

    selected_symbol_id = st.sidebar.selectbox(
        "Select a Symbol",
        options=symbol_ids,
        format_func=lambda symbol_id: symbols_map[symbol_id].symbol
        if symbol_id
        else "",
    )

    if (
        selected_exchange_id != st.session_state.selected_exchange_id
        or selected_symbol_id != st.session_state.selected_symbol_id
    ):
        st.session_state.selected_exchange_id = selected_exchange_id
        st.session_state.selected_symbol_id = selected_symbol_id
        st.session_state.selected_ticker_id = None
        st.session_state.streaming_active = False
        st.session_state.start_chart = False
        st.session_state.start_date = None
        st.session_state.end_date = None
        st.session_state.last_minutes = None

    if not selected_exchange_id or not selected_symbol_id:
        return

    tickers: list[Ticker]
    try:
        tickers = rest_client.get_all_tickers_by_exchange_id(selected_exchange_id)
    except HTTPError:
        st.sidebar.error("Failed connecting to the server. Try again later.")
        return

    available_tickers = {
        ticker.id: ticker.ticker
        for ticker in tickers
        if ticker.symbol_id == selected_symbol_id
    }

    if not available_tickers:
        st.sidebar.warning("No tickers found for this pair. Please select another.")
        return

    available_ticker_ids_map = [None] + list(available_tickers.keys())

    selected_ticker_id = st.sidebar.selectbox(
        "Select a Ticker",
        options=available_ticker_ids_map,
        format_func=lambda ticker_id: available_tickers[ticker_id] if ticker_id else "",
    )

    if selected_ticker_id != st.session_state.selected_ticker_id:
        st.session_state.selected_ticker_id = selected_ticker_id

    if not selected_ticker_id:
        return

    st.session_state.start_chart = True

    st.sidebar.markdown("---")
    st.sidebar.subheader("Data Options")

    is_streaming_active = st.sidebar.checkbox("Live Streaming")
    st.session_state.streaming_active = is_streaming_active

    if is_streaming_active:
        st.session_state.last_minutes = st.sidebar.number_input(
            "Last minutes of data", min_value=0, value=st.session_state.last_minutes
        )
    else:
        start_date = st.sidebar.date_input(
            "Start Date - UTC",
            value=st.session_state.start_date.date()
            if st.session_state.start_date is not None
            else None,
            max_value=date.today(),
        )

        if start_date:
            start_date_time = st.sidebar.time_input(
                "Start Date's time",
                value=st.session_state.start_date.time()
                if st.session_state.start_date is not None
                else None,
            )

            if start_date_time:
                st.session_state.start_date = datetime.combine(
                    start_date, start_date_time
                )
            else:
                st.session_state.start_date = datetime.combine(
                    start_date, time(0, 0, 0, 0)
                )

        end_date = st.sidebar.date_input(
            "End Date - UTC",
            value=st.session_state.end_date.date()
            if st.session_state.end_date is not None
            else None,
            max_value=date.today(),
        )

        if end_date:
            end_date_time = st.sidebar.time_input(
                "End Date's time",
                value=st.session_state.end_date.time()
                if st.session_state.end_date is not None
                else None,
            )

            if end_date_time:
                st.session_state.end_date = datetime.combine(end_date, end_date_time)
            else:
                st.session_state.end_date = datetime.combine(end_date, time(0, 0, 0, 0))
