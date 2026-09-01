"""
Enterprise Predictive Analytics Engine
=======================================
Root Streamlit Entry Point

This file serves as the top-level entry point for Streamlit Cloud and standard
local runs (`streamlit run app.py`). It configures paths and executes the main
dashboard controller from `dashboards/app.py`.
"""

import runpy
import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Execute the primary multi-page dashboard application
DASHBOARD_APP = PROJECT_ROOT / "dashboards" / "app.py"
runpy.run_path(str(DASHBOARD_APP), run_name="__main__")
