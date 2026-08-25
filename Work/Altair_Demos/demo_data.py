from pathlib import Path

import pandas as pd


DATA_DIR = Path(__file__).resolve().parents[1] / "Data"


def read_portfolio(filename=DATA_DIR / "portfolio.csv"):
    return pd.read_csv(filename)


def read_prices(filename=DATA_DIR / "prices.csv"):
    prices = pd.read_csv(filename, header=None, names=["name", "current_price"])
    return prices.dropna()


def load_portfolio_report():
    portfolio = read_portfolio()
    prices = read_prices()
    report = portfolio.merge(prices, on="name", how="inner")
    report = report.rename(columns={"price": "purchase_price"})
    report["cost"] = report["shares"] * report["purchase_price"]
    report["value"] = report["shares"] * report["current_price"]
    report["change"] = report["value"] - report["cost"]
    report["return_pct"] = report["change"] / report["cost"]
    report["result"] = report["change"].apply(lambda change: "Gain" if change >= 0 else "Loss")
    return report


def holdings_by_name(report):
    grouped = (
        report.groupby("name", as_index=False)
        .agg(
            shares=("shares", "sum"),
            cost=("cost", "sum"),
            value=("value", "sum"),
            change=("change", "sum"),
        )
        .sort_values("value", ascending=False)
    )
    grouped["return_pct"] = grouped["change"] / grouped["cost"]
    grouped["result"] = grouped["change"].apply(lambda change: "Gain" if change >= 0 else "Loss")
    return grouped


def price_history():
    rows = []
    base = {
        "AA": [31, 28, 24, 20, 18, 13, 9],
        "CAT": [82, 77, 69, 56, 47, 41, 35],
        "GE": [39, 35, 29, 22, 17, 15, 13],
        "IBM": [89, 94, 98, 100, 103, 105, 106],
        "MSFT": [50, 46, 38, 31, 27, 23, 21],
    }
    dates = pd.date_range("2007-01-01", periods=7, freq="QE")
    for name, prices in base.items():
        for date, price in zip(dates, prices):
            rows.append({"date": date, "name": name, "price": price})
    return pd.DataFrame(rows)


def sector_holdings():
    report = holdings_by_name(load_portfolio_report()).copy()
    sectors = {
        "AA": "Materials",
        "CAT": "Industrials",
        "GE": "Industrials",
        "IBM": "Technology",
        "MSFT": "Technology",
    }
    report["sector"] = report["name"].map(sectors)
    return report
