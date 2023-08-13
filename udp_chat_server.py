import socket
import threading
import queue

#defining clients list using queue data structure
message_queue = queue.Queue()
clients_list = []

#creating server socket using IPV4 and UDPss
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((socket.gethostbyname(socket.gethostname()), 12345))
print("Server is starting...")

#no need to listen to the connections since it is an UDP server

#defining recieve function
def recieve():
    while True:
        try:
            #recieving data from the clients and inserting the tuple (message, address) into the queue asynchronously
            message, address = server_socket.recvfrom(1024)
            #print(message, address)
            message_queue.put((message, address)) 
        
        except:
            pass
        
#defining broadcast function
def broadcast():
    while True:
        #broadcasting only when the queue is not empty
        while not message_queue.empty():
            message, address = message_queue.get() #removing messages from the queue
            print(message.decode("utf-8"))
            
            #if the client is not in the client list then add it
            if address not in clients_list:
                clients_list.append(address)
                #print(clients_list)
                
            #sending back the data to the client    
            for client in clients_list:
                try:
                    if message.decode('utf-8').endswith("is online..."):
                        username = message.decode("utf-8")[0:message.decode("utf-8").index("is online...")] #describing the username using string slicing
                        server_socket.sendto(f"{username} entered the chatroom...".encode("utf-8"), client)
                        
                    else:
                        server_socket.sendto(message, client)
                        #print("test1")
                        
                except:
                    clients_list.remove(client)
                    
thread1 = threading.Thread(target=recieve)
thread2 = threading.Thread(target=broadcast)

thread1.start()
thread2.start()
