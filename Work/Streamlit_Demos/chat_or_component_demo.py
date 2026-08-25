import streamlit as st

from Work.Streamlit_Demos.demo_data import load_report, summarize


SUGGESTIONS = {
    ":blue[:material/account_balance_wallet:] Summarize portfolio": "summarize portfolio",
    ":orange[:material/trending_down:] Show biggest loss": "show biggest loss",
    ":green[:material/help:] Explain gain/loss": "explain gain loss",
}


def answer(prompt, report):
    prompt = prompt.lower()
    total_cost, total_value, gain_loss = summarize(report)

    if "loss" in prompt:
        worst = min(report, key=lambda row: row["change"])
        return (
            f"The largest loss is {worst['name']}: ${worst['change']:,.2f}. "
            "That comes from comparing current value with original cost."
        )

    if "gain" in prompt or "explain" in prompt:
        return (
            "Gain/loss uses ordinary Python arithmetic: "
            "`shares * current_price - shares * purchase_price`."
        )

    return (
        f"The selected CSV portfolio cost ${total_cost:,.2f} and is now worth "
        f"${total_value:,.2f}, for a gain/loss of ${gain_loss:,.2f}."
    )


st.set_page_config(
    page_title="Chat UI demo",
    page_icon=":material/chat:",
    layout="centered",
)

st.title("Chat UI demo")
st.caption("A canned portfolio helper using Streamlit chat elements, not an AI service.")

st.session_state.setdefault(
    "messages",
    [{"role": "assistant", "content": "Ask me a portfolio question from this tiny canned set."}],
)

report = load_report()

if len(st.session_state.messages) == 1:
    selected = st.pills("Try asking", list(SUGGESTIONS), label_visibility="collapsed")
    if selected:
        st.session_state.messages.append({"role": "user", "content": SUGGESTIONS[selected]})
        st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Ask about the portfolio"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    response = answer(prompt, report)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.write(response)
