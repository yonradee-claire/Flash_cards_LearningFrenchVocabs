from tkinter import *
import random
from tkinter import messagebox

import pandas as pd
import csv

BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Arial"
flip_timer = None

# ---------------------------- Manage data ------------------------------- #
try:
    data = pd.read_csv("data/words_to_learn.csv")
    if data.empty:
        messagebox.showinfo(title="You're done!", message="You have no words left to learn from last session!")
        exit()
except FileNotFoundError:
    df = pd.read_csv("data/french_words.csv")
    records = df.to_dict(orient="records")
else:
    records = data.to_dict(orient="records")
# Convert each row into {French: English}
word_list = [{row["French"]: row["English"]} for row in records]
# print(word_list) [{'partie': 'part'}, {'histoire': 'history'}]
# print(len(word_list)) #101

wrong_words = []  # To store wrongly guessed words
current_word = {}  # To track the word shown currently

def game():
    global key,key_eng,label_lang,label_word, flip_timer, current_word
    if flip_timer:
        window.after_cancel(flip_timer)

    try:
        position = random.randint(0, len(word_list)-1)
        current_word = word_list[position]
        key = list(current_word.keys())[0] # get key which is french vocabs
        key_eng = current_word[key] # a dictionary lookup using the key (which is french vocab)
    except ValueError:
        messagebox.showinfo(title="You're done!", message="There is no more words left in the vocab bank")

    canvas.itemconfig(card_image, image=card_front_img)
    label_lang.config(text="French", bg="white", fg="black", font=(FONT_NAME, 40, "italic"))
    label_word.config(text=key, bg="white", fg="black", font=(FONT_NAME, 60, "bold"))

    flip_timer = window.after(3000, func=flip_and_show) # Add this to fix "Race condition"

# "Race condition" is where multiple after(3000, flip_and_show) timers overlap, causing the card to
# flip or change unexpectedly before 3 seconds seem to pass. This usually happens because each call
# to game() (via button or on start) sets a new after(3000) timer without canceling the previous one.
# Fix it by adding flip_timer, When game() is called again (by pressing a button or on startup),
# the previous timer is cancelled, so it doesn't flip the old word after you've already moved on to a new one.

# ---------------------------- Right button ------------------------------- #

def right_button():
    if current_word in word_list:
        word_list.remove(current_word) # remove the current_word that got right_button clicked from word_list
    print(len(word_list))
    game()

# ---------------------------- Wrong button ------------------------------- #

def wrong_button():
    if current_word not in wrong_words:
        wrong_words.append(current_word) # add the current_word that got wrong_button clicked to wrong_words
    game()

# ---------------------------- Flip Card ------------------------------- #

def flip_and_show():
    canvas.itemconfig(card_image, image=card_back_img)
    label_lang.config(text="English", bg="#91C2AF", fg="white", font=(FONT_NAME, 40, "italic")) # change label
    label_word.config(text=key_eng, bg="#91C2AF", fg="white", font=(FONT_NAME, 60, "bold")) # change label


# ---------------------------- Save your progress ------------------------------- #

def save_wrong_words():
    combined = wrong_words.copy() #use .copy(), you make a new, separate list, so changes to combined won't affect wrong_words
    for word in word_list:
        if word not in combined:
            combined.append(word)

    with open("data/words_to_learn.csv", "w", newline="", encoding="utf-8") as f:
        fieldnames = ["French", "English"] # This defines the column headers for the CSV file
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader() # This writes the header row at the top of the CSV:
        for pair in combined:
            for fr, en in pair.items(): # This gets the key and value from the pair dictionary:
                writer.writerow({"French": fr, "English": en})

# newline="" prevents Python from adding extra blank lines between rows in the CSV file (important on Windows).
# This creates a DictWriter object that allows you to write dictionaries (like {"French": ..., "English": ...})
# as rows in the CSV file. It knows which keys to expect from the fieldnames.
# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flashy Cards")
window.config(padx=20, pady=20, bg=BACKGROUND_COLOR)

# Card front & back
canvas = Canvas(width=850, height=800, highlightthickness=0, bg=BACKGROUND_COLOR)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_image = canvas.create_image(430, 400, image=card_front_img)
canvas.grid(column=0, row=0, columnspan=2)

# Create the labels only once otherwise those labels accumulate on top of
# each other and never disappear!
label_lang = Label(text="", bg="white", font=(FONT_NAME, 40, "italic"))
label_word = Label(text="", bg="white", font=(FONT_NAME, 60, "bold"))
canvas.create_window(420, 270, window=label_lang)
canvas.create_window(420, 420, window=label_word)

# Right Button
right_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_img, highlightthickness=0, command=right_button)

# Wrong Button
wrong_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_img, highlightthickness=0, command=wrong_button)

# Add buttons on canvas closer to the card bottom (adjust y as needed)
canvas.create_window(590, 730, window=right_button) # x,y coordination
canvas.create_window(250, 730, window=wrong_button) # x,y coordination

# Call flip_card after 3000 milliseconds (3 seconds)
game()
window.after(3000, func=flip_and_show)

def on_closing():
    save_wrong_words()
    window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)
#.protocol() is a method that handles window manager events
# — these are signals from the operating system (like clicking "X" to close the window).
# This is a special protocol name that means:
# "What should happen when the user tries to close the window?"
# By default, clicking "X" will simply destroy the window and exit the app immediately.
# on_closing --> This is your custom function that you want to run instead of the default behavior.

window.mainloop()