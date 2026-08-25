import streamlit as st

from Work.Streamlit_Demos.multipage_demo.portfolio_tools import (
    selected_report,
    summarize,
)


report = selected_report()

if not report:
    st.info("Choose at least one stock in the sidebar.", icon=":material/filter_alt_off:")
    st.stop()

total_cost, total_value, gain_loss = summarize(report)

with st.container(horizontal=True):
    st.metric("Total cost", f"${total_cost:,.2f}", border=True)
    st.metric("Current value", f"${total_value:,.2f}", border=True)
    st.metric("Gain/loss", f"${gain_loss:,.2f}", border=True)

st.bar_chart(report, x="name", y="value", x_label="Stock", y_label="Value")
