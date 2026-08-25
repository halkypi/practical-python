import altair as alt
import streamlit as st

from demo_data import holdings_by_name, load_portfolio_report, price_history


st.set_page_config(
    page_title="Altair interaction",
    page_icon=":material/touch_app:",
    layout="wide",
)

st.title("Altair interaction")
st.caption("Selections, brushes, hover highlights, linked charts, and legends.")

holdings = holdings_by_name(load_portfolio_report())
history = price_history()

with st.sidebar:
    st.header("Chart controls")
    metric = st.segmented_control("Bar value", ["value", "change", "return_pct"], default="value")
    names = st.multiselect("Stocks", sorted(holdings["name"].unique()), default=sorted(holdings["name"].unique()))

holdings = holdings[holdings["name"].isin(names)]
history = history[history["name"].isin(names)]

if holdings.empty:
    st.info("Choose at least one stock.", icon=":material/filter_alt_off:")
    st.stop()

hover = alt.selection_point(fields=["name"], on="pointerover", empty=False)
brush = alt.selection_interval(encodings=["x"])
legend = alt.selection_point(fields=["name"], bind="legend")

bars = (
    alt.Chart(holdings)
    .mark_bar()
    .encode(
        x=alt.X(f"{metric}:Q", title=metric.replace("_", " ").title()),
        y=alt.Y("name:N", title="Stock", sort="-x"),
        color=alt.condition(hover, alt.Color("name:N", legend=None), alt.value("#b8b8b8")),
        opacity=alt.condition(hover, alt.value(1), alt.value(0.65)),
        tooltip=[
            alt.Tooltip("name:N", title="Stock"),
            alt.Tooltip("value:Q", title="Value", format="$,.2f"),
            alt.Tooltip("change:Q", title="Gain/loss", format="$,.2f"),
            alt.Tooltip("return_pct:Q", title="Return", format=".1%"),
        ],
    )
    .add_params(hover)
    .properties(height=260)
)

line = (
    alt.Chart(history)
    .mark_line(point=True)
    .encode(
        x=alt.X("date:T", title="Date"),
        y=alt.Y("price:Q", title="Price", axis=alt.Axis(format="$,.0f")),
        color=alt.Color("name:N", title="Stock"),
        opacity=alt.condition(legend, alt.value(1), alt.value(0.2)),
        tooltip=[
            alt.Tooltip("date:T", title="Date"),
            alt.Tooltip("name:N", title="Stock"),
            alt.Tooltip("price:Q", title="Price", format="$,.2f"),
        ],
    )
    .add_params(legend)
    .properties(height=260)
)

timeline = (
    alt.Chart(history)
    .mark_area(opacity=0.35)
    .encode(
        x=alt.X("date:T", title="Brush a date range"),
        y=alt.Y("mean(price):Q", title="Average price"),
    )
    .add_params(brush)
    .properties(height=90)
)

linked_points = (
    alt.Chart(history)
    .mark_circle(size=90)
    .encode(
        x=alt.X("date:T", title="Date"),
        y=alt.Y("price:Q", title="Price", axis=alt.Axis(format="$,.0f")),
        color=alt.Color("name:N", title="Stock"),
        tooltip=["name:N", alt.Tooltip("price:Q", format="$,.2f"), "date:T"],
    )
    .transform_filter(brush)
    .properties(height=260)
)

st.subheader("Hover on a stock")
st.altair_chart(bars)

st.subheader("Interactive legend")
st.altair_chart(line)

st.subheader("Brush and linked view")
st.altair_chart(timeline & linked_points)
