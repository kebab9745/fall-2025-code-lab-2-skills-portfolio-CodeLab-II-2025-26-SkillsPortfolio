import tkinter as tk
from tkinter import messagebox
import random

# store all jokes here
jokes = []

# keep track of current joke parts
current_setup = ""
current_punchline = ""

# read jokes from the text file
def loadJokes():
    global jokes
    try:
        file = open("randomJokes.txt", "r")
        jokes = file.readlines()  # grab all lines
        file.close()
    except:
        # show error if file is missing
        messagebox.showerror("Error", "Cannot find randomJokes.txt file!")

# pick a random joke and split it into setup and punchline
def getRandomJoke():
    global current_setup, current_punchline
    
    # make sure we have jokes loaded
    if len(jokes) == 0:
        messagebox.showerror("Error", "No jokes found!")
        return
    
    # grab random joke from list
    joke = random.choice(jokes)
    joke = joke.strip()  # remove extra spaces
    
    # split joke at the question mark
    if "?" in joke:
        parts = joke.split("?")
        current_setup = parts[0] + "?"  # setup part (the question)
        current_punchline = parts[1]     # punchline part (the answer)
    else:
        # if no question mark, just show whole joke
        current_setup = joke
        current_punchline = ""

# when user clicks "tell me a joke" button
def tellJoke():
    getRandomJoke()
    setup_label.config(text=current_setup)  # show the setup
    punchline_label.config(text="")          # hide punchline for now
    show_btn.config(state="normal")          # enable the show punchline button

# reveal the punchline when user clicks button
def showPunchline():
    punchline_label.config(text=current_punchline)  # display punchline
    show_btn.config(state="disabled")                # disable button so they cant spam it

# get another joke
def nextJoke():
    tellJoke()

# close the app
def quitApp():
    window.quit()

# create main window
window = tk.Tk()
window.title("Joke Teller")
window.geometry("500x400")

# load jokes when app starts
loadJokes()

# title at top
title_label = tk.Label(window, text="Joke Assistant", font=("Arial", 20))
title_label.pack(pady=20)

# button to get a joke
alexa_btn = tk.Button(window, text="Alexa tell me a Joke", font=("Arial", 12), width=20, command=tellJoke)
alexa_btn.pack(pady=10)

# label to show joke setup
setup_label = tk.Label(window, text="", font=("Arial", 14), wraplength=450)
setup_label.pack(pady=20)

# button to reveal punchline (starts disabled)
show_btn = tk.Button(window, text="Show Punchline", font=("Arial", 12), width=15, command=showPunchline, state="disabled")
show_btn.pack(pady=10)

# label to show punchline
punchline_label = tk.Label(window, text="", font=("Arial", 12), wraplength=450)
punchline_label.pack(pady=10)

# button to get next joke
next_btn = tk.Button(window, text="Next Joke", font=("Arial", 12), width=15, command=nextJoke)
next_btn.pack(pady=10)

# button to exit app
quit_btn = tk.Button(window, text="Quit", font=("Arial", 12), width=15, command=quitApp)
quit_btn.pack(pady=10)

# start the app
window.mainloop()