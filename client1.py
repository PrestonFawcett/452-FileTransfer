import tkinter as tk
from tkinter import messagebox
import socket
from time import sleep
from _thread import *
import random
from Crypto.PublicKey import RSA
from Crypto.PublicKey import DSA
from Crypto.Random import get_random_bytes

# MAIN GAME WINDOW
window_main = tk.Tk()
window_main.title("Poker Client")
window_main.resizable(width=False, height=False)
your_name = ""
dig_sig = ""
opponent_name = ""
game_round = 0
game_timer = 4
your_choice = ""
opponent_choice = ""
TOTAL_NO_OF_ROUNDS = 3
your_score = 0
opponent_score = 0

# generate cards
numberoptions = list(range(1, 13 + 3))
pnum1 = random.choice(numberoptions)
pnum2 = random.choice(numberoptions)
pnum3 = random.choice(numberoptions)

# booleans to control which cards are used
card1_used = False
card2_used = False
card3_used = False

# network client
client = None
HOST_ADDR = "127.0.0.1"
HOST_PORT = 8080

digital_signature = tk.Frame(window_main)
top_welcome_frame = tk.Frame(window_main)
lbl_ds = tk.Label(digital_signature, text="Digital Signature:")
lbl_name = tk.Label(top_welcome_frame, text="Name:")
lbl_ds.pack(side=tk.LEFT)
lbl_name.pack(side=tk.LEFT)
ent_ds = tk.Entry(digital_signature)
ent_name = tk.Entry(top_welcome_frame)
ent_ds.pack(side=tk.LEFT)
ent_name.pack(side=tk.LEFT)
btn_connect = tk.Button(top_welcome_frame, text="Connect", command=lambda: connect())
btn_connect.pack(side=tk.LEFT)
digital_signature.pack(side=tk.TOP)
top_welcome_frame.pack(side=tk.TOP)

top_message_frame = tk.Frame(window_main)
lbl_line = tk.Label(top_message_frame, text="***********************************************************").pack()
lbl_welcome = tk.Label(top_message_frame, text="")
lbl_welcome.pack()
lbl_line_server = tk.Label(top_message_frame, text="***********************************************************")
lbl_line_server.pack_forget()
top_message_frame.pack(side=tk.TOP)

top_frame = tk.Frame(window_main)
top_left_frame = tk.Frame(top_frame, highlightbackground="green", highlightcolor="green", highlightthickness=1)
lbl_your_score = tk.Label(top_left_frame, text="Your Score: " + str(your_score), font="Helvetica 13 bold")
lbl_opponent_score = tk.Label(top_left_frame, text="Opponent Score: " + str(opponent_score), font="Helvetica 13 bold")
lbl_your_score.grid(row=0, column=0, padx=5, pady=8)
lbl_opponent_score.grid(row=1, column=0, padx=5, pady=8)
top_left_frame.pack(side=tk.LEFT, padx=(10, 10))

top_right_frame = tk.Frame(top_frame, highlightbackground="green", highlightcolor="green", highlightthickness=1)
lbl_game_round = tk.Label(top_right_frame, text="Round (x) starts in", foreground="blue", font="Helvetica 14 bold")
lbl_timer = tk.Label(top_right_frame, text=" ", font="Helvetica 24 bold", foreground="blue")
lbl_game_round.grid(row=0, column=0, padx=5, pady=5)
lbl_timer.grid(row=1, column=0, padx=5, pady=5)
top_right_frame.pack(side=tk.RIGHT, padx=(10, 10))

top_frame.pack_forget()

middle_frame = tk.Frame(window_main)

lbl_line = tk.Label(middle_frame, text="***********************************************************").pack()
lbl_line = tk.Label(middle_frame, text="**** GAME LOG ****", font="Helvetica 13 bold", foreground="blue").pack()
lbl_line = tk.Label(middle_frame, text="***********************************************************").pack()

round_frame = tk.Frame(middle_frame)
lbl_round = tk.Label(round_frame, text="Round", font="Helvetica 13 bold")
lbl_round.pack()
lbl_your_choice = tk.Label(round_frame, text="Your choice: " + "None", font="Helvetica 11 bold")
lbl_your_choice.pack()
lbl_opponent_choice = tk.Label(round_frame, text="Opponent choice: " + "None", font="Helvetica 11 bold")
lbl_opponent_choice.pack()
lbl_result = tk.Label(round_frame, text=" ", foreground="blue", font="Helvetica 14 bold")
lbl_result.pack()
round_frame.pack(side=tk.TOP)

final_frame = tk.Frame(middle_frame)
lbl_line = tk.Label(final_frame, text="***********************************************************").pack()
lbl_final_result = tk.Label(final_frame, text=" ", font="Helvetica 13 bold", foreground="blue")
lbl_final_result.pack()
lbl_line = tk.Label(final_frame, text="***********************************************************").pack()
lbl_line = tk.Label(final_frame, text="**** YOUR HAND ****", font="Helvetica 13 bold", foreground="blue").pack()
final_frame.pack(side=tk.TOP)

middle_frame.pack_forget()

button_frame = tk.Frame(window_main)

btn_card1 = tk.Button(button_frame, text=pnum1, command=lambda: choice(pnum1, btn_card1), state=tk.DISABLED,
                      font="Helvetica 13 bold", bg='white', fg='red')
btn_card2 = tk.Button(button_frame, text=pnum2, command=lambda: choice(pnum2, btn_card2), state=tk.DISABLED,
                      font="Helvetica 13 bold", bg='white', fg='red')
btn_card3 = tk.Button(button_frame, text=pnum3, command=lambda: choice(pnum3, btn_card3), state=tk.DISABLED,
                      font="Helvetica 13 bold", bg='white', fg='red')
btn_card1.grid(row=0, column=0)
btn_card2.grid(row=0, column=1)
btn_card3.grid(row=0, column=2)
button_frame.pack(side=tk.BOTTOM)

button_frame.pack_forget()

# inputs: your score vs opponent score
def game_logic(you, opponent):
    p1choice = you

    # two raw variables to go through byte to int process to translate into readable number
    p2choice_raw1 = opponent.decode("utf-8")
    p2choice_raw2 = p2choice_raw1.replace('b', '')
    p2choice = int(p2choice_raw2.replace("'", ''))
    player0 = "you"
    player1 = "opponent"

    if p1choice == p2choice:
        winner = "draw"
    elif p1choice > p2choice:
        winner = player0
    elif p1choice < p2choice:
        winner = player1

    return winner


# inputs: todo for enabling/disabling buttons, three booleans to control which buttons have been used
def enable_disable_buttons(todo, usedbutton1, usedbutton2, usedbutton3):
    if todo == "disable":
        btn_card1.config(state=tk.DISABLED)
        btn_card2.config(state=tk.DISABLED)
        btn_card3.config(state=tk.DISABLED)

    else:
        if not usedbutton1:
            btn_card1.config(state=tk.NORMAL)
        if not usedbutton2:
            btn_card2.config(state=tk.NORMAL)
        if not usedbutton3:
            btn_card3.config(state=tk.NORMAL)


# activated when clicking the connect button
def connect():
    global your_name
    if len(ent_name.get()) < 1:
        tk.messagebox.showerror(title="ERROR!!!", message="Please enter a valid name")
    if ent_ds.get() != "RSA" and ent_ds.get() != "DSA":
        print(ent_ds.get())
        tk.messagebox.showerror(title="ERROR!!", message="Please enter a valid digital signature type (RSA or DSA)")
    else:
        your_name = ent_name.get()
        dig_sig = ent_ds.get()
        lbl_your_score["text"] = "Your Score: " + str(your_score)
        connect_to_server(your_name)


# the countdown function
def count_down(my_timer, nothing):
    global game_round
    global card1_used, card2_used, card3_used
    if game_round <= TOTAL_NO_OF_ROUNDS:
        game_round = game_round + 1

    lbl_game_round["text"] = "Round " + str(game_round) + " starts in"

    while my_timer > 0:
        my_timer = my_timer - 1
        print("game timer is: " + str(my_timer))
        lbl_timer["text"] = my_timer
        sleep(1)

    enable_disable_buttons("enable", card1_used, card2_used, card3_used)
    lbl_round["text"] = "Round - " + str(game_round)
    lbl_final_result["text"] = ""

# activated when a card button is selected
def choice(arg, button):
    global your_choice, client, game_round
    global card1_used, card2_used, card3_used
    your_choice = arg
    lbl_your_choice["text"] = "Your choice: " + str(your_choice)

    if client:
        client.send(("Game_Round" + str(game_round) + str(your_choice)).encode())
        if button == btn_card1:
            card1_used = True
        elif button == btn_card2:
            card2_used = True
        elif button == btn_card3:
            card3_used = True
        enable_disable_buttons("disable", card1_used, card2_used, card3_used)

# connection to server
def connect_to_server(name):
    global client, your_name
    global card1_used, card2_used, card3_used
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST_ADDR, HOST_PORT))
        client.send(str.encode(name))  # Send name to server after connecting

        # disable widgets
        btn_connect.config(state=tk.DISABLED)
        ent_name.config(state=tk.DISABLED)
        ent_ds.config(state=tk.DISABLED)
        lbl_name.config(state=tk.DISABLED)
        lbl_ds.config(state=tk.DISABLED)
        enable_disable_buttons("disable", card1_used, card2_used, card3_used)

        # start a thread to keep receiving message from server
        # do not block the main thread :)
        start_new_thread(receive_message_from_server, (client, "m"))
    except socket.error as e:
        tk.messagebox.showerror(title="ERROR!!!", message="Cannot connect to host: " + HOST_ADDR + " on port: " + str(
            HOST_PORT) + " Server may be Unavailable. Try again later")

# used to handle messages to and from the server
def receive_message_from_server(sck, m):
    global your_name, opponent_name, game_round
    global your_choice, opponent_choice, your_score, opponent_score
    global pnum1, pnum2, pnum3
    global card1_used, card2_used, card3_used

    while True:
        from_server = sck.recv(4096)

        if not from_server: break

        if from_server.startswith(str.encode('welcome')):
            if from_server == 'welcome1':
                lbl_welcome["text"] = "Server says: Welcome " + your_name + "! Waiting for player 2"
            elif from_server == 'welcome2':
                lbl_welcome["text"] = "Server says: Welcome " + your_name + "! Game will start soon"
            lbl_line_server.pack()

        elif from_server.startswith(str.encode('opponent_name$')):
            lbl_opponent_score["text"] = "Opponent Score: " + str(opponent_score)
            top_frame.pack()
            middle_frame.pack()
            button_frame.pack()

            # we know two users are connected so game is ready to start
            start_new_thread(count_down, (game_timer, ""))
            lbl_welcome.config(state=tk.DISABLED)
            lbl_line_server.config(state=tk.DISABLED)

        elif from_server.startswith(str.encode("$opponent_choice")):
            # get the opponent choice from the server
            opponent_choice = from_server.replace(b"$opponent_choice", b"")

            # figure out who wins in this round
            who_wins = game_logic(your_choice, opponent_choice)
            if who_wins == "you":
                your_score += 1
                round_result = "WIN"
            elif who_wins == "opponent":
                opponent_score += 1
                round_result = "LOSS"
            else:
                round_result = "DRAW"

            # Update GUI every round
            # two raw variables to go through byte to int process to translate into readable number
            oppchoice_raw1 = opponent_choice.decode('utf-8')
            oppchoice_raw2 = oppchoice_raw1.replace('b', '')
            final_oppchoice = oppchoice_raw2.replace("'", '')
            lbl_opponent_choice["text"] = "Opponent choice: " + str(final_oppchoice)
            lbl_result["text"] = "Round Result: " + str(round_result)
            lbl_your_score["text"] = "Your Score: " + str(your_score)
            lbl_opponent_score["text"] = "Opponent Score: " + str(opponent_score)

            # is it round 3?
            if game_round == TOTAL_NO_OF_ROUNDS:
                if your_score > opponent_score:
                    final_result = "You Win :)"
                    color = "green"
                elif your_score < opponent_score:
                    final_result = "You Lose :("
                    color = "red"
                else:
                    final_result = "It's a Draw"
                    color = "black"

                lbl_final_result["text"] = "FINAL RESULT: " + str(your_score) + " - " + str(
                    opponent_score) + ". " + final_result
                lbl_final_result.config(foreground=color)

                # reset cards used
                card1_used = False
                card2_used = False
                card3_used = False

                enable_disable_buttons("disable", card1_used, card2_used, card3_used)
                game_round = 0
                your_score = 0
                opponent_score = 0

                # generate new cards
                pnum1 = random.choice(numberoptions)
                pnum2 = random.choice(numberoptions)
                pnum3 = random.choice(numberoptions)

                btn_card1.config(text=pnum1)
                btn_card2.config(text=pnum2)
                btn_card3.config(text=pnum3)
                button_frame.pack_forget()
                button_frame.pack()

            # Start the timer
            start_new_thread(count_down, (game_timer, ""))

    sck.close()


window_main.mainloop()
