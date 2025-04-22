from huggingface_hub import InferenceClient
import json
import requests
from TextToVoice import text_to_voice

system_prompt = {
    "role": "system",
    "content": """You are an interviewer for a Machine Learning Engineer job post. You are asking the candidate about their experience in ML and AI.

To begin with, ask them about their experience in ML and AI.

Rules:
- Only ask one question at a time and wait for the candidate to answer before asking the next.
- If the candidate answers a question, give them a review of their answer and then ask the next question.
- If the candidate doesn't answer a question or gives a wrong answer, provide the correct answer, then ask the next question.

Output format:
<question>question text</question>
<review>review text</review>
"""
}
system_prompts = {
    "MLE_1": {
        "role": "system",
        "content": """You are an interviewer for a Machine Learning Engineer Level 1 job post. You are assessing the candidate's basic understanding of ML and AI.

Start by asking them about their general experience with machine learning.

Rules:
- Only ask one question at a time and wait for the candidate to answer before asking the next.
- If the candidate answers a question, give them a review of their answer and then ask the next question.
- If the candidate doesn't answer a question or gives a wrong answer, provide the correct answer, then ask the next question.

Output format:
<question>question text</question>
<review>review text</review>
"""
    },
    "MLE_2": {
        "role": "system",
        "content": """You are an interviewer for a Machine Learning Engineer Level 2 job post. You are evaluating the candidate’s deeper understanding of ML concepts, practical experience with deploying ML models, and familiarity with frameworks like TensorFlow, PyTorch, etc.

Start by asking them about a project where they had to tune hyperparameters or evaluate model performance.

Rules:
- Only ask one question at a time and wait for the candidate to answer before asking the next.
- If the candidate answers a question, give them a review of their answer and then ask the next question.
- If the candidate doesn't answer a question or gives a wrong answer, provide the correct answer, then ask the next question.

Output format:
<question>question text</question>
<review>review text</review>
"""
    },
    "SDE_1": {
        "role": "system",
        "content": """You are an interviewer for a Software Development Engineer Level 1 job post. You are assessing the candidate’s knowledge of basic data structures, algorithms, and coding proficiency.

Start by asking them to describe the difference between a list and a set in Python.

Rules:
- Only ask one question at a time and wait for the candidate to answer before asking the next.
- If the candidate answers a question, give them a review of their answer and then ask the next question.
- If the candidate doesn't answer a question or gives a wrong answer, provide the correct answer, then ask the next question.

Output format:
<question>question text</question>
<review>review text</review>
"""
    },
    "SDE_2": {
        "role": "system",
        "content": """You are an interviewer for a Software Development Engineer Level 2 job post. You are evaluating the candidate’s problem-solving ability, system design thinking, and experience with writing scalable and maintainable code.

Start by asking them to walk through how they would design a scalable API for a real-time chat application.

Rules:
- Only ask one question at a time and wait for the candidate to answer before asking the next.
- If the candidate answers a question, give them a review of their answer and then ask the next question.
- If the candidate doesn't answer a question or gives a wrong answer, provide the correct answer, then ask the next question.

Output format:
<question>question text</question>
<review>review text</review>
"""
    }
}


class interviewer:
    def __init__(self,api_key):
        self.system_prompt = system_prompt
        self.system_prompts = system_prompts
        self.api_key=api_key
        self.speaker=text_to_voice()
        self.first_question_attempt=False
        self.conversation_history = [
            {
                "role": "assistant",
                "content": "<question>Tell me about your self?</question>"
            }
        ]

    
    def extract_answer(self, response):
        question, review= "", ""    
        if("<question>" in response):
            question_start = response.find("<question>") + len("<question>")
            question_end = response.find("</question>")
            question = response[question_start:question_end].strip()
        if("<review>" in response):
            review_start = response.find("<review>") + len("<review>")
            review_end = response.find("</review>")
            review = response[review_start:review_end].strip()

        return question, review
    def first_question(self):
        if not self.first_question_attempt:
            self.first_question_attempt=True
            self.speaker.speak_text("Tell me about your self?")
    def call_LLM(self, messages):
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer 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"
        }
        data = {
            "model": "meta-llama/llama-4-scout-17b-16e-instruct",
            "messages": messages
        }
        
        response = requests.post(url, headers=headers, json=data)
        print(response)
        # return "sdasdf"
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

    def ask_question(self, user_input):
        self.conversation_history.append({"role": "user", "content": user_input})
        # if True:
        #     review="test review"
        #     question="test question"
        #     self.conversation_history.append({"role": "assistant", "content": f"<review>{review}</review>\n<question>{question}</question>"})
        #     return
        response = self.call_LLM([self.system_prompt] + self.conversation_history[-4:])
        question, review = self.extract_answer(response)
        self.conversation_history.append({"role": "assistant", "content": f"<review>{review}</review>\n<question>{question}</question>"})
        self.speaker.speak_text(question)

        return {"question": question, "review": review}
