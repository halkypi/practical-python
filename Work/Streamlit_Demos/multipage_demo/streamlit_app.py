import streamlit as st

from Work.Streamlit_Demos.multipage_demo.portfolio_tools import make_report


st.set_page_config(
    page_title="Multipage portfolio",
    page_icon=":material/account_tree:",
    layout="wide",
)

report = make_report()
names = sorted({row["name"] for row in report})
st.session_state.setdefault("selected_stocks", names)
st.session_state.setdefault("class_notes", [])

with st.sidebar:
    st.header("Shared filters")
    st.multiselect("Stocks", names, key="selected_stocks")
    st.caption("This sidebar runs before every page.")

page = st.navigation(
    [
        st.Page("app_pages/dashboard.py", title="Dashboard", icon=":material/dashboard:"),
        st.Page("app_pages/data.py", title="Data", icon=":material/table_chart:"),
        st.Page("app_pages/notes.py", title="Notes", icon=":material/edit_note:"),
    ],
    position="top",
)

st.title(f"{page.icon} {page.title}")
page.run()
