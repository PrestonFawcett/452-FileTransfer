import tkinter as tk
import socket
from time import sleep
from _thread import *

window = tk.Tk()
window.title("Poker Server")
window.resizable(width=False, height=False)

# Middle frame consisting of two labels for displaying the host and port info
middleFrame = tk.Frame(window)
lblHost = tk.Label(middleFrame, text = "Address: X.X.X.X")
lblHost.pack(side=tk.LEFT)
lblPort = tk.Label(middleFrame, text = "Port:XXXX")
lblPort.pack(side=tk.LEFT)
middleFrame.pack(side=tk.TOP, pady=(5, 0))

# The client frame shows the client area
clientFrame = tk.Frame(window)
lblLine = tk.Label(clientFrame, text="**********Player List**********").pack()
scrollBar = tk.Scrollbar(clientFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
tkDisplay = tk.Text(clientFrame, height=10, width=30)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
scrollBar.config(command=tkDisplay.yview)
tkDisplay.config(yscrollcommand=scrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
clientFrame.pack(side=tk.BOTTOM, pady=(5, 10))


server = None
HOST_ADDR = "127.0.0.1"
HOST_PORT = 8080
client_name = " "
clients = []
clients_names = []
player_data = []


# Start server function
def start_server():
    global server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(socket.AF_INET)
    print(socket.SOCK_STREAM)

    server.bind((HOST_ADDR, HOST_PORT))
    server.listen(5)  # server is listening for client connection

    start_new_thread(accept_clients, (server, " "))

    lblHost["text"] = "Address: " + HOST_ADDR
    lblPort["text"] = "Port: " + str(HOST_PORT)

def accept_clients(the_server, y):
    while True:
        if len(clients) < 2:
            client, addr = the_server.accept()
            clients.append(client)

            # use a thread so as not to clog the gui thread
            start_new_thread(send_receive_client_message, (client, addr))

# Function to receive message from current client AND
# Send that message to other clients
def send_receive_client_message(client_connection, client_ip_addr):
    global server, client_name, clients, player_data, player0, player1

    client_msg = " "

    # send welcome message to client
    client_name = client_connection.recv(4096)
    if len(clients) < 2:
        client_connection.send(str.encode("welcome1"))
    else:
        client_connection.send(str.encode("welcome2"))

    clients_names.append(client_name)
    update_client_names_display(clients_names)  # update client names display

    if len(clients) > 1:
        sleep(1)

        # send opponent name
        print(type(clients_names[1]))
        print(type(clients_names[0]))
        clients[0].send(("opponent_name$" + str(clients_names[1])).encode())
        clients[1].send(("opponent_name$" + str(clients_names[0])).encode())
        # go to sleep

    while True:
        data = client_connection.recv(4096)
        if not data: break

        # get the player choice from received data
        player_choice = data[11:len(data)]

        msg = {
            "choice": player_choice,
            "socket": client_connection
        }

        if len(player_data) < 2:
            player_data.append(msg)

        if len(player_data) == 2:
            # send player 1 choice to player 2 and vice versa
            player_data[0].get("socket").send(("$opponent_choice" + str(player_data[1].get("choice"))).encode())
            player_data[1].get("socket").send(("$opponent_choice" + str(player_data[0].get("choice"))).encode())

            player_data = []

    # find the client index then remove from both lists(client name list and connection list)
    idx = get_client_index(clients, client_connection)
    del clients_names[idx]
    del clients[idx]
    client_connection.close()

    update_client_names_display(clients_names)  # update client names display


# Return the index of the current client in the list of clients
def get_client_index(client_list, curr_client):
    idx = 0
    for conn in client_list:
        if conn == curr_client:
            break
        idx = idx + 1

    return idx


# Update client name display when a new client connects OR
# When a connected client disconnects
def update_client_names_display(name_list):
    tkDisplay.config(state=tk.NORMAL)
    tkDisplay.delete('1.0', tk.END)

    for c in name_list:
        tkDisplay.insert(tk.END, c+"\n".encode('ascii'))
    tkDisplay.config(state=tk.DISABLED)

start_server()

window.mainloop()