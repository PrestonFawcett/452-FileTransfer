import socket
import os
import random
from _thread import *

ServerSideSocket = socket.socket()
host = '127.0.0.1'
port = 2004
ThreadCount = 0
numberoptions = list(range(1, 11 + 3))

p1num1 = 0
p1num2 = 0
p1num3 = 0

p2num1 = 0
p2num2 = 0
p2num3 = 0
try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))
print('Socket is listening..')
ServerSideSocket.listen(3)


def multi_threaded_client(connection):
    connection.send(str.encode('Server is working:'))
    rounds = 1
    while rounds < 4:
        data = connection.recv(2048)
        response = 'You chose: ' + data.decode('utf-8')

        choice = int(data.decode('utf-8'))

        # testing separate rounds for single player, will need to implement way to keep track for multiple players
        if rounds == 1:
            if choice == p1num1:
                print("Round 1 is correct")
            else:
                print("no")
        elif rounds == 2:
            if choice == p1num2:
                print("Round 2 is correct")
            else:
                print("no")
        elif rounds == 3:
            if choice == p1num3:
                print("Round 3 is correct")
            else:
                print("no")
        else:
            break
        rounds += 1
        if not data:
            break
        connection.sendall(str.encode(response))
    connection.close()


while True:

    Client, address = ServerSideSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(multi_threaded_client, (Client,))
    ThreadCount += 1
    print('Player Count: ' + str(ThreadCount))

    # this means two players are connected. highly recommend you make a duplicate client to test this feature out, otherwise comment out the if statement
    if ThreadCount == 2:
        # player 1 numbers
        p1num1 = random.choice(numberoptions)
        p1num2 = random.choice(numberoptions)
        p1num3 = random.choice(numberoptions)

        # player 2 numbers
        p2num1 = random.choice(numberoptions)
        p2num2 = random.choice(numberoptions)
        p2num3 = random.choice(numberoptions)

        print(p1num1, p1num2, p1num3)

ServerSideSocket.close()