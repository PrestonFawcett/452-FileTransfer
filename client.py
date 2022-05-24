import socket
import random
from Crypto.PublicKey import RSA
from Crypto.PublicKey import DSA
from Crypto.Random import get_random_bytes


ClientMultiSocket = socket.socket()
host = '127.0.0.1'
port = 2004
pnum1 = 0
pnum2 = 0
pnum3 = 0
phand = []
numberoptions = list(range(1, 13 + 3))
pnum1 = random.choice(numberoptions)
pnum2 = random.choice(numberoptions)
pnum3 = random.choice(numberoptions)

phand.append(pnum1)
phand.append(pnum2)
phand.append(pnum3)

def generate_RSA():
    private_key = RSA.generate(2048)
    public_key = private_key.publickey().export_key()
    return public_key, private_key

def generate_DSA():
    private_key = DSA.generate(2048)
    public_key = private_key.publickey().export_key()
    return public_key, private_key
    
while True:
    print("Choose RSA or DSA for encryption: ")
    x = input()
    if x == "RSA":
        pubkey, privkey = generate_RSA()
        break
    elif x == "DSA":
        pubkey, privkey = generate_DSA()
        break
    else:
        print("Invalid")

session_key = get_random_bytes(16)


def game_logic(you, opponent):
    winner = ""
    p1numchoice = 0
    p2numchoice = 0
    player1 = "you"
    player2 = "opponent"

    if p1numchoice == p2numchoice:
        winner = "draw"
    elif p1numchoice > p2numchoice:
        winner = player1
    elif p1numchoice < p2numchoice:
        winner = player2

    return winner


print('Waiting for Poker Server to implement')
try:
    ClientMultiSocket.connect((host, port))
except socket.error as e:
    print(str(e))
res = ClientMultiSocket.recv(2048)
print(res.decode('utf-8'))
while True:
    res = ClientMultiSocket.recv(2048)
    print(res.decode('utf-8'))
    print("Your hand:", phand)
    Input = input('Enter a card to play: ')

    if int(Input) not in phand:
        print("invalid selection")
    else:
        phand.remove(int(Input))
        ClientMultiSocket.send(str.encode(Input))
        res = ClientMultiSocket.recv(1024)
        print(res.decode('utf-8'))
ClientMultiSocket.close()
