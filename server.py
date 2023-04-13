import sympy
import random
import math
import threading
import socket
import time


HEADER = 64
# step 1 define the port we will work on
PORT = 5050
# STEP 2 get the name of the server
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
# bind the socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# start the communication and wait for clints
server.bind(ADDR)
FORMAT = "utf-8"
DISCONECTE_MESSAGE = "!DISCONNECT"

# handle one connection between clinet and server

clients = []
clients_e = []
clients_N = []


def recive(client):
    msg_length = int(client.recv(HEADER).decode(FORMAT))
    e = int(client.recv(msg_length).decode(FORMAT))
    return e


def send(client, msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


def send_global(message, sender):
    for client in clients:
        if(client != sender):
            print(message, type(message))
            send(client, message)
            # client.send(message.encode(FORMAT))


def spread_public_keys():
    for i in range(len(clients)):
        client = clients[i]
        for j in range(len(clients)):
            if(i != j):
                send(client, str(clients_e[j]))
                send(client, str(clients_N[j]))


def add_client(client):

    e = int(recive(client))
    N = int(recive(client))
    clients.append(client)
    clients_e.append(e)
    clients_N.append(N)
    print('client ', client, 'has public key e= '+str(e), ', N= '+str(N))
    print(f"total number er of clints now is : {len(clients)}")


def remove_client(client):
    index = clients.index(client)
    clients.pop(index)
    clients_e.pop(index)
    clients_N.pop(index)


def handle_client(conn, addr):
    print("[NEW CONNECTION] ", addr, " connected.", flush=True)
    connected = True
    add_client(conn)
    spread_public_keys()
    print('finish spread keys', flush=True)
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONECTE_MESSAGE:
                connected = False
                remove_client(conn)
                print("remove client ", addr, flush=True)
                print(f"[ACTIVE CONNECTIONS] {len(clients)}", flush=True)
            else:
                print(f"[{addr}] {msg}", flush=True)
                send_global(str(msg), conn)
            # conn.send("Msg recived".encode(FORMAT))

# handle all connections between clints and the server


def start():
    server.listen()
    print("[LISTENING] server is listening on ", SERVER, flush=True)
    while True:
        coon, addr = server.accept()
        print(coon, flush=True)
        thread = threading.Thread(target=handle_client, args=(coon, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {len(clients)}", flush=True)


print("STARTING server is starting.....")
start()
