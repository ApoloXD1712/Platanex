import customtkinter
import tkinter as tk
from conexionDB import *
import botonesMongodb
import botonesBD
from PIL import ImageTk, Image


def mostrarMotor(on_return):
    root = tk.Toplevel()
    root.geometry("500x350")

    # Cargar la imagen de fondo
    background_image = Image.open("fondomenu.png")
    background_image = background_image.resize((720, 500), Image.ANTIALIAS)
    background_image = ImageTk.PhotoImage(background_image)

    # Crear una etiqueta con la imagen de fondo
    background_label = tk.Label(root, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Mover la etiqueta de fondo detrás de los demás widgets
    background_label.lower()

    def mostrarMotor():
        root.deiconify()

    def ocultarMongo():
        root.withdraw()
        botonesMongodb.mostrarBotones(mostrarMotor)

    def ocultarMysql():
        root.withdraw()
        botonesBD.mostrarBotones(mostrarMotor)

    def volver():
        root.destroy()
        on_return()

    frame = customtkinter.CTkFrame(master=root)
    frame.pack(pady=20, padx=60, fill="both", expand=True)

    label = customtkinter.CTkLabel(master=frame, text="Platanex", font=("Roboto", 24))
    label.pack(pady=12, padx=10)

    button2 = customtkinter.CTkButton(master=frame, text="MySQL", command=ocultarMysql)
    button2.pack(pady=12, padx=10)

    button3 = customtkinter.CTkButton(master=frame, text="MongoDB", command=ocultarMongo)
    button3.pack(pady=14, padx=10)

    button4 = customtkinter.CTkButton(master=frame, text="Volver", command=volver)
    button4.pack(pady=14, padx=10)

    root.mainloop()