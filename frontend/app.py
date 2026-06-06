import streamlit as st
import requests

BACKEND_URL = (
    "https://kartikeyas-ai-persona.onrender.com/chat"
)

st.set_page_config(
    page_title="Kartikeya AI Persona",
    page_icon="🤖",
    layout="wide"
)

st.title(
    "🤖 Kartikeya AI Persona"
)

st.write(
    """
Ask about:

• Skills
• Experience
• Projects
• GitHub repositories
• Technical decisions
• Architecture
• Career background
"""
)

if (
    "messages"
    not in st.session_state
):
    st.session_state.messages = []

for message in (
    st.session_state.messages
):

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

prompt = st.chat_input(
    "Ask something..."
)

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message(
        "user"
    ):
        st.markdown(prompt)

    try:

        response = requests.post(
            BACKEND_URL,
            json={
                "message": prompt,
                "history":
                    st.session_state.messages
            },
            timeout=120
        )

        answer = (
            response.json()
            .get(
                "response",
                "No response returned."
            )
        )

    except Exception as e:

        answer = (
            f"Error: {str(e)}"
        )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    with st.chat_message(
        "assistant"
    ):
        st.markdown(answer)