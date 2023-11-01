from tkinter import *
from tkinter import messagebox
import random
import pyperclip
from google_sheets import GoogleSheetAPI
import datetime
from tkinter.simpledialog import askstring
import os

date = datetime.datetime.today().strftime("%d/%m/%Y")

google = GoogleSheetAPI()
google.spreadsheet = os.getenv("google_passwords_sheet_id")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    password_entry.delete(0, END)  # prima di generare la password cancello ciò che c'è scritto dentro l'entry

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    letters_list = [random.choice(letters) for _ in range(nr_letters)]  # loop tante volte quante il numero di lettere selezionato sopra
    symbols_list = [random.choice(symbols) for _ in range(nr_symbols)]
    number_list = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = letters_list + symbols_list + number_list  # basta fare così per unire liste diverse

    random.shuffle(password_list)  # mischio i caratteri

    password = "".join(password_list)  # trasformo, con il method .join, le tre liste in una stringa i quali items saranno
    # , in questo caso, separati da ""(nulla)

    password_entry.insert(0, password)  # non è necessario il return perchè già così chiamo il comando da eseguire
    # per scrivere sul password entry la password generata

    pyperclip.copy(password)  # ho importato questo metodo che permette di copiare (ctrl-c) automaticamente(senza fare ctrl-c) la
    # password generata così da inserirle nel momento di creazione dell'account


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_entry.get().title()  # con .get() acquisisco ciò che è scritto dentro l'entry. title rende maiuscola ogni prima lettere di ogni parola
    username = username_entry.get()
    password = password_entry.get()

    if len(website) == 0 or len(password) == 0:  # se non ho scritto nulla dentro queste due entry, allora mi darà un
        # popup di errore, else la funzione procede
        messagebox.showinfo(title="Oops", message="Please don't leave any field empty!")
    else:
        # # messagebox è un method di tkinter che crea vari tipi di finestre di dialogo. Questa sotto in particolare
        # produce una boolean che se premuto OK è True
        is_ok = messagebox.askokcancel(title=website,
                                       message=f"These are the details entered: \n\nEmail/Username: {username}\nPassword: {password}\n\nIs it ok to save?")
        if is_ok:
            google.range_name = "passwords"
            result = google.execute_google_method("read")  # execute_google_method ritorna outcome
            data = result.json  # è l'attributo di outcome che contiene il json con tutti i dati delle passwords
            if website in data["Websites"]:
                keep_saving = messagebox.askquestion(title="Already exist", message=f"{website} is already in your database, would you like to continue anyway?")
                if keep_saving == "yes":
                    note = askstring(title="Notes", prompt="Would like to add notes to your new data?Click cancel to skip")
                    google.range_name = "passwords"
                    google.values = [[website, username, password, date, note]]
                    result = google.execute_google_method("append")
                    print(result)
                    if result.status == "OK":
                        messagebox.showinfo(title="Success", message="Data Saved")
                    elif result.status == "KO":
                        messagebox.showinfo(title="Oops",
                                            message="Something went wrong, try again or contact the administrator")
            else:
                note = askstring(title="Notes", prompt="Would like to add notes to your new data?Click cancel to skip")
                google.range_name = "passwords"
                google.values = [[website, username, password, date, note]]
                result = google.execute_google_method("append")
                print(result)
                if result.status == "OK":
                    messagebox.showinfo(title="Success", message="Data Saved")
                elif result.status == "KO":
                    messagebox.showinfo(title="Oops",
                                        message="Something went wrong, try again or contact the administrator")

        website_entry.delete(0, END)  # cancello ciò che ho scritto sulle entries per reinserire altri dati
        password_entry.delete(0, END)


# ---------------------------- SEARCH USERNAME/PASSWORD ------------------------------- #

def search():
    website = website_entry.get().title()
    google.range_name = "passwords"
    result = google.execute_google_method("read")
    data = result.json
    if website in data["Websites"]:
        index = data["Websites"].index(website)
        username = data["Usernames"][index]
        password = data["Passwords"][index]
        update = messagebox.askquestion(title=website, message=f"Username/Email: {username}\nPassword: {password}\n\nWould you like to update your data?")
        if update == "yes":
            website = askstring(title="Website", prompt="Type again the website name:")
            username = askstring(title="Username/Email", prompt="Type the username/email:")
            password = askstring(title="Password", prompt="Type the password:")
            note = askstring(title="Notes", prompt="Would like to update the notes too??Click cancel to skip")
            google.range_name = f"A{index + 2}"  # + 2 perchè parte da 2 la riga su sheets
            google.values = [[website, username, password, date, note]]
            google.execute_google_method("update")
    else:
        messagebox.showinfo(title="Not found", message="Sorry we couldn't find your data!")

    website_entry.delete(0, END)  # cancello ciò che ho scritto sulle entries per reinserire altri dati
    password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

canvas = Canvas(width=200, height=200)
lock_image = PhotoImage(file="logo.png")

canvas.create_image(100, 100, image=lock_image)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website")
website_label.grid(row=1, column=0)

password_label = Label(text="Password")
password_label.grid(row=3, column=0)

username_label = Label(text="Email/Username")
username_label.grid(row=2, column=0)

# Entries
website_entry = Entry(width=33)
website_entry.grid(row=1, column=1)
website_entry.focus()  # appena lancio l'app, il cursore lampeggierà qua

password_entry = Entry(width=33)
password_entry.grid(row=3, column=1)

username_entry = Entry(width=52)
username_entry.grid(row=2, column=1, columnspan=2)
username_entry.insert(0, "contact.magrone@gmail.com")

# Buttons
generate_pw_button = Button(text="Generate Password", command=generate_password)
generate_pw_button.grid(row=3, column=2)

add_button = Button(text="Add", width=44, command=save)
add_button.grid(row=4, column=1, columnspan=2)

search_button = Button(text="Search/Update", width=15, command=search)
search_button.grid(row=1, column=2)

window.mainloop()
