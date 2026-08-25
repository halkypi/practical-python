from pathlib import Path
import csv

import streamlit as st


DATA_DIR = Path(__file__).resolve().parents[2] / "Data"


@st.cache_data
def read_portfolio(filename=DATA_DIR / "portfolio.csv"):
    portfolio = []
    with open(filename, newline="") as file:
        rows = csv.DictReader(file)
        for row in rows:
            if not row or not row.get("name"):
                continue
            portfolio.append(
                {
                    "name": row["name"],
                    "shares": int(row["shares"]),
                    "price": float(row["price"]),
                }
            )
    return portfolio


@st.cache_data
def read_prices(filename=DATA_DIR / "prices.csv"):
    prices = {}
    with open(filename, newline="") as file:
        rows = csv.reader(file)
        for row in rows:
            if not row or not any(item.strip() for item in row):
                continue
            name, price = row
            prices[name] = float(price)
    return prices


def make_report():
    report = []
    prices = read_prices()
    for holding in read_portfolio():
        current_price = prices[holding["name"]]
        cost = holding["shares"] * holding["price"]
        value = holding["shares"] * current_price
        report.append(
            {
                "name": holding["name"],
                "shares": holding["shares"],
                "purchase_price": holding["price"],
                "current_price": current_price,
                "cost": cost,
                "value": value,
                "change": value - cost,
            }
        )
    return report


def selected_report():
    selected = st.session_state.get("selected_stocks", [])
    return [row for row in make_report() if row["name"] in selected]


def summarize(report):
    total_cost = sum(row["cost"] for row in report)
    total_value = sum(row["value"] for row in report)
    return total_cost, total_value, total_value - total_cost

