import streamlit as st
from interviewer import interviewer

st.set_page_config(page_title="ML Interview Chat", layout="centered")

# Step 1: Ask for Hugging Face token if not provided
if 'hf_token' not in st.session_state:
    st.title("🔐 Enter Hugging Face Token")
    hf_token_input = st.text_input("Hugging Face Token", type="password")
    st.markdown("how to get your token: link to guide (https://huggingface.co/docs/hub/en/security-tokens)")
    if st.button("Continue") and hf_token_input.strip():
        st.session_state.hf_token = hf_token_input
        st.rerun()
    st.stop()

# Step 2: Initialize interviewer if not already created
if 'interviewer' not in st.session_state:
    st.session_state.interviewer = interviewer(st.session_state.hf_token)

# Step 3: Choose interviewer type
if 'interviewer_type' not in st.session_state:
    st.title("🎯 Choose Interview Role")
    options = list(st.session_state.interviewer.system_prompts.keys())
    selected_role = st.selectbox("Select the role you are interviewing for:", options)
    if st.button("Start Interview"):
        st.session_state.interviewer_type = selected_role
        st.session_state.interviewer.system_prompt = st.session_state.interviewer.system_prompts[selected_role]
        st.rerun()
    st.stop()

# ✅ Step 4: Main Interview Screen
st.title(f"🤖 {st.session_state.interviewer_type} Interview Bot")
st.markdown("Simulate a job interview for an ML Engineer role.")
st.markdown("---")
st.markdown("### Chat History")

for msg in st.session_state.interviewer.conversation_history:
    if msg['role'] == 'assistant':
        question, review = st.session_state.interviewer.extract_answer(msg['content'])
        if review:
            st.markdown(f"**🧠 Review:** {review}")
        if question:
            st.markdown(f"**🗣️ Interviewer:** {question}")
    elif msg['role'] == 'user':
        st.markdown(f"**👤 You:** {msg['content']}")

st.markdown("---")

# User input
user_input = st.text_input("Your answer:", key="input_box")

if st.button("Submit Answer") and user_input.strip():
    response = st.session_state.interviewer.ask_question(user_input)
    st.rerun()

# Optional reset button
if st.button("Reset Interview"):
    for key in ["interviewer", "hf_token", "interviewer_type", "input_box"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()
