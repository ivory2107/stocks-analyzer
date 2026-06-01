import json
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent / "python-dashboard"))

from test_dashboard import run_quick_test


def main():
    result = run_quick_test()
    report_path = Path(__file__).resolve().parent / "dashboard_report.json"
    report_path.write_text(json.dumps(result, indent=2))

    print("Test report summary:")
    print(f"  summary: {result['summary']}")
    print(f"  rows_loaded: {result['rows_loaded']}")
    print(f"  price_column: {result['price_column']}")
    print(f"  anomalies_detected: {result['anomalies_detected']}")
    print(f"  forecast_rows: {result['forecast_rows']}")
    print(f"  output_image: {result['output_image']}")
    print(f"Saved dashboard report to: {report_path}")


if __name__ == "__main__":
    main()
