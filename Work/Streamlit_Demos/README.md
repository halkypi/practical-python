# Streamlit demo apps

Run these from the repository root.

| App | Run command | Purpose |
| --- | --- | --- |
| Dashboard basics | `streamlit run Work/Streamlit_Demos/dashboard_basics.py` | Shows page config, sidebar filters, metrics, `st.dataframe`, column config, and a bar chart. |
| Widgets and state | `streamlit run Work/Streamlit_Demos/widgets_and_state.py` | Shows `st.pills`, `st.segmented_control`, `st.toggle`, forms, `st.session_state`, reset behavior, and empty states. |
| Layout and design | `streamlit run Work/Streamlit_Demos/layout_and_design.py` | Shows sidebar discipline, columns, bordered containers, captions, Material icons, status messages, and Markdown. |
| Performance and caching | `streamlit run Work/Streamlit_Demos/performance_and_caching.py` | Shows reruns, `@st.cache_data`, cache clearing, and separation of loading from filtering/display. |
| Multipage demo | `streamlit run Work/Streamlit_Demos/multipage_demo/streamlit_app.py` | Shows modern multipage Streamlit with `st.navigation` and `st.Page` across Dashboard, Data, and Notes pages. |
| Chat UI demo | `streamlit run Work/Streamlit_Demos/chat_or_component_demo.py` | Shows a simple canned portfolio chat UI with `st.chat_message`, `st.chat_input`, and suggestion pills. |

These demos use `Work/Data/portfolio.csv` and `Work/Data/prices.csv`, and the CSV readers skip blank rows.

