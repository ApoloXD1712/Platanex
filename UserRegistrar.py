import customtkinter
import tkinter as tk
from conexionDB import *
from PIL import ImageTk, Image

def mostrarRegistro(on_return):

    db = DataBase()

    customtkinter.set_appearance_mode("light")

    customtkinter.set_default_color_theme("dark-blue")

    root = tk.Toplevel()
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

    def volver():
        root.destroy()
        on_return()

    user_var = customtkinter.StringVar()
    pass_var = customtkinter.StringVar()

    def registro():
        usuario = user_var.get()
        contraseña = pass_var.get()
        val = (usuario, contraseña)
        sql = "INSERT INTO login (usuario, contraseña,tipo) VALUES (%s, %s,0)"
        db.cursor.execute(sql, val)
        db.connection.commit()
        volver()
        


    frame = customtkinter.CTkFrame(master=root)
    frame.pack(pady=100, padx=200, fill="both", expand=True)

    label = customtkinter.CTkLabel(
        master=frame, text="Administrador", font=("Roboto", 24))
    label.pack(pady=12, padx=10)

    user_var = customtkinter.StringVar()
    pass_var = customtkinter.StringVar()

    entry1 = customtkinter.CTkEntry(
        master=frame, placeholder_text="Username", textvariable=user_var)
    entry1.pack(pady=12, padx=10)

    entry2 = customtkinter.CTkEntry(
        master=frame, placeholder_text="Password", show="*", textvariable=pass_var)
    entry2.pack(pady=12, padx=10)

    button = customtkinter.CTkButton(
        master=frame, text="hacer registro", command=registro)
    button.pack(pady=12, padx=10)

    root.mainloop()