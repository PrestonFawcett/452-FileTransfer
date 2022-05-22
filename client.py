import socket
import random
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

print('Waiting for Poker Server to implement')
try:
    ClientMultiSocket.connect((host, port))
except socket.error as e:
    print(str(e))
res = ClientMultiSocket.recv(1024)
while True:
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