
import streamlit as st
import ollama

st.set_page_config(page_title="BhashaBuddy - Local Language Chatbot", page_icon="🗣️")
st.title("🗣️ BhashaBuddy - Local Language Chatbot")
st.markdown("Chat with an open-source LLM in your own language (Kannada, Hindi, Tamil, etc.)")

# Initialize session history
if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("Type your message:")

if user_input:
    # Append user message to history
    st.session_state.history.append(("user", user_input))
    
    # Query the model with instruction to provide both response and translation
    prompt = f"""Please respond to this message and also provide an English translation of your response.

User message: {user_input}

Format your response like this:
Response: [your response here]
English: [English translation here]"""
    
    response = ollama.chat(model='mistral', messages=[
        {'role': 'user', 'content': prompt}
    ])
    bot_reply = response['message']['content']
    
    # Try to parse the response to separate original and translation
    if "English:" in bot_reply:
        parts = bot_reply.split("English:")
        if len(parts) == 2:
            original = parts[0].replace("Response:", "").strip()
            translation = parts[1].strip()
            st.session_state.history.append(("bot", original, translation))
        else:
            st.session_state.history.append(("bot", bot_reply, ""))
    else:
        st.session_state.history.append(("bot", bot_reply, ""))

# Display conversation
for entry in st.session_state.history:
    if entry[0] == "user":
        st.markdown(f"**🧑 You:** {entry[1]}")
    else:
        # Bot response with original and translation
        if len(entry) == 3:  # Has translation
            st.markdown(f"**🤖 Bot:** {entry[1]}")
            st.markdown(f"**🔤 English:** {entry[2]}")
        else:  # Old format without translation
            st.markdown(f"**🤖 Bot:** {entry[1]}")
