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

# Color Palette (Forest Signal: Trust & Growth-Oriented Design System)
PRIMARY_COLOR = "#1B4332"      # Deep Forest Green — Headers, Nav
PRIMARY_DARK = "#143628"       # Deep Forest Dark
PRIMARY_LIGHT = "#D8F3DC"      # Minty Light Tint
PRIMARY_SOFT = "#E9F5ED"       # Pale Mint Soft

ACCENT_COLOR = "#F4A261"       # Warm Amber — Alerts, CTAs, Highlights
ACCENT_DARK = "#E76F51"        # Terracotta Amber
ACCENT_LIGHT = "#FFE5D0"       # Soft Amber Tint

SECONDARY_COLOR = "#2D6A4F"    # Growth Emerald Forest
SECONDARY_DARK = "#1B4332"     # Forest Dark
SECONDARY_LIGHT = "#D8F3DC"    # Soft Mint Tint

SUCCESS_COLOR = "#2D6A4F"      # Growth Emerald
WARNING_COLOR = "#F4A261"      # Warm Amber
DANGER_COLOR = "#E63946"       # Crimson Coral Risk
INFO_COLOR = "#457B9D"         # Steel Ocean Slate

BG_LIGHT_GREY = "#F1FAEE"      # Pale Mint-White Canvas & Background
SURFACE_LIGHT_GREY = "#E8F3E8" # Pale Mint Surface Panel
BORDER_LIGHT_GREY = "#D0E3D5"  # Soft Mint-Slate Border

TEXT_PRIMARY = "#112211"       # Deep Forest Text 900
TEXT_SECONDARY = "#2D4A3E"     # Forest Slate 700
TEXT_COLOR = "#112211"
MUTED_TEXT_COLOR = "#52796F"   # Muted Sage Slate 500
GRID_COLOR = "#D0E3D5"

CHART_PALETTE = [
    "#1B4332",  # Deep Forest Green (Primary Series)
    "#F4A261",  # Warm Amber (Accent / CTAs / Highlights)
    "#2D6A4F",  # Growth Emerald (Secondary Series)
    "#457B9D",  # Steel Ocean (Comparison Cohort)
    "#E63946",  # Crimson Coral (Risk / Friction)
    "#52796F",  # Muted Sage (Baseline / Benchmark)
]

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
