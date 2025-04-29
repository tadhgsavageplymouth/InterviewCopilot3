#!/usr/bin/env python3
"""
main.py — ChatGPT-driven interview on NAO with emotion detection
Usage:
    python3 main.py <topic> <nao_ip>
"""
import sys
import time
import cv2
import openai
from nao_communication.nao_client import NaoClient
from facial_recognition.emotion_detector import EmotionDetector

# Load your OpenAI key
KEY_FILE = r"C:\Users\tsavage2\InterviewCopilot\OpenAIAPIKey.txt"
with open(KEY_FILE, 'r') as f:
    openai.api_key = f.read().strip()

# ChatGPT settings
MODEL = "gpt-3.5-turbo"
TEMPERATURE = 0.7

def generate_question(topic, prev_answer=None):
    if prev_answer:
        prompt = (f"Given the previous answer: {prev_answer!r}, "
                  f"ask a deeper interview question on {topic}.")
    else:
        prompt = f"Ask a basic interview question about {topic}."
    resp = openai.ChatCompletion.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=TEMPERATURE
    )
    return resp.choices[0].message.content.strip()

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 main.py <topic> <nao_ip>")
        sys.exit(1)

    topic, nao_ip = sys.argv[1], sys.argv[2]
    client = NaoClient(nao_ip)
    detector = EmotionDetector()
    cap = cv2.VideoCapture(0)
    prev_answer = None

    try:
        while True:
            question = generate_question(topic, prev_answer)
            print("NAO asks:", question)
            client.send_message(question)

            # give the robot time to speak
            time.sleep(max(len(question.split())*0.5, 2))

            # grab one frame
            ret, frame = cap.read()
            if not ret:
                print("ERROR: Camera frame not available")
                break
            emotion = detector.detect_emotion(frame)
            print("Detected emotion:", emotion)

            # get your answer
            prev_answer = input("Your answer (or 'exit'): ")
            if prev_answer.lower() == 'exit':
                break

    except KeyboardInterrupt:
        print("Interrupted — exiting")
    finally:
        client.close()
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
