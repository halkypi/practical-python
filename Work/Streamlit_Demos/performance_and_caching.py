from pathlib import Path
import csv
import time

import streamlit as st


DATA_DIR = Path(__file__).resolve().parents[1] / "Data"


@st.cache_data
def read_portfolio(filename):
    time.sleep(0.2)
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
def read_prices(filename):
    time.sleep(0.2)
    prices = {}
    with open(filename, newline="") as file:
        rows = csv.reader(file)
        for row in rows:
            if not row or not any(item.strip() for item in row):
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
                "value": value,
                "change": value - cost,
            }
        )
    return report


def filter_report(report, selected_names):
    return [row for row in report if row["name"] in selected_names]


st.set_page_config(
    page_title="Performance and caching",
    page_icon=":material/speed:",
    layout="wide",
)

st.title("Performance and caching")
st.caption("The app reruns top-to-bottom, but cached data loading does not repeat work.")

st.session_state.setdefault("reruns", 0)
st.session_state.reruns += 1

started = time.perf_counter()
portfolio = read_portfolio(DATA_DIR / "portfolio.csv")
prices = read_prices(DATA_DIR / "prices.csv")
load_seconds = time.perf_counter() - started
report = make_report(portfolio, prices)
names = sorted({row["name"] for row in report})

with st.sidebar:
    st.header("Rerun controls")
    selected = st.multiselect("Stocks", names, default=names)
    st.button("Rerun now", icon=":material/play_arrow:")
    if st.button("Clear cached data", icon=":material/delete:"):
        st.cache_data.clear()
        st.success("Cache cleared. The next rerun will reload the CSV files.")

filtered = filter_report(report, selected)

with st.container(horizontal=True):
    st.metric("Script reruns", st.session_state.reruns, border=True)
    st.metric("CSV load time", f"{load_seconds:.3f}s", border=True)
    st.metric("Rows after filter", len(filtered), border=True)

left, right = st.columns(2)
with left:
    with st.container(border=True):
        st.subheader("Cached loading")
        st.code(
            """@st.cache_data
def read_prices(filename):
    return load_csv(filename)""",
            language="python",
        )
        st.caption("Loading is separate from filtering, so filter widgets stay cheap.")

with right:
    with st.container(border=True):
        st.subheader("Filtered display")
        if filtered:
            st.bar_chart(filtered, x="name", y="value", x_label="Stock", y_label="Value")
        else:
            st.info("No rows selected.", icon=":material/filter_alt_off:")

st.dataframe(
    filtered,
    column_config={
        "name": st.column_config.TextColumn("Stock"),
        "purchase_price": st.column_config.NumberColumn("Purchase price", format="$%.2f"),
        "current_price": st.column_config.NumberColumn("Current price", format="$%.2f"),
        "value": st.column_config.NumberColumn("Value", format="$%.2f"),
        "change": st.column_config.NumberColumn("Gain/loss", format="$%.2f"),
    },
    hide_index=True,
)

