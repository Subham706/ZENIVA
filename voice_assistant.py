import streamlit as st
import google.generativeai as genai
from streamlit_chat import message

def ai_assistant_page():

    # Page title
    st.title("🤖 ZENIVA - AI Health Assistant")
    st.caption("Ask me anything about health, fitness, diet, or wellness!")

    # Configure Gemini API
    genai.configure(api_key="AIzaSyBVs8RCNT4ftw1izLDVMa79DA0oy--sLLQ")

    model = genai.GenerativeModel("models/gemini-2.5-flash")  # or your working model

    # Session for chat history
    if "messages_ai" not in st.session_state:
        st.session_state["messages_ai"] = []

    # Display chat history
    for i, chat in enumerate(st.session_state["messages_ai"]):
        message(chat["user"], is_user=True, key=f"user_{i}")
        message(chat["bot"], key=f"bot_{i}")

    # User input box
    user_input = st.chat_input("Type your question...")

    if user_input:
        st.session_state["messages_ai"].append({"user": user_input, "bot": "..."})

        try:
            with st.spinner("Thinking..."):
                response = model.generate_content(user_input)
                reply = response.text
        except:
            reply = "⚠️ Sorry, I am unable to connect to AI service right now."

        # Save result
        st.session_state["messages_ai"][-1]["bot"] = reply

        st.rerun()
