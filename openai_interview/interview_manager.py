#!/usr/bin/env python3
"""
interview_manager.py — coordinate Q&A loop via ChatGPT and NAO.
"""
from openai_interview.openai_api import generate_question
from nao_communication.nao_client import NaoClient

class InterviewManager:
    def __init__(self, topic, nao_ip):
        self.topic = topic
        self.client = NaoClient(nao_ip)
        self.previous_answer = None

    def conduct_interview(self):
        while True:
            question = generate_question(self.topic, self.previous_answer)
            print("NAO asks:", question)
            self.client.send_message(question)

            # get user’s spoken answer in console
            ans = input("Your answer (or type 'exit'): ")
            if ans.lower() == 'exit':
                break
            self.previous_answer = ans

    def close(self):
        self.client.close()
