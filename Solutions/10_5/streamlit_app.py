from pathlib import Path
import csv

import streamlit as st


DATA_DIR = Path(__file__).resolve().parents[2] / "Work" / "Data"


@st.cache_data
def read_portfolio(filename):
    with open(filename, newline="") as file:
        rows = csv.DictReader(file)
        portfolio = []
        for row in rows:
            portfolio.append(
                {
                    "name": row["name"],
                    "shares": int(row["shares"]),
                    "price": float(row["price"]),
                }
            )
        return portfolio


@st.cache_data
def read_prices(filename):
    prices = {}
    with open(filename, newline="") as file:
        rows = csv.reader(file)
        for row in rows:
            if not row:
                continue
            name, price = row
            prices[name] = float(price)
    return prices


def make_report(portfolio, prices):
    report = []
    for holding in portfolio:
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


st.set_page_config(page_title="Portfolio Dashboard", layout="wide")

st.title("Portfolio Dashboard")
st.caption("A Streamlit version of the Practical Python portfolio exercises.")

portfolio = read_portfolio(DATA_DIR / "portfolio.csv")
prices = read_prices(DATA_DIR / "prices.csv")
report = make_report(portfolio, prices)

names = {row["name"] for row in report}

with st.sidebar:
    st.header("Filters")
    selected = st.multiselect("Stocks", sorted(names), default=sorted(names))
    min_value = st.slider("Minimum value", 0, 20000, 0, step=500)

filtered = [
    row for row in report if row["name"] in selected and row["value"] >= min_value
]

total_cost = sum(row["cost"] for row in filtered)
total_value = sum(row["value"] for row in filtered)
gain_loss = total_value - total_cost

metric_cols = st.columns(3)
metric_cols[0].metric("Total cost", f"${total_cost:,.2f}")
metric_cols[1].metric("Current value", f"${total_value:,.2f}")
metric_cols[2].metric("Gain/loss", f"${gain_loss:,.2f}")

st.subheader("Holdings")
if filtered:
    st.dataframe(
        filtered,
        column_config={
            "name": st.column_config.TextColumn("Stock"),
            "shares": st.column_config.NumberColumn("Shares"),
            "purchase_price": st.column_config.NumberColumn(
                "Purchase price", format="$%.2f"
            ),
            "current_price": st.column_config.NumberColumn(
                "Current price", format="$%.2f"
            ),
            "cost": st.column_config.NumberColumn("Cost", format="$%.2f"),
            "value": st.column_config.NumberColumn("Value", format="$%.2f"),
            "change": st.column_config.NumberColumn("Gain/loss", format="$%.2f"),
        },
        hide_index=True,
    )

    st.subheader("Value by Stock")
    st.bar_chart(filtered, x="name", y="value", x_label="Stock", y_label="Value")
else:
    st.info("No holdings match the current filters.")
