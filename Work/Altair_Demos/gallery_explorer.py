import altair as alt
import pandas as pd
import streamlit as st

from demo_data import holdings_by_name, load_portfolio_report, price_history, sector_holdings


st.set_page_config(
    page_title="Altair gallery explorer",
    page_icon=":material/explore:",
    layout="wide",
)


def simple_bar():
    data = holdings_by_name(load_portfolio_report())
    return (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x=alt.X("value:Q", title="Value", axis=alt.Axis(format="$,.0f")),
            y=alt.Y("name:N", title="Stock", sort="-x"),
            tooltip=["name:N", alt.Tooltip("value:Q", format="$,.2f")],
        )
        .properties(height=300)
    )


def scatter_tooltips():
    data = holdings_by_name(load_portfolio_report())
    return (
        alt.Chart(data)
        .mark_circle(size=120, opacity=0.75)
        .encode(
            x=alt.X("cost:Q", title="Cost", axis=alt.Axis(format="$,.0f")),
            y=alt.Y("value:Q", title="Value", axis=alt.Axis(format="$,.0f")),
            color=alt.Color("name:N", title="Stock"),
            tooltip=["name:N", alt.Tooltip("return_pct:Q", title="Return", format=".1%")],
        )
        .properties(height=300)
    )


def interactive_brush():
    data = price_history()
    brush = alt.selection_interval(encodings=["x"])
    overview = (
        alt.Chart(data)
        .mark_area(opacity=0.35)
        .encode(x="date:T", y="mean(price):Q")
        .add_params(brush)
        .properties(height=90)
    )
    detail = (
        alt.Chart(data)
        .mark_circle(size=80)
        .encode(
            x="date:T",
            y=alt.Y("price:Q", axis=alt.Axis(format="$,.0f")),
            color="name:N",
            tooltip=["name:N", "date:T", alt.Tooltip("price:Q", format="$,.2f")],
        )
        .transform_filter(brush)
        .properties(height=260)
    )
    return overview & detail


def histogram():
    data = load_portfolio_report()
    return (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x=alt.X("return_pct:Q", bin=True, title="Return"),
            y=alt.Y("count():Q", title="Rows"),
            tooltip=[alt.Tooltip("count():Q", title="Rows")],
        )
        .properties(height=300)
    )


def layered_rule():
    data = holdings_by_name(load_portfolio_report())
    bars = alt.Chart(data).mark_bar().encode(
        x=alt.X("change:Q", title="Gain/loss", axis=alt.Axis(format="$,.0f")),
        y=alt.Y("name:N", title="Stock", sort="-x"),
        color=alt.condition("datum.change >= 0", alt.value("#1b9e77"), alt.value("#d95f02")),
    )
    rule = alt.Chart(data).mark_rule(color="#555").encode(x=alt.datum(0))
    return (bars + rule).properties(height=300)


def faceted_bars():
    data = sector_holdings()
    return (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x=alt.X("value:Q", title="Value", axis=alt.Axis(format="$,.0f")),
            y=alt.Y("name:N", title=None, sort="-x"),
            color=alt.Color("sector:N", legend=None),
            tooltip=["sector:N", "name:N", alt.Tooltip("value:Q", format="$,.2f")],
        )
        .properties(width=220, height=170)
        .facet(column=alt.Column("sector:N", title="Sector"))
    )


def line_chart():
    data = price_history()
    return (
        alt.Chart(data)
        .mark_line(point=True)
        .encode(
            x=alt.X("date:T", title="Date"),
            y=alt.Y("price:Q", title="Price", axis=alt.Axis(format="$,.0f")),
            color=alt.Color("name:N", title="Stock"),
            tooltip=["name:N", "date:T", alt.Tooltip("price:Q", format="$,.2f")],
        )
        .properties(height=300)
    )


def heatmap():
    data = pd.DataFrame(
        [
            {"stock": "AA", "measure": "Cost", "amount": 3220},
            {"stock": "AA", "measure": "Value", "amount": 922},
            {"stock": "CAT", "measure": "Cost", "amount": 12516},
            {"stock": "CAT", "measure": "Value", "amount": 5319},
            {"stock": "IBM", "measure": "Cost", "amount": 11599},
            {"stock": "IBM", "measure": "Value", "amount": 15942},
            {"stock": "MSFT", "measure": "Cost", "amount": 13491},
            {"stock": "MSFT", "measure": "Value", "amount": 5222},
        ]
    )
    return (
        alt.Chart(data)
        .mark_rect()
        .encode(
            x=alt.X("measure:N", title="Measure"),
            y=alt.Y("stock:N", title="Stock"),
            color=alt.Color("amount:Q", title="Amount", scale=alt.Scale(scheme="tealblues")),
            tooltip=["stock:N", "measure:N", alt.Tooltip("amount:Q", format="$,.0f")],
        )
        .properties(height=300)
    )


EXAMPLES = {
    "Simple charts": {
        "Sorted bar chart": ("Sort by value so the largest holding is easiest to see.", simple_bar),
        "Line chart": ("Draw price history with one color per stock.", line_chart),
        "Scatter with tooltips": ("Use tooltips for details that would clutter the chart.", scatter_tooltips),
    },
    "Interactive charts": {
        "Brush and linked chart": ("Brush the top chart to filter the detailed points.", interactive_brush),
    },
    "Distributions": {
        "Histogram": ("Bin returns to see how rows are distributed.", histogram),
    },
    "Composition": {
        "Layered rule": ("Layer a zero rule over gain and loss bars.", layered_rule),
        "Faceted bars": ("Split the same bar chart by sector.", faceted_bars),
    },
    "Tables": {
        "Heatmap": ("A table-like chart where color carries the amount.", heatmap),
    },
}

st.title("Altair gallery explorer")
st.caption("A small classroom set adapted from common Altair gallery patterns.")

with st.sidebar:
    st.header("Example")
    category = st.selectbox("Category", list(EXAMPLES))
    example_name = st.selectbox("Chart", list(EXAMPLES[category]))

caption, chart_fn = EXAMPLES[category][example_name]
st.subheader(example_name)
st.caption(caption)
st.altair_chart(chart_fn())
