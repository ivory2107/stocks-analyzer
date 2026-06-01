import argparse # users can specify a custom CSV file and output path trend
from datetime import datetime # convert dates to ordinal numbers
from pathlib import Path # handle file paths in a cross-platform way

import matplotlib.pyplot as plt # plotting library
import numpy as np # numerical operations, especially for anomaly detection
import pandas as pd # data manipulation and analysis
import seaborn as sns # statistical data visualization, on top of mathlib
from sklearn.linear_model import LinearRegression #simple linear regression model for forecasting

# loading stock data from a CSV file, ensuring date parsing and handling missing values
def load_stock_data(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path) # reads csv into the data frame
    if df.empty:
        raise ValueError(f"CSV file is empty: {csv_path}")

    # searches for columns that contain data information (has "date" or "time")
    # and converts them to datetime format.
    date_cols = [c for c in df.columns if "date" in c.lower() or "time" in c.lower()]
    if not date_cols:
        raise ValueError("Could not find a date column in the CSV. Rename it to Date or DateTime.")

    # converts column to datetime objects
    date_col = date_cols[0]
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    if df[date_col].isna().any():
        raise ValueError("Some date values could not be parsed. Check the CSV date format.")

    df = df.sort_values(date_col).reset_index(drop=True) # sort by dates
    df = df.dropna(subset=[date_col]) # drop rows with missing dates
    df = df.ffill().bfill()
    # fills missing values in other columns by forward and backward filling

    # standardises the date column name to "Date"
    return df.rename(columns={date_col: "Date"})

# selects the most appropriate price column from the dataframe, prioritising "Close" and "Adj Close"
def select_price_column(df: pd.DataFrame) -> str:
    for candidate in ["Close", "Adj Close", "close", "adj_close", "adjusted_close"]:
        if candidate in df.columns:
            return candidate

    # looks for columns that are commonly used for price data and selects the last one found
    price_cols = [c for c in df.columns if c.lower() in {"open", "high", "low", "close", "adj close", "volume"}]
    if "Close" in df.columns:
        return "Close"
    if price_cols:
        return price_cols[-1]

    raise ValueError("Could not find a price column. Expected Close, Adj Close, or similar.")

# adds a simple moving average (SMA) column to the dataframe based on the specified price column and window size
def add_moving_average(df: pd.DataFrame, price_col: str, window: int = 20) -> pd.DataFrame:
    df[f"SMA_{window}"] = df[price_col].rolling(window=window, min_periods=1).mean()
    return df

# detects anomalies in the price data using a rolling mean and standard deviation to calculate z-scores, 
# marking points that exceed the specified threshold as anomalies
def detect_anomalies(df: pd.DataFrame, price_col: str, window: int = 20, threshold: float = 3.0) -> pd.DataFrame:
    rolling_mean = df[price_col].rolling(window=window, min_periods=1).mean()
    rolling_std = df[price_col].rolling(window=window, min_periods=1).std().replace(0, np.nan)
    z_scores = (df[price_col] - rolling_mean) / rolling_std
    df["Anomaly"] = (z_scores.abs() > threshold).fillna(False)
    return df

# trains a simple linear regression model on the historical price data to predict future prices 
# for a specified number of business days ahead
def train_simple_forecast(df: pd.DataFrame, price_col: str, days_ahead: int = 5) -> pd.DataFrame:
    x = df["Date"].map(datetime.toordinal).to_numpy().reshape(-1, 1)
    y = df[price_col].to_numpy()
    model = LinearRegression()
    model.fit(x, y)

    last_date = df["Date"].iloc[-1]
    future_dates = pd.date_range(last_date + pd.Timedelta(days=1), periods=days_ahead, freq="B")
    x_future = future_dates.map(datetime.toordinal).to_numpy().reshape(-1, 1)
    prediction = model.predict(x_future)

    return pd.DataFrame({"Date": future_dates, price_col: prediction})

# plots the stock price data along with the moving average, anomalies, and forecasted values using seaborn and matplotlib
def plot_stock_dashboard(df: pd.DataFrame, price_col: str, output_path: Path | None = None, title: str = "Stock Price Dashboard", show: bool = True):
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(14, 8))

    sma_col = next((c for c in df.columns if c.startswith("SMA_")), None)
    anomaly_mask = df["Anomaly"].fillna(False).astype(bool) if "Anomaly" in df.columns else pd.Series(False, index=df.index, dtype=bool)
    anomaly_df = df[anomaly_mask].copy()
    forecast_df = df[df["Date"] > df["Date"].max()] if "Date" in df.columns else pd.DataFrame()

    ax = plt.gca()
    ax.plot(df["Date"], df[price_col], label=price_col, color="#2c7fb8", linewidth=2)
    if sma_col is not None:
        ax.plot(df["Date"], df[sma_col], label=sma_col, color="#dd1c77", linewidth=1.8, linestyle="--")

    if not anomaly_df.empty:
        ax.scatter(anomaly_df["Date"], anomaly_df[price_col], color="#fdae61", edgecolor="black", zorder=5, label="Anomaly", s=80)

    if not forecast_df.empty:
        ax.plot(forecast_df["Date"], forecast_df[price_col], label="Forecast", color="#238b45", linewidth=2, linestyle=":")
        ax.scatter(forecast_df["Date"], forecast_df[price_col], color="#238b45", s=50)

    ax.set_title(title, fontsize=18, pad=18)
    ax.set_xlabel("Date", fontsize=14)
    ax.set_ylabel(f"{price_col} Price", fontsize=14)
    ax.tick_params(axis="x", rotation=25)
    ax.legend(loc="upper left", fontsize=12)

    if "Volume" in df.columns:
        ax2 = ax.twinx()
        ax2.bar(df["Date"], df["Volume"], alpha=0.18, color="#6a3d9a", label="Volume")
        ax2.set_ylabel("Volume", fontsize=14)
        ax2.legend(loc="upper right", fontsize=12)

    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, dpi=200)
        print(f"Saved chart to {output_path}")
    if show:
        plt.show()
    else:
        plt.close()

# builds the dashboard by loading the stock data, adding the moving average, detecting anomalies, training the forecast model, and plotting the results
def build_dashboard(csv_path: Path, sma_window: int = 20, anomaly_threshold: float = 3.0, forecast_days: int = 5, output_path: Path | None = None):
    df = load_stock_data(csv_path)
    price_col = select_price_column(df)
    df = add_moving_average(df, price_col, window=sma_window)
    df = detect_anomalies(df, price_col, window=sma_window, threshold=anomaly_threshold)

    forecast_df = train_simple_forecast(df, price_col, days_ahead=forecast_days)
    combined_df = pd.concat([df, forecast_df], ignore_index=True, sort=False)

    plot_stock_dashboard(combined_df, price_col, output_path, title=f"{csv_path.stem} Trend + SMA + Forecast")

# parses command-line arguments to allow users to specify the CSV file, SMA window size, anomaly detection threshold, forecast days, 
# and output path for the chart image
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stock data dashboard with trends, moving average, anomaly detection, and a simple forecast.")
    parser.add_argument("--csv", type=Path, default=None, help="Path to the stock CSV file.")
    parser.add_argument("--window", type=int, default=20, help="SMA window size in days.")
    parser.add_argument("--threshold", type=float, default=3.0, help="Anomaly detection z-score threshold.")
    parser.add_argument("--forecast-days", type=int, default=5, help="Number of future business days to predict.")
    parser.add_argument("--output", type=Path, default=None, help="Optional path to save the generated chart image.")
    return parser.parse_args()

# main function to execute the dashboard building process based on command-line arguments or defaults
def main():
    args = parse_args()
    csv_path = args.csv
    if csv_path is None:
        csv_path = Path(__file__).resolve().parent.parent / "data" / "sample" / "stock_log (1).csv"

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    build_dashboard(csv_path, sma_window=args.window, anomaly_threshold=args.threshold, forecast_days=args.forecast_days, output_path=args.output)


if __name__ == "__main__":
    main()
