import altair as alt
import streamlit as st

from demo_data import load_portfolio_report, price_history, sector_holdings


st.set_page_config(
    page_title="Altair transforms",
    page_icon=":material/functions:",
    layout="wide",
)

st.title("Altair transforms")
st.caption("Aggregate, bin, calculate, fold, window, rank, and top-k examples.")

rows = load_portfolio_report()
sectors = sector_holdings()
history = price_history()

with st.sidebar:
    st.header("Transform controls")
    top_k = st.slider("Top holdings", 1, 5, 3)
    bin_step = st.slider("Return bin size", 0.05, 0.30, 0.10, step=0.05)

aggregate = (
    alt.Chart(sectors)
    .mark_bar()
    .encode(
        x=alt.X("sum(value):Q", title="Value", axis=alt.Axis(format="$,.0f")),
        y=alt.Y("sector:N", title="Sector", sort="-x"),
        color=alt.Color("sector:N", legend=None),
        tooltip=[
            alt.Tooltip("sector:N", title="Sector"),
            alt.Tooltip("sum(value):Q", title="Value", format="$,.2f"),
        ],
    )
    .properties(height=240)
)

bins = (
    alt.Chart(rows)
    .mark_bar()
    .encode(
        x=alt.X("return_pct:Q", bin=alt.Bin(step=bin_step), title="Return"),
        y=alt.Y("count():Q", title="Rows"),
        tooltip=[alt.Tooltip("count():Q", title="Rows")],
    )
    .properties(height=240)
)

calculated = (
    alt.Chart(rows)
    .transform_calculate(
        dollars_per_share="datum.current_price - datum.purchase_price",
    )
    .mark_bar()
    .encode(
        x=alt.X("dollars_per_share:Q", title="Change per share", axis=alt.Axis(format="$,.0f")),
        y=alt.Y("name:N", title="Stock", sort="-x"),
        color=alt.condition("datum.dollars_per_share >= 0", alt.value("#1b9e77"), alt.value("#d95f02")),
        tooltip=[
            "name:N",
            alt.Tooltip("dollars_per_share:Q", title="Change/share", format="$,.2f"),
        ],
    )
    .properties(height=240)
)

folded = (
    alt.Chart(rows)
    .transform_fold(["cost", "value"], as_=["amount_kind", "amount"])
    .mark_bar()
    .encode(
        x=alt.X("name:N", title="Stock"),
        y=alt.Y("amount:Q", title="Amount", axis=alt.Axis(format="$,.0f")),
        color=alt.Color("amount_kind:N", title="Amount"),
        xOffset="amount_kind:N",
        tooltip=["name:N", "amount_kind:N", alt.Tooltip("amount:Q", format="$,.2f")],
    )
    .properties(height=240)
)

ranked = (
    alt.Chart(sectors)
    .transform_window(
        rank="rank()",
        sort=[alt.SortField("value", order="descending")],
    )
    .transform_filter(f"datum.rank <= {top_k}")
    .mark_bar()
    .encode(
        x=alt.X("value:Q", title="Value", axis=alt.Axis(format="$,.0f")),
        y=alt.Y("name:N", title="Stock", sort="-x"),
        color=alt.Color("sector:N", title="Sector"),
        tooltip=["name:N", "sector:N", alt.Tooltip("value:Q", format="$,.2f"), "rank:O"],
    )
    .properties(height=240)
)

rolling = (
    alt.Chart(history)
    .transform_window(
        rolling_mean="mean(price)",
        frame=[-2, 0],
        groupby=["name"],
    )
    .mark_line(point=True)
    .encode(
        x=alt.X("date:T", title="Date"),
        y=alt.Y("rolling_mean:Q", title="Three-point average", axis=alt.Axis(format="$,.0f")),
        color=alt.Color("name:N", title="Stock"),
        tooltip=["name:N", "date:T", alt.Tooltip("rolling_mean:Q", format="$,.2f")],
    )
    .properties(height=240)
)

left, right = st.columns(2)
with left:
    st.subheader("Aggregate")
    st.altair_chart(aggregate)
with right:
    st.subheader("Bin")
    st.altair_chart(bins)

left, right = st.columns(2)
with left:
    st.subheader("Calculate")
    st.altair_chart(calculated)
with right:
    st.subheader("Fold")
    st.altair_chart(folded)

left, right = st.columns(2)
with left:
    st.subheader("Window rank")
    st.altair_chart(ranked)
with right:
    st.subheader("Window average")
    st.altair_chart(rolling)
