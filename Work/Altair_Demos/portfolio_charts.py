import altair as alt
import streamlit as st

from demo_data import holdings_by_name, load_portfolio_report


st.set_page_config(
    page_title="Portfolio charts",
    page_icon=":material/account_balance:",
    layout="wide",
)

st.title("Portfolio charts")
st.caption("Altair charts built from the course portfolio and prices files.")

rows = load_portfolio_report()
holdings = holdings_by_name(rows)

with st.sidebar:
    st.header("Filters")
    result = st.segmented_control("Result", ["All", "Gain", "Loss"], default="All")
    sort_by = st.selectbox("Sort by", ["value", "change", "return_pct", "shares"])

if result != "All":
    holdings = holdings[holdings["result"] == result]

holdings = holdings.sort_values(sort_by, ascending=False)

if holdings.empty:
    st.warning("No holdings match the current filters.", icon=":material/warning:")
    st.stop()

with st.container(horizontal=True):
    st.metric("Cost", f"${holdings['cost'].sum():,.2f}", border=True)
    st.metric("Value", f"${holdings['value'].sum():,.2f}", border=True)
    st.metric("Gain/loss", f"${holdings['change'].sum():,.2f}", border=True)

base = alt.Chart(holdings).encode(
    y=alt.Y("name:N", title="Stock", sort="-x"),
    tooltip=[
        alt.Tooltip("name:N", title="Stock"),
        alt.Tooltip("cost:Q", title="Cost", format="$,.2f"),
        alt.Tooltip("value:Q", title="Value", format="$,.2f"),
        alt.Tooltip("change:Q", title="Gain/loss", format="$,.2f"),
    ],
)

value_bar = base.mark_bar().encode(
    x=alt.X("value:Q", title="Current value", axis=alt.Axis(format="$,.0f")),
    color=alt.Color("result:N", title="Result", scale=alt.Scale(range=["#d95f02", "#1b9e77"])),
)

zero = alt.Chart(holdings).mark_rule(color="#555").encode(x=alt.datum(0))
change_bar = (
    alt.Chart(holdings)
    .mark_bar()
    .encode(
        x=alt.X("change:Q", title="Gain/loss", axis=alt.Axis(format="$,.0f")),
        y=alt.Y("name:N", title="Stock", sort="-x"),
        color=alt.condition("datum.change >= 0", alt.value("#1b9e77"), alt.value("#d95f02")),
        tooltip=[
            alt.Tooltip("name:N", title="Stock"),
            alt.Tooltip("change:Q", title="Gain/loss", format="$,.2f"),
            alt.Tooltip("return_pct:Q", title="Return", format=".1%"),
        ],
    )
)

share_arc = (
    alt.Chart(holdings)
    .mark_arc(innerRadius=45)
    .encode(
        theta=alt.Theta("value:Q", title="Value"),
        color=alt.Color("name:N", title="Stock"),
        tooltip=[
            alt.Tooltip("name:N", title="Stock"),
            alt.Tooltip("value:Q", title="Value", format="$,.2f"),
        ],
    )
    .properties(height=260)
)

price_compare = (
    alt.Chart(rows)
    .transform_fold(["purchase_price", "current_price"], as_=["price_kind", "price"])
    .mark_bar()
    .encode(
        x=alt.X("name:N", title="Stock"),
        y=alt.Y("price:Q", title="Price", axis=alt.Axis(format="$,.0f")),
        color=alt.Color("price_kind:N", title="Price"),
        xOffset="price_kind:N",
        tooltip=[
            alt.Tooltip("name:N", title="Stock"),
            alt.Tooltip("price_kind:N", title="Price"),
            alt.Tooltip("price:Q", title="Amount", format="$,.2f"),
        ],
    )
    .properties(height=260)
)

left, right = st.columns(2)
with left:
    st.subheader("Current value")
    st.altair_chart(value_bar.properties(height=300))

with right:
    st.subheader("Gain and loss")
    st.altair_chart((change_bar + zero).properties(height=300))

left, right = st.columns(2)
with left:
    st.subheader("Portfolio share")
    st.altair_chart(share_arc)

with right:
    st.subheader("Purchase vs current price")
    st.altair_chart(price_compare)
