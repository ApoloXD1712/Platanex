import customtkinter
import tkinter as tk
from conexionDB import *
import Login
import UserLogin
from PIL import ImageTk, Image


root = tk.Tk()
root.geometry("720x500")

# Cargar la imagen de fondo
background_image = Image.open("fondomenu.png")
background_image = background_image.resize((720, 500), Image.ANTIALIAS)
background_image = ImageTk.PhotoImage(background_image)

# Crear una etiqueta con la imagen de fondo
background_label = tk.Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Mover la etiqueta de fondo detrás de los demás widgets
background_label.lower()

def mostrarInicio():
    root.deiconify()

def ocultarInicio():
    root.withdraw()
    Login.mostrarLogin(mostrarInicio)

def ocultarIniciouser():
    root.withdraw()
    UserLogin.mostrarLoginuser(mostrarInicio)



frame = tk.Frame(master=root)
frame.pack(pady=100, padx=100, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Platanex", font=("Roboto", 24))
label.pack(pady=12, padx=10)

button2 = customtkinter.CTkButton(master=frame, text="Administrador", command=ocultarInicio)
button2.pack(pady=12, padx=10)

button3 = customtkinter.CTkButton(master=frame, text="Usuario", command=ocultarIniciouser)
button3.pack(pady=14, padx=10)

root.mainloop()