import streamlit as st
from main import chat_with_gpt

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
)

st.title("🤖 AI Chatbot")
st.caption("Streamlit + OpenAI (modern API)")

# Initialize chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Input box
user_input = st.chat_input("Type your message...")

if user_input:
    # Store user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = chat_with_gpt(st.session_state.messages)
            st.write(reply)

    # Store assistant reply
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })

# Sidebar controls
with st.sidebar:
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()