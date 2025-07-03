import streamlit as st
import google.generativeai as genai

# Page setup
st.set_page_config(page_title="Chat with AI BOT", layout="centered")

st.markdown("<h1 style='text-align: center;'>💬 Chat with AI</h1>", unsafe_allow_html=True)
st.markdown("---")

# API key from secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("models/gemini-1.5-flash")

# Session state to track chat
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat()
    st.session_state.history = []  # Stores (user, bot) message pairs

# Display chat history like ChatGPT
for i, (user_msg, bot_msg) in enumerate(st.session_state.history):
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_msg)
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(bot_msg)

# Input box
user_input = st.chat_input("Type your message...")

if user_input:
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Gemini is typing..."):
            try:
                response = st.session_state.chat.send_message(user_input)
                bot_reply = response.text
            except Exception as e:
                bot_reply = f"❌ Error: {e}"
            st.markdown(bot_reply)

    # Save to history
    st.session_state.history.append((user_input, bot_reply))
