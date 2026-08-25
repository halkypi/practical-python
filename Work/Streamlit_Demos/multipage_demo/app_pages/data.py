import streamlit as st

from Work.Streamlit_Demos.multipage_demo.portfolio_tools import selected_report


report = selected_report()

if not report:
    st.warning("No rows to display.", icon=":material/warning:")
    st.stop()

st.caption("The Data page reuses the shared sidebar selection from the entrypoint.")
st.dataframe(
    report,
    column_config={
        "name": st.column_config.TextColumn("Stock", pinned=True),
        "shares": st.column_config.NumberColumn("Shares", format="%d"),
        "purchase_price": st.column_config.NumberColumn("Purchase price", format="$%.2f"),
        "current_price": st.column_config.NumberColumn("Current price", format="$%.2f"),
        "cost": st.column_config.NumberColumn("Cost", format="$%.2f"),
        "value": st.column_config.NumberColumn("Value", format="$%.2f"),
        "change": st.column_config.NumberColumn("Gain/loss", format="$%.2f"),
    },
    hide_index=True,
)
