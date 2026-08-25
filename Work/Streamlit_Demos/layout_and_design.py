import streamlit as st

from Work.Streamlit_Demos.demo_data import filter_report, load_report, summarize


st.set_page_config(
    page_title="Layout and design",
    page_icon=":material/space_dashboard:",
    layout="wide",
)

report = load_report()
names = sorted({row["name"] for row in report})

with st.sidebar:
    st.header(":material/filter_list: Filters")
    selected = st.multiselect("Stocks", names, default=names)
    minimum_value = st.slider("Minimum value", 0, 25000, 0, step=500)
    st.caption("Global controls stay in the sidebar.")

st.title(":material/analytics: Layout and design")
st.caption("Restrained hierarchy: title, metrics, two focused panels, then detail.")

filtered = filter_report(report, selected, minimum_value)
if not filtered:
    st.info("No holdings match the current filters.", icon=":material/info:")
    st.stop()

total_cost, total_value, gain_loss = summarize(filtered)
status_color = "green" if gain_loss >= 0 else "red"
status_label = "Gain" if gain_loss >= 0 else "Loss"

st.markdown(f":{status_color}-badge[{status_label}] :small[Compared with original purchase cost]")

with st.container(horizontal=True):
    st.metric(":material/payments: Total cost", f"${total_cost:,.2f}", border=True)
    st.metric(":material/account_balance_wallet: Current value", f"${total_value:,.2f}", border=True)
    st.metric(":material/trending_up: Gain/loss", f"${gain_loss:,.2f}", border=True)

left, right = st.columns(2, gap="large")

with left:
    with st.container(border=True, height="stretch"):
        st.subheader(":material/bar_chart: Value")
        st.caption("The same report rows can feed a chart directly.")
        st.bar_chart(filtered, x="name", y="value", x_label="Stock", y_label="Value")

with right:
    with st.container(border=True, height="stretch"):
        st.subheader(":material/query_stats: Return")
        st.caption("A second view answers a different classroom question.")
        st.bar_chart(filtered, x="name", y="return_pct", x_label="Stock", y_label="Return")

with st.container(border=True):
    st.subheader(":material/table_chart: Detail")
    st.markdown("Gain/loss is computed as `shares * current_price - shares * purchase_price`.")
    st.dataframe(
        filtered,
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
