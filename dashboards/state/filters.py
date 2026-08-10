"""
Centralized Session State & Filter Management
==============================================
Enterprise Predictive Analytics Engine
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
import streamlit as st


FILTER_KEYS = {
    "date_range": "global_filter_date_range",
    "selected_categories": "global_filter_categories",
    "selected_states": "global_filter_states",
    "min_review_score": "global_filter_min_review_score",
}


def init_filter_state():
    """
    Initialize default session state keys if not already present.
    """
    if "filters_initialized" not in st.session_state:
        st.session_state["filters_initialized"] = True
        st.session_state[FILTER_KEYS["date_range"]] = None
        st.session_state[FILTER_KEYS["selected_categories"]] = []
        st.session_state[FILTER_KEYS["selected_states"]] = []
        st.session_state[FILTER_KEYS["min_review_score"]] = 1


def get_filter(key: str, default: Any = None) -> Any:
    """
    Retrieve filter value safely from Streamlit session state.
    """
    session_key = FILTER_KEYS.get(key, key)
    return st.session_state.get(session_key, default)


def set_filter(key: str, value: Any) -> None:
    """
    Store filter value into Streamlit session state.
    """
    session_key = FILTER_KEYS.get(key, key)
    st.session_state[session_key] = value


def reset_all_filters() -> None:
    """
    Reset all filters to default empty states.
    """
    st.session_state[FILTER_KEYS["date_range"]] = None
    st.session_state[FILTER_KEYS["selected_categories"]] = []
    st.session_state[FILTER_KEYS["selected_states"]] = []
    st.session_state[FILTER_KEYS["min_review_score"]] = 1
