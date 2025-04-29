#!/usr/bin/env python3
"""
nao_client.py — simple wrapper to send text over TCP to the NAO proxy server.
"""
import socket

class NaoClient:
    def __init__(self, robot_ip, robot_port=10000, timeout=5):
        self.robot_ip = robot_ip
        self.robot_port = robot_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(timeout)
        self.sock.connect((self.robot_ip, self.robot_port))

    def send_message(self, text):
        # send the text
        self.sock.sendall(text.encode('utf-8'))
        # read ack
        data = self.sock.recv(1024)
        return data.decode('utf-8')

    def close(self):
        self.sock.close()
