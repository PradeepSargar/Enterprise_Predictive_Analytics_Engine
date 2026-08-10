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

# Color Palette (Sky Blue, Light Purple, Light Grey Canvas)
PRIMARY_COLOR = "#0EA5E9"      # Modern Sky Blue
PRIMARY_DARK = "#0284C7"       # Deep Sky Blue
PRIMARY_LIGHT = "#E0F2FE"      # Soft Sky Tint

SECONDARY_COLOR = "#A855F7"    # Light Purple / Violet
SECONDARY_DARK = "#7E22CE"     # Deep Purple
SECONDARY_LIGHT = "#F3E8FF"    # Soft Lavender Tint

SUCCESS_COLOR = "#10B981"      # Emerald Teal
WARNING_COLOR = "#F59E0B"      # Amber
DANGER_COLOR = "#EF4444"       # Coral Red
INFO_COLOR = "#38BDF8"         # Bright Sky Blue

BG_LIGHT_GREY = "#F8FAFC"      # Clean Slate-50
SURFACE_LIGHT_GREY = "#F1F5F9" # Muted Slate-100
BORDER_LIGHT_GREY = "#E2E8F0"  # Subtle Border Slate-200

TEXT_PRIMARY = "#0F172A"       # Deep Slate 900
TEXT_SECONDARY = "#475569"     # Muted Slate 600
TEXT_COLOR = "#0F172A"
MUTED_TEXT_COLOR = "#64748B"
GRID_COLOR = "#E2E8F0"

CHART_PALETTE = [
    "#0EA5E9",  # Sky Blue
    "#A855F7",  # Light Purple
    "#38BDF8",  # Light Sky
    "#C084FC",  # Soft Lavender
    "#10B981",  # Emerald
    "#F59E0B",  # Amber
    "#EC4899",  # Pink
    "#6366F1",  # Indigo
    "#14B8A6",  # Teal
    "#8B5CF6",  # Violet
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
