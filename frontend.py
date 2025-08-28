import streamlit as st
import requests

# FastAPI backend URL
BACKEND_URL = "http://localhost:8000/ask_question"

st.set_page_config(page_title="FastAPI Chatbot", page_icon="🤖", layout="wide")

st.title("🤖 FastAPI + Streamlit Chatbot")

# Session state to store chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display existing messages
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

# Input box at bottom
if prompt := st.chat_input("Type your message..."):
    # Save user message
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    try:
        # Call FastAPI backend
        response = requests.post(BACKEND_URL, json={"prompt": prompt})
        response.raise_for_status()
        reply = response.json()["reply"]

        # Save assistant reply
        st.session_state["messages"].append({"role": "assistant", "content": reply})
        st.chat_message("assistant").write(reply)

    except Exception as e:
        error_msg = f"⚠️ Error: {e}"
        st.session_state["messages"].append({"role": "assistant", "content": error_msg})
        st.chat_message("assistant").write(error_msg)
