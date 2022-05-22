import socket
ClientMultiSocket = socket.socket()
host = '127.0.0.1'
port = 2004
print('Waiting for Poker Server to implement')
try:
    ClientMultiSocket.connect((host, port))
except socket.error as e:
    print(str(e))
res = ClientMultiSocket.recv(1024)
while True:
    Input = input('Enter a number between 1-15: ')
    ClientMultiSocket.send(str.encode(Input))
    res = ClientMultiSocket.recv(1024)
    print(res.decode('utf-8'))
ClientMultiSocket.close()