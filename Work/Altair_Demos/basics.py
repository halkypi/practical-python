import altair as alt
import streamlit as st

from demo_data import holdings_by_name, load_portfolio_report


st.set_page_config(
    page_title="Altair basics",
    page_icon=":material/bar_chart:",
    layout="wide",
)

st.title("Altair basics")
st.caption("Marks, encodings, sorting, color, size, tooltips, and filters.")

report = holdings_by_name(load_portfolio_report())

with st.sidebar:
    st.header("Filters")
    names = sorted(report["name"].unique())
    selected = st.multiselect("Stocks", names, default=names)
    minimum_value = st.slider("Minimum value", 0, 25000, 0, step=500)

filtered = report[(report["name"].isin(selected)) & (report["value"] >= minimum_value)]

if filtered.empty:
    st.info("No holdings match the current filters.", icon=":material/filter_alt_off:")
    st.stop()

bar = (
    alt.Chart(filtered)
    .mark_bar()
    .encode(
        x=alt.X("value:Q", title="Current value", axis=alt.Axis(format="$,.0f")),
        y=alt.Y("name:N", title="Stock", sort="-x"),
        color=alt.Color("result:N", title="Result", scale=alt.Scale(range=["#d95f02", "#1b9e77"])),
        tooltip=[
            alt.Tooltip("name:N", title="Stock"),
            alt.Tooltip("shares:Q", title="Shares", format=","),
            alt.Tooltip("value:Q", title="Value", format="$,.2f"),
            alt.Tooltip("change:Q", title="Gain/loss", format="$,.2f"),
        ],
    )
    .properties(height=280)
)

scatter = (
    alt.Chart(filtered)
    .mark_circle(opacity=0.75)
    .encode(
        x=alt.X("cost:Q", title="Original cost", axis=alt.Axis(format="$,.0f")),
        y=alt.Y("value:Q", title="Current value", axis=alt.Axis(format="$,.0f")),
        size=alt.Size("shares:Q", title="Shares"),
        color=alt.Color("name:N", title="Stock"),
        tooltip=[
            alt.Tooltip("name:N", title="Stock"),
            alt.Tooltip("cost:Q", title="Cost", format="$,.2f"),
            alt.Tooltip("value:Q", title="Value", format="$,.2f"),
            alt.Tooltip("return_pct:Q", title="Return", format=".1%"),
        ],
    )
    .properties(height=280)
)

st.subheader("Sorted bar chart")
st.altair_chart(bar)

st.subheader("Scatter plot with tooltips")
st.altair_chart(scatter)

with st.expander("Rows used by the charts"):
    st.dataframe(
        filtered,
        column_config={
            "name": st.column_config.TextColumn("Stock"),
            "cost": st.column_config.NumberColumn("Cost", format="$%.2f"),
            "value": st.column_config.NumberColumn("Value", format="$%.2f"),
            "change": st.column_config.NumberColumn("Gain/loss", format="$%.2f"),
            "return_pct": st.column_config.NumberColumn("Return", format="percent"),
        },
        hide_index=True,
    )
