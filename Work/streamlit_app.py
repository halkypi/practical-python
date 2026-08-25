# streamlit_app.py
#
# Exercise 10.1

from pathlib import Path

import streamlit as st


DATA_DIR = Path(__file__).parent / "Data"


st.set_page_config(page_title="Portfolio Dashboard", layout="wide")

st.title("Portfolio Dashboard")
st.caption("Build this app through the Section 10 exercises.")

st.write("Start by running this file with:")
st.code("streamlit run Work/streamlit_app.py")

st.write("Then replace this starter content as you complete the exercises.")
