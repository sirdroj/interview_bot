import streamlit as st
from interviewer2 import interviewer
from TextToVoice import text_to_voice
from Transcorder import Transcorder

st.set_page_config(page_title="ML Interview Chat", layout="centered")

# Initialize TTS (if you're using it later)
text_to_voice = text_to_voice()

# Step 1: Initialize interviewer and transcorder
if 'interviewer' not in st.session_state:
    api_key = "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"
    st.session_state.interviewer = interviewer(api_key)
    st.session_state.transcorder = Transcorder(api_key)

# Step 2: Choose Interview Role
if 'interviewer_type' not in st.session_state:
    st.title("🎯 Choose Interview Role")
    options = list(st.session_state.interviewer.system_prompts.keys())

    selected_role = st.selectbox("Select the role you are interviewing for:", options)
    if st.button("Start Interview"):
        st.session_state.interviewer_type = selected_role
        st.session_state.interviewer.system_prompt = st.session_state.interviewer.system_prompts[selected_role]
        st.rerun()
    st.stop()

# Step 3: Main Interview Screen
st.title(f"🤖 {st.session_state.interviewer_type} Interview Bot")
st.markdown("Simulate a job interview for an ML Engineer role.")
st.markdown("---")
st.markdown("### Chat History")

# Ask first question if not already asked
st.session_state.interviewer.first_question()

for msg in st.session_state.interviewer.conversation_history:
    if msg['role'] == 'assistant':
        question, review = st.session_state.interviewer.extract_answer(msg['content'])
        if review:
            st.markdown(f"**🧠 Review:** {review}")
        if question:
            st.markdown(f"**🗣️ Interviewer:** {question}")
            st.session_state.latest_question = question

    elif msg['role'] == 'user':
        st.markdown(f"**👤 You:** {msg['content']}")

st.markdown("---")

# Text input option
user_input = st.text_input("Your answer:", key="input_box")

if st.button("Submit Answer") and user_input.strip():
    response = st.session_state.interviewer.ask_question(user_input)
    st.rerun()

# 🎙️ Voice recording toggle button
if 'recording' not in st.session_state:
    st.session_state.recording = False

if st.button("🎙️ Start/Stop Recording"):
    if st.session_state.recording:
        st.session_state.recording = False
        st.info("🔁 Stopping and transcribing...")
        try:
            text = st.session_state.transcorder.stop_recording()
            st.success("✅ Transcription Complete.")
            st.markdown(f"**📝 Transcribed:** {text}")
            response = st.session_state.interviewer.ask_question(text)
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error: {e}")
    else:
        st.session_state.recording = True
        try:
            st.session_state.transcorder.start_recording()
            st.success("🎙️ Recording started. Press again to stop.")
        except Exception as e:
            st.error(f"❌ Failed to start recording: {e}")

# Reset button
if st.button("Reset Interview"):
    for key in ["interviewer", "interviewer_type", "input_box", "recording"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()
