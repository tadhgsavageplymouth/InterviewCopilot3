#!/usr/bin/env python3
"""
client_chatgpt.py — fetch prompts from OpenAI ChatGPT and forward them to the NAO proxy server
Usage:
    python3 client_chatgpt.py
"""
import socket
import time
import openai
import os

# Configuration
SERVER_IP   = "169.254.242.81"  # NAO proxy server IP
SERVER_PORT = 10000
MODEL       = "gpt-3.5-turbo"

# Read OpenAI API key from file
KEY_FILE = r"C:\Users\tsavage2\InterviewCopilot\OpenAIAPIKey.txt"
with open(KEY_FILE, 'r') as f:
    openai.api_key = f.read().strip()

# Simple conversation history
conversation = [
    {"role": "system",
     "content": "You are a helpful assistant generating interview questions for a user speaking to a NAO robot."}
]

def fetch_chat_prompt():
    resp = openai.ChatCompletion.create(
        model=MODEL,
        messages=conversation,
        temperature=0.7,
    )
    msg = resp.choices[0].message.content.strip()
    conversation.append({"role": "assistant", "content": msg})
    return msg

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        print(f"Connecting to {SERVER_IP}:{SERVER_PORT}")
        sock.connect((SERVER_IP, SERVER_PORT))
        print("Connected.")

        while True:
            prompt = fetch_chat_prompt()
            print("Sending to NAO:", prompt)
            sock.sendall(prompt.encode('utf-8'))

            ack = sock.recv(1024)
            if not ack:
                print("Server closed connection.")
                break
            print("NAO proxy reply:", ack.decode('utf-8'))

            time.sleep(2)

if __name__ == "__main__":
    main()
