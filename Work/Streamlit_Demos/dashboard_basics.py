import streamlit as st

from Work.Streamlit_Demos.demo_data import (
    filter_report,
    holdings_by_name,
    load_report,
    summarize,
)


st.set_page_config(
    page_title="Dashboard basics",
    page_icon=":material/dashboard:",
    layout="wide",
)

st.title("Dashboard basics")
st.caption("A compact portfolio dashboard using familiar Python data structures.")

report = load_report()
names = sorted({row["name"] for row in report})

with st.sidebar:
    st.header("Filters")
    selected = st.multiselect("Stocks", names, default=names)
    minimum_value = st.slider("Minimum holding value", 0, 25000, 0, step=500)
    st.caption("Filters live here so the main page can stay focused on results.")

filtered = filter_report(report, selected, minimum_value)
total_cost, total_value, gain_loss = summarize(filtered)

with st.container(horizontal=True):
    st.metric("Total cost", f"${total_cost:,.2f}", border=True)
    st.metric("Current value", f"${total_value:,.2f}", border=True)
    st.metric("Gain/loss", f"${gain_loss:,.2f}", border=True)

if not filtered:
    st.info("No holdings match the current filters.", icon=":material/filter_alt_off:")
    st.stop()

table_data = sorted(filtered, key=lambda row: row["value"], reverse=True)

st.subheader("Holdings")
st.dataframe(
    table_data,
    column_config={
        "name": st.column_config.TextColumn("Stock", pinned=True),
        "shares": st.column_config.NumberColumn("Shares", format="%d"),
        "purchase_price": st.column_config.NumberColumn("Purchase price", format="$%.2f"),
        "current_price": st.column_config.NumberColumn("Current price", format="$%.2f"),
        "cost": st.column_config.NumberColumn("Cost", format="$%.2f"),
        "value": st.column_config.NumberColumn("Value", format="$%.2f"),
        "change": st.column_config.NumberColumn("Gain/loss", format="$%.2f"),
        "return_pct": st.column_config.NumberColumn("Return", format="percent"),
    },
    hide_index=True,
)

st.subheader("Value by stock")
st.bar_chart(
    holdings_by_name(filtered),
    x="name",
    y="value",
    x_label="Stock",
    y_label="Value",
)
