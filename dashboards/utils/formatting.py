"""
Number & Currency Formatting Utilities
======================================
Enterprise Predictive Analytics Engine
"""

from __future__ import annotations

from typing import Optional, Union
import pandas as pd


def format_currency(
    value: Optional[Union[int, float]],
    symbol: str = "R$",
    decimals: int = 0,
) -> str:
    """
    Format a numeric value as standard BRL currency string.
    Example: 1655885.0 -> 'R$1,655,885'
    """
    if value is None or pd.isna(value):
        return "N/A"
    try:
        val = float(value)
        if decimals == 0:
            return f"{symbol}{val:,.0f}"
        return f"{symbol}{val:,.{decimals}f}"
    except (ValueError, TypeError):
        return "N/A"


def format_percent(
    value: Optional[Union[int, float]],
    decimals: int = 1,
    signed: bool = False,
) -> str:
    """
    Format a proportion (0.0 to 1.0) as percentage string.
    Example: 0.1634 -> '16.3%'
    """
    if value is None or pd.isna(value):
        return "N/A"
    try:
        val = float(value) * 100
        sign = "+" if signed and val > 0 else ""
        return f"{sign}{val:.{decimals}f}%"
    except (ValueError, TypeError):
        return "N/A"


def format_number(
    value: Optional[Union[int, float]],
    decimals: int = 0,
) -> str:
    """
    Format a number with commas.
    Example: 113425 -> '113,425'
    """
    if value is None or pd.isna(value):
        return "N/A"
    try:
        val = float(value)
        if decimals == 0:
            return f"{val:,.0f}"
        return f"{val:,.{decimals}f}"
    except (ValueError, TypeError):
        return "N/A"


def format_date_month(value: Optional[Union[str, pd.Timestamp]]) -> str:
    """
    Format timestamp as readable month string.
    Example: '2018-09-01' -> 'Sep 2018'
    """
    if value is None or pd.isna(value):
        return "N/A"
    try:
        dt = pd.to_datetime(value)
        return dt.strftime("%b %Y")
    except Exception:
        return str(value)
