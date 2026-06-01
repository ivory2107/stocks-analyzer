from pathlib import Path
import sys
import pandas as pd

sys.path.append(str(Path(__file__).resolve().parent))

from dashboard import (
    load_stock_data,
    select_price_column,
    add_moving_average,
    detect_anomalies,
    train_simple_forecast,
    plot_stock_dashboard,
)


def run_quick_test() -> dict:
    repo_root = Path(__file__).resolve().parent.parent
    csv_path = repo_root / "data" / "sample" / "stock_log (1).csv"

    df = load_stock_data(csv_path)
    rows_loaded = len(df)

    price_col = select_price_column(df)

    df = add_moving_average(df, price_col, window=10)
    df = detect_anomalies(df, price_col, window=10, threshold=4.0)
    sma_cols = [c for c in df.columns if c.startswith("SMA_")]
    anomalies = int(df["Anomaly"].sum())

    forecast = train_simple_forecast(df, price_col, days_ahead=3)
    forecast_rows = len(forecast)

    out = Path(__file__).resolve().parent / "test_output.png"
    combined = pd.concat([df, forecast], ignore_index=True, sort=False)
    plot_stock_dashboard(combined, price_col, output_path=out, title="Quick Test Plot", show=False)

    passed = rows_loaded > 0 and bool(price_col) and forecast_rows > 0

    result = {
        "csv_path": str(csv_path),
        "rows_loaded": rows_loaded,
        "price_column": price_col,
        "sma_columns": sma_cols,
        "anomalies_detected": anomalies,
        "forecast_rows": forecast_rows,
        "output_image": str(out),
        "test_passed": passed,
        "summary": "PASS" if passed else "FAIL",
    }

    print("Test summary:")
    for key, value in result.items():
        print(f"  {key}: {value}")

    return result


if __name__ == "__main__":
    run_quick_test()
