import tkinter as tkk
from tkinter import ttk
from tkinter.simpledialog import askstring
import time
import datetime as dt
import csv
import pandas as pd

window = tkk.Tk()
window.title("Typing Speed Detector")
window.minsize(width=500, height=700)
window.maxsize(width=500, height=700)
window.config(padx=50, pady=50, bg='#AC99F2')  # imposto i margini laterali dove non ci sarà contenuto e il colo di sfondo

test_text = "Questo sarà quello che dovrai scrivere. Scrivi\n esattamente come lo vedi incluso di punteggiatura e accenti e non preoccuparti di andare a capo."
test = "Questo sarà quello che dovrai scrivere. Scrivi esattamente come lo vedi incluso di punteggiatura e accenti e non preoccuparti di andare a capo."


# -----FUNZIONI NECESSARIE AL FUNZIONAMENTE DELL'APPLICAZIONE----
def countdown(n=6):  # imposto un argomento in quanto sotto andrò a richiamare la funzione
    if 0 < n:
        n -= 1
        countdown_l.config(text=n)  # scrivo n sul label
        window.after(1000, countdown, n)  # dopo 1000ms rilancio la funzione countdown con argument n
    elif 0 == n:
        countdown_l.config(text="GO!!!")
        start_time()


def start_time():
    global start
    start = time.time()  # da in secondi il momento attuale e la porto in global come si legge sopra
    test_t.config(state="normal")
    test_t.delete("1.0", "end")  # cancella dall'inizio alla fine il contenuto di test_text() di partenza
    test_t.focus_set()  # mette il cursore sul text widget

def reset():
    test_t.config(state="normal")
    test_t.delete("1.0", "end")
    test_t.insert(index="1.0", chars=test_text)
    test_t.config(state="disabled")
    countdown_l.config(text="Countdown")

def get_entry(event=None):
    test_t.config(state="disabled")
    if test_t.get(1.0, "end-1c") == test_text.replace("\n", ""):  # .get rileva ciò che è stato scritto. Dopo uso .replace perchè il testo rileva non contiene nessun "a capo"
        end = time.time()
        seconds = round((end - start), 2)
        global char_per_sec, char_per_min  # li esporto a global poichè mi serviranno su save()
        char_per_sec = round((len(test_text.replace("\n", ""))) / seconds, 2)  #numero di chars diviso i secondi
        char_per_min = round((len(test_text.replace("\n", "")) / seconds) * 60)
        typing_speed.config(
            text=f"Your Typing Speed is... {char_per_min} chars per minute\nor {char_per_sec} chars per second.")
        save_score_b.grid()  # faccio apparire il tasto save
    else:
        typing_speed.config(text="Texts do not match, wait few seconds and press START to start again.")
        window.after(3000, reset)


def refresh_table():
    try:
        file = open("typing_scores.csv", mode="r")  # provo ad aprire il file
        file.close()
    except FileNotFoundError:  # se non esiste lo creo
        with open("typing_scores.csv", mode="w") as data:
            fields = ["Name", "Chars per minute", "Chars per second", "Date"]
            data_write = csv.writer(data)
            data_write.writerow(fields)
    finally:  #  in ogni caso farà questo
        with open("typing_scores.csv", mode="r") as data:
            data_df = pd.read_csv(data)  # apro il csv con pandas per semplicità mettendo le righe in ordine decrescente come una classifica
            data_df.sort_values("Chars per minute", ascending=False, inplace=True)
            x = -1
            for index, row in data_df.head(10).iterrows():  # faccio head(10) perchè voglio visualizzare solo i primi 10 in classifica
                x += 1
                my_table.insert(parent='', index='end', iid=x, text='',
                                values=(row["Name"], row["Chars per minute"], row["Chars per second"], row["Date"]))  # per ogni riga inserisco ogni riga di pandas


def save():
    date = dt.date.today().strftime("%d/%m/%Y")
    name = askstring("Name", "What is your name?")
    new_score = [name, str(char_per_min), str(char_per_sec), str(date)]  # preparo la lista da inserire nel csv
    with open("typing_scores.csv", mode="a", newline="") as data:
        data_append = csv.writer(data)
        data_append.writerow(new_score)
    save_score_b.grid_remove()
    saved_l.grid()  # faccio apparire messaggio di salvataggio riuscito
    for i in my_table.get_children():  # cancello tutte le righe della table record affinchè possa aggiornarla dopo il nuovo salvataggio lanciando refresh
        my_table.delete(i)
    refresh_table()


title_l = tkk.Label(text="Test your typing speed by typing the text below once the countdown is over.", bg='#AC99F2')
title_l.config(pady=5)
title_l.grid(row=0)

start_l = tkk.Label(text="Press start to initialize the countdown.\nOnce you are done typing press 'enter'on the keyboard.", bg='#AC99F2')
start_l.grid(row=1)
start_l.config(pady=5)

start_b = tkk.Button(text="START", command=countdown)  # con command lancio la funzione
start_b.grid(row=2)
start_b.config(pady=5)

countdown_l = tkk.Label(text="Countdown", fg="red", font="Times 20 bold", bg='#AC99F2')
countdown_l.grid(row=3)
countdown_l.config(pady=20)

test_t = tkk.Text()
test_t.grid(row=6)
test_t.insert(index="1.0", chars=test_text)
test_t.config(state="disabled", width=50, height=3, bg='black', fg='yellow')  # state disabled impedisce l'editing
test_t.bind("<Return>", get_entry)  # .bind attiva la funzione una volta premuto il tasto return(enter)

typing_speed = tkk.Label(text="", pady=5, bg='#AC99F2')
typing_speed.grid(row=7)

save_score_b = tkk.Button(text="Save", command=save)
save_score_b.grid(row=8)
save_score_b.grid_remove()

saved_l = tkk.Label(text="Successfully saved", fg="red")
saved_l.grid(row=8)
saved_l.grid_remove()

my_table_label = tkk.Label(text="Record Table", bg='#AC99F2')
my_table_label.grid(row=9)
my_table_label.config(pady=20)

table = tkk.Frame(window)
table.grid(row=10)
my_table = ttk.Treeview(table, show="headings")
my_table['columns'] = ("Name", "Chars per min", "Chars per sec", "Date")
my_table.grid(row=11)

my_table.column("#0", width=0, stretch="no")
my_table.column("Name", anchor="center", width=80)
my_table.column("Chars per min", anchor="center", width=90)
my_table.column("Chars per sec", anchor="center", width=80)
my_table.column("Date", anchor="center", width=80)

my_table.heading("Name", text="Name", anchor="center")
my_table.heading("Chars per min", text="Chars per min", anchor="center")
my_table.heading("Chars per sec", text="Chars per sec", anchor="center")
my_table.heading("Date", text="Date", anchor="center")

refresh_table()

window.mainloop()
