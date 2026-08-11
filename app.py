"""
Main Streamlit Application Launcher.

Redirects execution to the centralized application entry point at:
    dashboards/app.py
"""

from pathlib import Path
import runpy
import sys

# Ensure the project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Launch the official dashboard application
dashboard_app = PROJECT_ROOT / "dashboards" / "app.py"
runpy.run_path(str(dashboard_app), run_name="__main__")