import altair as alt
import streamlit as st

from demo_data import holdings_by_name, load_portfolio_report, price_history, sector_holdings


st.set_page_config(
    page_title="Altair composition",
    page_icon=":material/view_quilt:",
    layout="wide",
)

st.title("Altair composition")
st.caption("Layers, concatenation, repeated views, and facets.")

holdings = holdings_by_name(load_portfolio_report())
sectors = sector_holdings()
history = price_history()

value_bars = (
    alt.Chart(holdings)
    .mark_bar(color="#4c78a8")
    .encode(
        x=alt.X("value:Q", title="Value", axis=alt.Axis(format="$,.0f")),
        y=alt.Y("name:N", title="Stock", sort="-x"),
        tooltip=["name:N", alt.Tooltip("value:Q", format="$,.2f")],
    )
)

labels = (
    alt.Chart(holdings)
    .mark_text(align="left", dx=4)
    .encode(
        x="value:Q",
        y=alt.Y("name:N", sort="-x"),
        text=alt.Text("value:Q", format="$,.0f"),
    )
)

layered = (value_bars + labels).properties(height=260)

costs = (
    alt.Chart(holdings)
    .mark_bar(color="#72b7b2")
    .encode(
        x=alt.X("cost:Q", title="Cost", axis=alt.Axis(format="$,.0f")),
        y=alt.Y("name:N", title="Stock", sort="-x"),
        tooltip=["name:N", alt.Tooltip("cost:Q", format="$,.2f")],
    )
    .properties(height=230)
)

changes = (
    alt.Chart(holdings)
    .mark_bar()
    .encode(
        x=alt.X("change:Q", title="Gain/loss", axis=alt.Axis(format="$,.0f")),
        y=alt.Y("name:N", title="Stock", sort="-x"),
        color=alt.condition("datum.change >= 0", alt.value("#1b9e77"), alt.value("#d95f02")),
        tooltip=["name:N", alt.Tooltip("change:Q", format="$,.2f")],
    )
    .properties(height=230)
)

repeated = (
    alt.Chart(holdings)
    .mark_circle(size=110, opacity=0.75)
    .encode(
        x=alt.X(alt.repeat("column"), type="quantitative"),
        y=alt.Y(alt.repeat("row"), type="quantitative"),
        color=alt.Color("name:N", legend=None),
        tooltip=["name:N", alt.Tooltip("cost:Q", format="$,.2f"), alt.Tooltip("value:Q", format="$,.2f")],
    )
    .properties(width=180, height=180)
    .repeat(row=["value"], column=["cost", "shares", "return_pct"])
)

facet = (
    alt.Chart(sectors)
    .mark_bar()
    .encode(
        x=alt.X("value:Q", title="Value", axis=alt.Axis(format="$,.0f")),
        y=alt.Y("name:N", title=None, sort="-x"),
        color=alt.Color("sector:N", legend=None),
        tooltip=["sector:N", "name:N", alt.Tooltip("value:Q", format="$,.2f")],
    )
    .properties(width=220, height=150)
    .facet(column=alt.Column("sector:N", title="Sector"))
)

line = (
    alt.Chart(history)
    .mark_line()
    .encode(
        x=alt.X("date:T", title="Date"),
        y=alt.Y("price:Q", title="Price", axis=alt.Axis(format="$,.0f")),
        color=alt.Color("name:N", title="Stock"),
        tooltip=["name:N", "date:T", alt.Tooltip("price:Q", format="$,.2f")],
    )
    .properties(height=240)
)

st.subheader("Layered chart")
st.altair_chart(layered)

st.subheader("Horizontal composition")
st.altair_chart(costs | changes)

st.subheader("Vertical composition")
st.altair_chart(costs & changes)

st.subheader("Repeated chart")
st.altair_chart(repeated)

st.subheader("Faceted chart")
st.altair_chart(facet)

st.subheader("Line chart as a separate view")
st.altair_chart(line)
