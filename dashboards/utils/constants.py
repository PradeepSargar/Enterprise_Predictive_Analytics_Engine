"""
Application Constants
=====================
Enterprise Predictive Analytics Engine
"""

from __future__ import annotations

# Currency & Formatting
CURRENCY_SYMBOL = "R$"
CURRENCY_NAME = "BRL"
DEFAULT_DECIMAL_PLACES = 2

# Risk & Classification Thresholds
LOW_REVIEW_THRESHOLD = 2
RISK_PROBABILITY_THRESHOLD = 0.40

# Color Palette
PRIMARY_COLOR = "#2563EB"
SECONDARY_COLOR = "#7C3AED"
SUCCESS_COLOR = "#059669"
WARNING_COLOR = "#D97706"
DANGER_COLOR = "#DC2626"
INFO_COLOR = "#0891B2"

TEXT_PRIMARY = "#0F172A"
TEXT_SECONDARY = "#475569"
GRID_COLOR = "#E2E8F0"

# Segment Profile Labels
SEGMENT_NAMES = {
    0: "Recent One-Time Buyers",
    1: "Lapsed / At Risk",
    2: "Loyal Repeat Customers",
    3: "High-Value Outliers",
}

# Top Categories and Regions Defaults
DEFAULT_CATEGORIES = [
    "bed_bath_table",
    "health_beauty",
    "sports_leisure",
    "computers_accessories",
    "furniture_decor",
]

DEFAULT_STATES = ["SP", "RJ", "MG", "RS", "PR"]
