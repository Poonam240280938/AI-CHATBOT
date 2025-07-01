import streamlit as st
import google.generativeai as genai

# Configure your Gemini API key
genai.configure(api_key="AIzaSyAUttfqEGrmFH1IyCEd73yewo6vOCODdNY")

# Initialize model (flash version)
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# Session state to keep chat persistent
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat()
if "messages" not in st.session_state:
    st.session_state.messages = []

# Title
st.title("🤖 AI Chatbot")
st.caption("Type 'bye' to end the chat.")

# Show previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input box
user_input = st.chat_input("Say something...")

if user_input:
    # Append user input to session
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Check for exit command
    if user_input.strip().lower() == "bye":
        farewell = "Goodbye, My Lord! 👑"
        st.session_state.messages.append({"role": "assistant", "content": farewell})
        with st.chat_message("assistant"):
            st.markdown(farewell)
    else:
        try:
            # Send message to Gemini model
            response = st.session_state.chat.send_message(user_input)
            reply = response.text
        except Exception as e:
            reply = f"❌ Error: {e}"

        # Append model reply
        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)