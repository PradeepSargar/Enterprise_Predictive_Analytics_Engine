"""
Enterprise Predictive Analytics Engine
---------------------------------------

Main Streamlit application entry point.

This file is responsible for:

1. Configuring the Streamlit application.
2. Loading the global design system.
3. Defining the dashboard navigation.
4. Running the selected dashboard page.

Page-specific analytics should remain inside the individual
files under dashboards/pages/.
"""

import streamlit as st

from dashboards.styles.theme import inject_global_styles


# =====================================================================
# APPLICATION CONFIGURATION
# =====================================================================

# Configure the application before rendering any dashboard content.
# Wide mode gives analytics visualizations enough horizontal space.
st.set_page_config(
    page_title="Enterprise Predictive Analytics Engine",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =====================================================================
# GLOBAL DESIGN SYSTEM
# =====================================================================

# Apply the centralized CSS theme to the entire application.
inject_global_styles()


# =====================================================================
# APPLICATION NAVIGATION
# =====================================================================

# Each page is explicitly registered here.
#
# This gives us complete control over:
#   - Page order
#   - Navigation labels
#   - Icons
#   - Navigation groups
#
# The actual analytical logic stays inside each page file.

pages = {
    "Overview": [
        st.Page(
            "dashboards/pages/01_Executive_Overview.py",
            title="Executive Overview",
            icon=":material/dashboard:",
            default=True,
        ),
    ],

    "Customer Intelligence": [
        st.Page(
            "dashboards/pages/02_Customer_Analytics.py",
            title="Customer Analytics",
            icon=":material/groups:",
        ),
        st.Page(
            "dashboards/pages/03_Customer_Risk.py",
            title="Customer Risk",
            icon=":material/security:",
        ),
    ],

    "Predictive Intelligence": [
        st.Page(
            "dashboards/pages/04_Revenue_Forecast.py",
            title="Revenue Forecast",
            icon=":material/monitoring:",
        ),
        st.Page(
            "dashboards/pages/05_Model_Performance.py",
            title="Model Performance",
            icon=":material/model_training:",
        ),
    ],

    "Data": [
        st.Page(
            "dashboards/pages/06_Data_Explorer.py",
            title="Data Explorer",
            icon=":material/table_view:",
        ),
    ],
}


# =====================================================================
# RUN THE SELECTED PAGE
# =====================================================================

# st.navigation() creates the application's sidebar navigation.
# The selected page is then executed with page.run().
page = st.navigation(
    pages,
    position="sidebar",
)

page.run()