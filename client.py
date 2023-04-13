#   recive the message from the sender
#   decreipt the recived number from the sender
#   find the 5 character corresponding to the recived number
import sympy
import random
import math
import threading
import socket


HEADER = 64
PORT = 5050
FORMAT = "utf-8"
DISCONECTE_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())

ADDR = (SERVER, PORT)
# bind the socket
ciennt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect the client to the server
ciennt.connect(ADDR)

finish_get_keys = False


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    ciennt.send(send_length)
    ciennt.send(message)


def recive():
    msg_length = int(ciennt.recv(HEADER).decode(FORMAT))
    e = ciennt.recv(msg_length).decode(FORMAT)
    return e
#   take the message from the user
#   convert the message to sequence of numbers to send it
#   encript each number alone
#   send the encripted number by socket


def modify_message(message):
    length = len(message)
    new_string = ' '
    for i in range(length):
        find1 = message[i].isalpha()
        find2 = message[i].isnumeric()
        find3 = message[i] == ' '
        if (not (find1 or find2 or find3)):
            message = message.replace(message[i], new_string)
    if (len(message) % 5 != 0):
        reminder = 5-len(message) % 5
        message = message+' '*reminder
    return message


def alphabet_conversion(char):
    out = 0
    find1 = char.isnumeric()
    find2 = char.isalpha()
    find3 = char == ' '
    if (find1):
        out = int(char)
    elif (find2):
        out = ord(char)-ord('a')+10
    elif (find3):
        out = 36
    return out


def alpahbet_extraction(num):
    c = ''
    if(num < 10):
        c = str(num)
    elif(num < 36):
        num -= 10
        num += ord('a')
        c = chr(num)
    else:
        c = ' '
    return c


def extract_message(dec_message):
    c0, c1, c2, c3, c4 = '', '', '', '', ''

    num = dec_message % 37
    c0 = alpahbet_extraction(num)

    dec_message = (dec_message-num)//37
    num = dec_message % 37
    c1 = alpahbet_extraction(num)

    dec_message = (dec_message-num)//37
    num = dec_message % 37
    c2 = alpahbet_extraction(num)

    dec_message = (dec_message-num)//37
    num = dec_message % 37
    c3 = alpahbet_extraction(num)

    dec_message = (dec_message-num)//37
    num = dec_message % 37
    c4 = alpahbet_extraction(num)

    message = c0+c1+c2+c3+c4
    return message


def get_numeric_sequnce(message):
    sequence = []
    sequence_size = len(message)//5
    for i in range(sequence_size):
        block = message[5*i:5*i+5]
        block_number = 0
        for j in range(5):
            block_number += pow(37, j) * alphabet_conversion(block[j])
        sequence.append(block_number)
    return sequence


def init_RSA():
    bit_size = int(
        input("Please enter the size of the publick key N in bits: "))
    bit_size_p = bit_size//2
    bit_size_q = bit_size-bit_size_p

    lower_range_p = 1 << (bit_size_p-1)
    upper_range_p = sum(1 << i for i in range(bit_size_p))
    p = sympy.randprime(lower_range_p, upper_range_p)

    lower_range_q = 1 << (bit_size_q-1)
    upper_range_q = sum(1 << i for i in range(bit_size_q))
    q = sympy.randprime(lower_range_q, upper_range_q)
    N = p*q
    phai = (p-1)*(q-1)
    e = random.randint(2, phai)
    temp = math.gcd(phai, e)
    while temp > 1:
        e = e//temp
        temp = math.gcd(phai, e)
    d = pow(e, -1, phai)
    return p, q, N, phai, e, d


def get_public_key():
    print('hi1', flush=True)
    rec_e = int(recive())
    print('hi2', rec_e, flush=True)
    # send("ok")
    rec_N = int(recive())
    print('hi3', rec_N, flush=True)
    finish_get_keys = True
    return rec_e, rec_N


def send_public_key(e, N):
    send(str(e))
    send(str(N))


def encript(num, reciver_e, reciver_N):
    encripted_num = pow(num, reciver_e, reciver_N)
    return encripted_num


def decript(encripted_num, d, N):
    dec_message = pow(encripted_num, d, N)
    return dec_message


def handle_recive(e, d, N, ciennt):
    # befor recive i need to send my public key to the other side
    send_public_key(e, N)
    while (finish_get_keys == False):
        ds = 12
    print('start reciving', flush=True)
    while True:
        sequence_len = int(recive())
        print(sequence_len)
        message = ''
        for i in range(sequence_len):
            encripted_num = int(recive())
            dec_message = decript(encripted_num, d, N)
            message = message+extract_message(dec_message)
        print("recived:"+message, flush=True)


# init the bublic and private key of the
p, q, N, phai, e, d = init_RSA()
print("the parameters of the RSA is:", flush=True)
print(f"p={p}, q={q}, N={N}, phai={phai}, e={e}, d={d}", flush=True)

recive_thread = threading.Thread(target=handle_recive, args=(e, d, N, ciennt))
recive_thread.daemon = True
recive_thread.start()

# befor sending i need to get the public key of the other side
print('wait for server to give the public keys', flush=True)
reciver_e, reciver_N = get_public_key()
finish_get_keys = True
print(
    f"the public key (e,N) of the other side=({reciver_e},{reciver_N}) ", flush=True)

while True:
    message = input()
    if(message == "~~"):
        break
    message = modify_message(message)
    numeric_sequnce = get_numeric_sequnce(message)
    send(str(len(numeric_sequnce)))
    for i in range(len(numeric_sequnce)):
        encripted_num = encript(numeric_sequnce[i], reciver_e, reciver_N)
        send(str(encripted_num))
send(DISCONECTE_MESSAGE)
