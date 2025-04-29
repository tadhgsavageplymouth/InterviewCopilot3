# -*- coding: utf-8 -*-
# server.py — listen on 0.0.0.0:10000 and keep speaking every message until the client disconnects

import socket
import sys
from naoqi import ALProxy

LISTEN_IP   = '0.0.0.0'
LISTEN_PORT = 10000
ROBOT_IP    = '127.0.0.1'
ROBOT_PORT  = 9559

def main():
    # 1) Create the TTS proxy once
    try:
        tts = ALProxy('ALTextToSpeech', ROBOT_IP, ROBOT_PORT)
    except Exception, e:
        print 'ERROR: could not connect to ALTextToSpeech proxy:', e
        sys.exit(1)

    # 2) Create & bind listening socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((LISTEN_IP, LISTEN_PORT))
        server.listen(1)
    except Exception, e:
        print 'ERROR: failed to bind/listen:', e
        sys.exit(1)
    print 'Proxy listening on %s:%d' % (LISTEN_IP, LISTEN_PORT)

    # 3) Accept clients forever
    while True:
        conn, addr = server.accept()
        print 'Client connected from', addr
        try:
            # 4) Read multiple messages until client disconnects
            while True:
                try:
                    data = conn.recv(1024)
                except socket.error, e:
                    print 'Socket error on recv():', e
                    break
                if not data:
                    print 'Client closed connection cleanly.'
                    break
                text = data.strip()
                print '→ Received:', text

                # speak it
                try:
                    tts.say(text)
                except Exception, e:
                    print 'ERROR: TTS failed:', e

                # acknowledge back to the client
                try:
                    conn.sendall('Spoken: ' + text)
                except socket.error, e:
                    print 'Socket error on sendall():', e
                    break
        finally:
            conn.close()
            print 'Connection handler exiting — back to listening for new clients.'

if __name__ == '__main__':
    main()
