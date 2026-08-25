import streamlit as st


def add_note():
    text = st.session_state.get("new_note", "").strip()
    if text:
        st.session_state.class_notes.append(text)
        st.session_state.new_note = ""


with st.form("notes_form"):
    st.text_input("Class note", key="new_note", placeholder="Add an instructor note")
    st.form_submit_button("Add note", icon=":material/add:", on_click=add_note)

if st.session_state.class_notes:
    for number, note in enumerate(st.session_state.class_notes, start=1):
        st.markdown(f"**{number}.** {note}")
else:
    st.info("No notes yet.", icon=":material/edit_note:")

