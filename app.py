import streamlit as st

from src.chatbot import FAQChatbot

st.set_page_config(page_title="CodeAlpha FAQ Assistant", page_icon="💬")
st.title("CodeAlpha FAQ Assistant")
st.caption("Ask a question about the CodeAlpha internship.")


@st.cache_resource
def load_bot() -> FAQChatbot:
    return FAQChatbot()



bot = load_bot()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! Ask me about tasks, submission, certificates and more.",
        }
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Type your question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    result = bot.reply(prompt)
    text = result["answer"]
    if result["suggestions"]:
        text += "\n\n" + "\n".join(f"- {s}" for s in result["suggestions"])

    st.session_state.messages.append({"role": "assistant", "content": text})
    with st.chat_message("assistant"):
        st.write(text)
