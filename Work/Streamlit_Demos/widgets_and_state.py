import streamlit as st

from Work.Streamlit_Demos.demo_data import filter_report, load_report, summarize


FILTER_KEYS = ["stock_pills", "view_mode", "losers_only", "min_value"]


def reset_filters():
    for key in FILTER_KEYS:
        st.session_state.pop(key, None)


def add_note():
    note = st.session_state.get("note_text", "").strip()
    if note:
        st.session_state.notes.append(note)
        st.session_state.note_text = ""


st.set_page_config(
    page_title="Widgets and state",
    page_icon=":material/tune:",
    layout="wide",
)

st.session_state.setdefault("notes", [])

report = load_report()
names = sorted({row["name"] for row in report})

st.title("Widgets and state")
st.caption("Modern selection widgets, forms, and session state on portfolio data.")

with st.sidebar:
    st.header("Controls")
    selected = st.pills(
        "Stocks",
        names,
        default=names,
        selection_mode="multi",
        key="stock_pills",
    )
    view_mode = st.segmented_control(
        "View",
        ["Summary", "Rows", "Notes"],
        default="Summary",
        key="view_mode",
    )
    losers_only = st.toggle("Show losers only", key="losers_only")
    minimum_value = st.slider("Minimum value", 0, 25000, 0, step=500, key="min_value")
    st.button("Reset filters", icon=":material/refresh:", on_click=reset_filters)

filtered = filter_report(report, selected, minimum_value, losers_only)

if not filtered:
    st.warning("The current widget choices produce an empty result.", icon=":material/warning:")
    st.caption("Reset the filters or turn off 'Show losers only' to bring rows back.")
    st.stop()

if view_mode == "Summary":
    total_cost, total_value, gain_loss = summarize(filtered)
    with st.container(horizontal=True):
        st.metric("Rows", len(filtered), border=True)
        st.metric("Current value", f"${total_value:,.2f}", border=True)
        st.metric("Gain/loss", f"${gain_loss:,.2f}", border=True)

    st.bar_chart(filtered, x="name", y="change", x_label="Stock", y_label="Gain/loss")

elif view_mode == "Rows":
    st.dataframe(
        filtered,
        column_config={
            "name": st.column_config.TextColumn("Stock"),
            "purchase_price": st.column_config.NumberColumn("Purchase price", format="$%.2f"),
            "current_price": st.column_config.NumberColumn("Current price", format="$%.2f"),
            "cost": st.column_config.NumberColumn("Cost", format="$%.2f"),
            "value": st.column_config.NumberColumn("Value", format="$%.2f"),
            "change": st.column_config.NumberColumn("Gain/loss", format="$%.2f"),
            "return_pct": st.column_config.NumberColumn("Return", format="percent"),
        },
        hide_index=True,
    )

else:
    with st.form("note_form", border=True):
        st.text_input(
            "Instructor note",
            key="note_text",
            placeholder="Try: What changed after filtering to losers only?",
        )
        st.form_submit_button("Add note", icon=":material/add:", on_click=add_note)

    if st.session_state.notes:
        for number, note in enumerate(st.session_state.notes, start=1):
            st.markdown(f"**{number}.** {note}")
    else:
        st.info("No notes yet.", icon=":material/edit_note:")
