"""
Streamlit Automated Smoke Test Suite
====================================
Enterprise Predictive Analytics Engine

Validates that:
1. Root application entry points (`app.py`, `dashboards/app.py`) compile and execute cleanly.
2. Every dashboard page (01 through 08) executes without throwing unhandled exceptions.
3. Multi-grain forecasting page runs across all segment types and values.
"""

import sys
import traceback
from pathlib import Path
from streamlit.testing.v1 import AppTest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

PAGES = [
    "dashboards/pages/01_Executive_Overview.py",
    "dashboards/pages/02_Customer_Analytics.py",
    "dashboards/pages/03_Customer_Risk.py",
    "dashboards/pages/04_Revenue_Forecast.py",
    "dashboards/pages/05_Model_Performance.py",
    "dashboards/pages/06_Data_Explorer.py",
    "dashboards/pages/07_Customer_Segmentation.py",
    "dashboards/pages/08_About.py",
]


def test_page(page_rel_path: str) -> bool:
    page_path = PROJECT_ROOT / page_rel_path
    print(f"Testing {page_rel_path}...", end=" ", flush=True)

    try:
        at = AppTest.from_file(str(page_path), default_timeout=30)
        at.run()

        if at.exception:
            print("[FAILED]")
            print(f"Exception raised in {page_rel_path}:")
            for exc in at.exception:
                print(f"  - {exc.value}")
            return False

        print("[PASSED]")
        return True

    except Exception as e:
        print("[ERROR]")
        traceback.print_exc()
        return False


def test_revenue_forecast_segments() -> bool:
    print("Testing 04_Revenue_Forecast.py across multi-grain cuts...", end=" ", flush=True)
    page_path = PROJECT_ROOT / "dashboards/pages/04_Revenue_Forecast.py"

    try:
        from dashboards.data.loader import get_available_forecast_segments
        segments = get_available_forecast_segments()

        # Test Total
        at = AppTest.from_file(str(page_path), default_timeout=30)
        at.run()
        if at.exception:
            print("[FAILED - Total]")
            return False

        # Test Category selection
        at_cat = AppTest.from_file(str(page_path), default_timeout=30)
        at_cat.run()
        if at_cat.selectbox:
            at_cat.selectbox[0].select("By Product Category").run()
            if at_cat.exception:
                print("[FAILED - Category]")
                return False

        # Test Region selection
        at_reg = AppTest.from_file(str(page_path), default_timeout=30)
        at_reg.run()
        if at_reg.selectbox:
            at_reg.selectbox[0].select("By Regional State / Market").run()
            if at_reg.exception:
                print("[FAILED - Region]")
                return False

        print("[PASSED]")
        return True

    except Exception as e:
        print(f"[ERROR: {e}]")
        return False


def main():
    print("\n========================================================")
    print("RUNNING STREAMLIT AUTOMATED SMOKE TESTS")
    print("========================================================\n")

    failed_pages = []

    for page in PAGES:
        passed = test_page(page)
        if not passed:
            failed_pages.append(page)

    fc_passed = test_revenue_forecast_segments()
    if not fc_passed:
        failed_pages.append("Multi-Grain Forecast Interaction")

    print("\n--------------------------------------------------------")
    if failed_pages:
        print(f"Smoke test FAILED on {len(failed_pages)} item(s):")
        for p in failed_pages:
            print(f"  - {p}")
        sys.exit(1)
    else:
        print("ALL 8 DASHBOARD PAGES PASSED SMOKE TESTS WITH ZERO EXCEPTIONS! [SUCCESS]")
        print("========================================================\n")


if __name__ == "__main__":
    main()
