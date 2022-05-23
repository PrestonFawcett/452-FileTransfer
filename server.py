import socket
import sys
import random
from _thread import *

ServerSideSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 2004
ThreadCount = 0
numberoptions = list(range(1, 13 + 3))

players = []
player_data = []

p1num1 = 0
p1num2 = 0
p1num3 = 0
p1hand = []
p1numchoice = 0

p2num1 = 0
p2num2 = 0
p2num3 = 0
p2hand = []
p2numchoice = 0



try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))
print('Socket is listening..')
ServerSideSocket.listen(3)


# where we should put the bulk of the game logic
def multi_threaded_client(connection):
    p1score = 0
    p2score = 0

    if len(players) < 2:
        connection.send(str.encode('Welcome, Player 1!'))
    else:
        connection.send(str.encode('Welcome, Player 2!'))
        connection.sendall(str.encode('All players have connected!'))

    rounds = 1
    while rounds < 4:
        data = connection.recv(2048)
        response = 'You chose: ' + data.decode('utf-8')

        choice = int(data.decode('utf-8'))

        if not data:
            break
        connection.send(str.encode(response))

        if p1numchoice > p2numchoice:
            p1score += 1
        if p2numchoice > p1numchoice:
            p2score += 1

        if rounds == 4:
            print("Player 1:  " + p1score + "  Player 2:  " + p2score)
            if p1score > p2score:
                print("Player 1 wins")
                break
            if p2score > p1score:
                print("Player 2 wins")
                break
            else:
                print("Draw")
                break
        rounds += 1
    connection.close()


# to keep the server running
while True:
    Client, address = ServerSideSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(multi_threaded_client, (Client,))
    ThreadCount += 1
    print('Player Count: ' + str(ThreadCount))
    players.append(Client)
    print(players)

    # this means two players are connected. highly recommend you make a duplicate client to test this feature out,
    # otherwise comment out the if statement
    if len(players) == 2:
        # player 1 numbers
        p1num1 = random.choice(numberoptions)
        p1num2 = random.choice(numberoptions)
        p1num3 = random.choice(numberoptions)

        p1hand.append(p1num1)
        p1hand.append(p1num2)
        p1hand.append(p1num3)

        # player 2 numbers
        p2num1 = random.choice(numberoptions)
        p2num2 = random.choice(numberoptions)
        p2num3 = random.choice(numberoptions)

        p2hand.append(p2num1)
        p2hand.append(p2num2)
        p2hand.append(p2num3)

        #print(p1num1, p1num2, p1num3)

ServerSideSocket.close()
