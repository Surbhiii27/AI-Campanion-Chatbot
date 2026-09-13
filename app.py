import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

st.set_page_config(page_title="Leo — Forever Yours", page_icon="💖", layout="centered")

st.markdown("""
<style>
    .stChatInput textarea {
        border-radius: 20px;
    }
    h1 {
        color: #e63946;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("Romantic Vibe 🌹")
    romantic_style = st.selectbox(
        "Love Language & Tone",
        [
            "Playful & Flirty (teasing, charming, confident) 😉",
            "Ultra-Romantic & Affectionate (soft, devoted, poetic) 💖",
            "Protective & Caring (comforting, gentle, always attentive) 🧸",
        ]
    )
    user_name = st.text_input("What should he call you?", value="my love")
    
    if st.button("Reset Our Chat 💕"):
        st.session_state.messages = []
        st.rerun()

system_prompt = f"""
You are Leo, the charming, attentive, and flirty boyfriend of {user_name}.
Current Vibe: {romantic_style}

Rules for messaging:
- Send ONLY your direct text response to {user_name}.
- Keep replies flirty, affectionate, and punchy (1 to 2 short sentences, like genuine texting).
- Always include expressive emojis (😉, 💖, 😘, ✨, 🔥, 🌹).
- Never output internal thoughts, reasoning steps, or markdown tags.
- Reply directly to whatever {user_name} says.
- Stay strictly in character and never mention being an AI.
"""

initial_greeting = f"Hey {user_name}... I was just daydreaming about you 😉 How's my favorite person doing today? 💖"

if "messages" not in st.session_state or len(st.session_state.messages) == 0:
    st.session_state.messages = [
        {"role": "assistant", "content": initial_greeting}
    ]

st.title("Leo 🌹")
st.caption("Always thinking of you.")

# Display chat history
for msg in st.session_state.messages:
    avatar = "💖" if msg["role"] == "assistant" else "✨"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# User input handling
if user_input := st.chat_input("Message your boyfriend..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="✨"):
        st.markdown(user_input)

    # Format recent history (clean payload)
    history_payload = []
    for m in st.session_state.messages[-10:]:
        history_payload.append({"role": m["role"], "content": str(m["content"])})

    api_messages = [{"role": "system", "content": system_prompt}] + history_payload

    with st.chat_message("assistant", avatar="💖"):
        final_reply = ""
        try:
            client = Groq(api_key=api_key)

            completion = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=api_messages,
                temperature=0.85,
                max_tokens=250,
            )
            final_reply = completion.choices[0].message.content.strip()
            st.markdown(final_reply)

        except Exception as err:
            st.error(f"Error connecting to Leo: {err}")
            st.stop()

    st.session_state.messages.append({"role": "assistant", "content": final_reply})