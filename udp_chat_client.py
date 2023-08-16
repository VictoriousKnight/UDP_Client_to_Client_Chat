import socket
import threading
import random

#creating client socket using IPV4 and UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.bind((socket.gethostbyname(socket.gethostname()), random.randint(13000, 60000)))

#taking username input
username = input("Username: ")

#defining recieve function
def recieve():
    while True:
        try:
            message, _ = client_socket.recvfrom(1024)
            print(f"{message.decode('utf-8')}")
            
        except:
            pass
        
thread = threading.Thread(target=recieve)
thread.start()

#sending messages to the server
client_socket.sendto(f"{username} is online...".encode('utf-8'), (socket.gethostbyname(socket.gethostname()), 12345))

while True:
    message = input()
    if message == "!DISCONNECT":
        client_socket.sendto(f"{username} left the chatroom...".encode('utf-8'), (socket.gethostbyname(socket.gethostname()), 12345))
        exit()
    else:
        client_socket.sendto(f"{username}: {message}".encode('utf-8'), (socket.gethostbyname(socket.gethostname()), 12345))
