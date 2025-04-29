#!/usr/bin/env python3
"""
openai_api.py — wraps OpenAI ChatCompletion for interview questions.
"""
import openai
import os

# read key from the same folder (or adjust the path)
KEY_FILE = os.path.expanduser('~/InterviewCopilot/OpenAIAPIKey.txt')
with open(KEY_FILE, 'r') as f:
    # if file contains e.g. OPENAI_API_KEY=sk-..., split on '='
    key = f.read().strip().split('=',1)[-1]
    openai.api_key = key

def generate_question(topic, previous_answer=None):
    """
    Ask GPT for a next interview question on `topic`.
    If previous_answer is provided, ask a deeper follow-up.
    """
    if previous_answer:
        prompt = (
            f"Given the previous answer: {previous_answer!r}, "
            f"ask a deeper follow-up interview question about {topic}."
        )
    else:
        prompt = f"Ask a basic interview question about {topic}."
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user","content":prompt}],
        temperature=0.7
    )
    return resp.choices[0].message.content.strip()
