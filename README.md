# 💼 ML Interview Chat App

An interactive **AI-powered mock interview application** built with **Streamlit**, powered by **Groq's LLM & TTS APIs**, and supporting **voice-based conversation**. The app simulates technical interviews for roles like **Machine Learning Engineer** or **Software Developer**, evaluates answers, and provides **spoken feedback** and **follow-up questions**.

---

## 🚀 Features

- 🧠 Role-based interview simulation (MLE Level 1, MLE Level 2, SDE Level 1/2)
- 💬 LLM-generated dynamic interview questions and answer reviews
- 🎙️ Voice input using real-time audio transcription (Whisper-v3)
- 🔊 AI voice output using Groq's PlayAI TTS
- 📜 Conversation history with review and questions
- 🔁 Reset interview anytime

---



## 📁 Project Structure

```
.
├── main.py                # Streamlit UI and interview logic
├── interviewer.py         # Interview agent logic using Groq LLM
├── TextToVoice.py         # TTS voice output (Groq PlayAI)
├── Transcorder.py         # Audio recording & transcription (Groq Whisper)
└── README.md              # Project documentation
```

---

## ⚙️ Installation & Setup

1. **Clone this repo**

```bash
git clone https://github.com/your-username/interview-chat-app.git
cd interview-chat-app
```

2. **Install required packages**

```bash
pip install -r requirements.txt
```


3. **Run the app**

```bash
streamlit run main.py
```

---

## 🧠 Workflow

1. **User selects a role** (e.g., Machine Learning Engineer Level 1).
2. The app initializes the interviewer agent with a system prompt tailored to the selected role.
3. **The interview begins** with a preloaded question.
4. **User answers** via:
   - Typing in the text box, or
   - Recording voice using “🎙️ Start/Stop Recording” (transcribes audio and submits).
5. The interviewer:
   - Reviews the answer,
   - Speaks out the review and next question using **Groq TTS**,
   - Updates chat history.
6. User continues the conversation in rounds.
7. At any time, the user can click **Reset Interview** to restart.

---

## 🛠️ Notes

- Uses **Groq LLM**: `llama-4-scout-17b-16e-instruct`
- **Speech-to-text**: Whisper Large v3 model
- **Text-to-speech**: PlayAI TTS voice: `Fritz-PlayAI`
- Works best with a microphone-enabled system for recording

---

## 📌 Example Roles

- `MLE_1`: Beginner-level ML questions
- `MLE_2`: Mid-level ML questions (deployment, frameworks)
- `SDE_1`: Basic Python/data structure questions
- `SDE_2`: Advanced coding and system design

---

## 📞 Voice Input Troubleshooting

If voice recording doesn't work:
- Ensure microphone permission is granted
- Ensure `pygame` and `sounddevice` modules are properly installed
- Check system audio device configuration

---

## 📃 License

This project is for educational use only. API keys should be kept private.
