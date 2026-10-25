import streamlit as st

from src.chatbot import FAQChatbot

st.set_page_config(page_title="CodeAlpha FAQ Assistant", page_icon="💬")

USER_AVATAR = "👤"
BOT_AVATAR = "🤖"

# ---------- CSS: marker diye user message ke right e pathano ----------
st.markdown(
    """
    <style>
    /* jei chat message er bhetore .user-msg marker ache, shetai user er message */
    div[data-testid="stChatMessage"]:has(.user-msg) {
        flex-direction: row-reverse;   /* emoji right e jabe */
        width: fit-content;            /* bubble text er size onujayi hobe */
        max-width: 80%;
        margin-left: auto;             /* pura bubble right side e jabe */
    }

    /* text sob somoy left align */
    div[data-testid="stChatMessage"] p,
    div[data-testid="stChatMessage"] li,
    div[data-testid="stChatMessageContent"] {
        text-align: left !important;
    }

    /* marker ta jate kono jayga na ne */
    .user-msg {
        display: none;
    }
    div[data-testid="stElementContainer"]:has(.user-msg) {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("CodeAlpha FAQ Assistant")
st.caption("Ask a question about the CodeAlpha internship.")


def render_message(role: str, content: str) -> None:
    """Ekta message screen e dekhay. User hole marker boshay."""
    avatar = USER_AVATAR if role == "user" else BOT_AVATAR
    with st.chat_message(role, avatar=avatar):
        if role == "user":
            st.markdown('<span class="user-msg"></span>', unsafe_allow_html=True)
        st.markdown(content)


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
    render_message(msg["role"], msg["content"])

if prompt := st.chat_input("Type your question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    render_message("user", prompt)

    result = bot.reply(prompt)
    text = result["answer"]
    if result["suggestions"]:
        text += "\n\n" + "\n".join(f"- {s}" for s in result["suggestions"])

    st.session_state.messages.append({"role": "assistant", "content": text})
    render_message("assistant", text)
