import tkinter
import tkinter as ttk
from tkinter import ttk, Tk
from tkinter import filedialog
from PIL import ImageTk, Image, ImageDraw, ImageFont  # PILLOW

# ---- WINDOW BASIC SETTINGS ----
window = tkinter.Tk()
window.title("Image Watermarker")
window.config(pady=30, padx=50)
window.resizable(width=True, height=True)


# ---- FINESTRA DI DIALOGO PER CERCARE IL FILE ----
def file_explorer():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
    return file_path


# ---- APERTURA FOTO E ATTIVAZIONE OPZIONI ----
def open_image():
    file_path = file_explorer()
    global image  # Esporto la var image a globale per poterla riprendere successivamente da draw_watermark()
    image = Image.open(file_path).convert("RGBA")  # Converto l'immagine con Pillow a RGBA per gestire l'Alpha(trasparenza)
    img_resized = image.resize((300, 300))  # La ridimensiono per visualizzarla nell'app come preview
    img_resized = ImageTk.PhotoImage(img_resized)  # Converto l'immagine per Tkinter
    panel = ttk.Label(image=img_resized)  # Il label diventa un immagine
    panel.image = img_resized  # Visualizza l'immagine
    panel.grid(row=2, column=0, columnspan=3)
    text_label.grid()  # Qui dopo faccio apparire tutte le opzioni per applicare il watermark
    text_entry.grid()
    rgba_label.grid()
    font_size_label.grid()
    font_size_entry.grid()
    red_label.grid()
    green_label.grid()
    blue_label.grid()
    alpha_label.grid()
    red_entry.grid()
    green_entry.grid()
    blue_entry.grid()
    alpha_entry.grid()
    position_label.grid()
    position_combobox.grid()
    add_water_button.grid()


def show_full_size(img):
    img.show()

# ---- WATERMARKER ----
def draw_watermark():
    if "image" not in globals():
        return
    width, height = image.size
    txt_image = Image.new("RGBA", image.size, (255, 255, 255, 0))  # Creo un'immagine text vuota e trasparente che andrà a sovrapporsi all'image originale
    font = ImageFont.truetype("constanz.ttf", int(font_size_entry.get()))  # Imposto il font del testo di txt_image da Pillow
    draw = ImageDraw.Draw(txt_image)  # Questo è l'object di Pillow per scrivere su txt_image
    watermark_text = text_entry.get()  # Testo che voglio scrivere su txt_image
    position = position_combobox.get()  # Posizione del testo rispetto alla foto
    if position == "Center":
        a, b = 2, 2
    elif position == "Left":
        a, b = 20, 2
    elif position == "Right":
        a, b = 1.1, 2
    elif position == "Top":
        a, b = 2, 10
    elif position == "Bottom":
        a, b = 2, 1.1
    _, _, text_width, text_height = draw.textbbox((0, 0), watermark_text, font)  # estrapolo larghezza e altezza del testo
    x = (width - text_width) / a  # Per la posizione del testo(il centro del testo) x e y
    y = (height - text_height) / b
    draw.text((x, y), watermark_text, fill=(int(red_entry.get()), int(green_entry.get()), int(blue_entry.get()), int(alpha_entry.get())), font=font)  # Applico il testo
    new_image = Image.alpha_composite(image, txt_image)  # Sovrappongo le due immagini
    new_image_resized = new_image.resize((300, 300))
    water_img_resized = ImageTk.PhotoImage(new_image_resized)
    panel2 = ttk.Label(image=water_img_resized)  # Visualizzo la nuova immagine nell'app
    panel2.image = water_img_resized
    panel2.grid(row=2, column=4)
    full_size_b = ttk.Button(text="Show full size and save", command=lambda: show_full_size(new_image))
    full_size_b.grid(row=3, column=4)


# ---- APPLICATION STRUCTURE ----
title_label = ttk.Label(text="Upload an image from your drive to apply watermark")
upload_button = ttk.Button(text="Upload File", command=open_image)

text_label = ttk.Label(text="Text to write")
text_entry = ttk.Entry()
font_size_label = ttk.Label(text="Font size")
font_size_entry = ttk.Entry(width=5)
rgba_label = ttk.Label(text="RGBA Values:")
red_label = ttk.Label(text="Red")
green_label = ttk.Label(text="Green")
blue_label = ttk.Label(text="Blue")
alpha_label = ttk.Label(text="Alpha")
red_entry = ttk.Entry(width=5)
green_entry = ttk.Entry(width=5)
blue_entry = ttk.Entry(width=5)
alpha_entry = ttk.Entry(width=5)
position_label = ttk.Label(text="Text Position")
position_combobox = ttk.Combobox(values=["Center", "Left", "Right", "Top", "Bottom"], state="readonly")
add_water_button = ttk.Button(text="Add Watermark", command=draw_watermark)


# ---- GRID ----
title_label.grid(row=0, pady=5, column=0, columnspan=3)
upload_button.grid(row=1, pady=5, column=1)

text_label.grid(row=3, column=1, pady=(15, 1))
text_entry.grid(row=4, column=1)
font_size_label.grid(row=3, column=2, pady=(15, 1))
font_size_entry.grid(row=4, column=2)
rgba_label.grid(row=5, column=1, pady=(15, 1))
red_label.grid(row=6, column=0)
green_label.grid(row=6, column=1)
blue_label.grid(row=6, column=2)
alpha_label.grid(row=8, column=1)
red_entry.grid(row=7, column=0)
green_entry.grid(row=7, column=1)
blue_entry.grid(row=7, column=2)
alpha_entry.grid(row=9, column=1)
position_label.grid(row=10, column=1, pady=(15, 1))
position_combobox.grid(row=11, column=1)
add_water_button.grid(row=12, column=1, pady=(15, 1))

text_label.grid_remove()
text_entry.grid_remove()
font_size_label.grid_remove()
font_size_entry.grid_remove()
rgba_label.grid_remove()
red_label.grid_remove()
green_label.grid_remove()
blue_label.grid_remove()
alpha_label.grid_remove()
red_entry.grid_remove()
green_entry.grid_remove()
blue_entry.grid_remove()
alpha_entry.grid_remove()
position_label.grid_remove()
position_combobox.grid_remove()
add_water_button.grid_remove()

window.mainloop()
