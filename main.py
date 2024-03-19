# Imports
import json 
from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
from pyperclip import copy

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate():
    # Dictionary Of All Possible Characters for Password
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    # Creating Password
    password_list = [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]
    shuffle(password_list)

    # Returning Password and Extras
    password = ''.join(password_list)
    password_input.delete(0, END)
    password_input.insert(0, password)
    copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def savePassword():
    # Get Input Data
    website = website_input.get()
    username = username_input.get()
    password = password_input.get()

    # Ensures All Fields are Filled
    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please Make Sure All Fields are Filled")
    else:
        # Creates Dictionary out of Fields
        new_data = {website: {"username": [username],"password": [password]}}
        try:
            # Getting Data and Updating Data from Json
            with open("password.json", 'r') as file:
                data = json.load(file)
                if website in data:
                    data[website]['username'] += [username]
                    data[website]['password'] += [password]
                else:
                    data.update(new_data)
        except FileNotFoundError:
            # Creating Json if Doesn't Exist
            with open("password.json", 'w') as file:
                json.dump(new_data, file, indent=4)
        else:
            # Dumps Updated Json into Data
            with open("password.json", 'w') as file:
                json.dump(data, file, indent=4)
        finally:
            # Does Extras Once Json Updating is Complete
            website_input.delete(0, END)
            password_input.delete(0, END)

# ---------------------------- FIND PASSWORD ------------------------------- #
def findPassword():
    try:
        with open("password.json", 'r') as file:
            data = json.load(file)
            website = website_input.get()
            if website in data:
                user_pass = {data[website]['username'][i]: data[website]['password'][i] for i in range(len(data[website]['username']))}
                message_list = [f"Email/Username: {username}\nPassword: {password}\n\n" for username, password in user_pass.items()]
                message = "".join(message_list)
                messagebox.showinfo(title=website, message=message)
            else:
                messagebox.showinfo(title="Oops", message=f"No Details for {website} Exists")
    except FileNotFoundError:
        messagebox.showinfo(title="Oops", message="No Data File Found")

# ---------------------------- UI SETUP ------------------------------- #
# Creating Window
window = Tk()
window.title("MyPass")
window.config(padx=50, pady=50, bg="white")

# Creating Logo Image
logo_img = PhotoImage(file="logo.gif")
canvas = Canvas(width=200, height=200, bg="white", highlightthickness=0)
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0, pady=5)

# Creating Labels
website_lb = Label(text="Website: ", bg="white")
username_lb = Label(text="Email/Username: ", bg="white")
password_lb = Label(text="Password: ", bg="white")
website_lb.grid(column=0, row=1, pady=5)
username_lb.grid(column=0, row=2, pady=5)
password_lb.grid(column=0, row=3, pady=5)

# Creating Inputs
username_input = Entry(width=39, highlightthickness=0)
password_input = Entry(width=21, highlightthickness=0)
website_input = Entry(width=21, highlightthickness=0)
username_input.grid(column=1, row=2, columnspan=2, pady=5)
password_input.grid(column=1, row=3, pady=5)
website_input.grid(column=1, row=1, pady=5)
website_input.focus()

# Creating Buttons
search_btn = Button(text="Search", highlightthickness=0, bg="white", command=findPassword, width=15)
generate_btn = Button(text="Generate Password", highlightthickness=0, bg="white", command=generate, width=15)
add_btn = Button(text="Add", width=36, highlightthickness=0, bg="white", command=savePassword)
search_btn.grid(column=2, row=1, pady=5)
generate_btn.grid(column=2, row=3, pady=5)
add_btn.grid(column=1, row=4, columnspan=2, pady=5)

# Setting Default Information on Relaunch
try:
    with open("password.json", 'r') as file:
        txt = json.load(file)
        username_input.insert(0, txt[list(txt)[-1]]['username'][-1])
except FileNotFoundError:
    pass
except json.decoder.JSONDecodeError:
    default_data = {'default_data': {"username": ['username'],"password": ['password']}}
    with open("password.json", 'w') as file:
        json.dump(default_data, file, indent=4)

# Keeping Window Open
window.mainloop()