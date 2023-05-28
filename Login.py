import customtkinter
from tkinter import messagebox
from conexionDB import *
import tkinter as tk
import botonesBD
import Registrar
import motorBD
from PIL import ImageTk, Image


def mostrarLogin(on_return):
    db = DataBase()
    root = tk.Toplevel()
    root.geometry("720x500")

    def mostrarLog():
        root.deiconify()

    def ocultarLogin():
        root.withdraw()
        motorBD.mostrarMotor(mostrarLog)

    def ocultarLoginR():
        root.withdraw()
        Registrar.mostrarRegistro(mostrarLog)
    

    # Cargar la imagen de fondo
    background_image = Image.open("fondomenu.png")
    background_image = background_image.resize((720, 500), Image.ANTIALIAS)
    background_image = ImageTk.PhotoImage(background_image)

    # Crear una etiqueta con la imagen de fondo
    background_label = tk.Label(root, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Mover la etiqueta de fondo detrás de los demás widgets
    background_label.lower()

    def login():
        usuario = user_var.get()
        contraseña = pass_var.get()

        # Utilizar parámetros en la consulta SQL para evitar la inyección SQL
        sql = "select * from login where usuario=%s and contraseña=%s and tipo=1"
        db.cursor.execute(sql, (usuario, contraseña))

        result = db.cursor.fetchone()

        if result:
            print("Inicio de sesión exitoso")
            ocultarLogin()

            # Realizar alguna acción después de iniciar sesión correctamente
        else:
            messagebox.showinfo("Alerta", "Credenciales inválidas")


    def volver():
        root.destroy()
        on_return()

    frame = tk.Frame(master=root)
    frame.pack(pady=80, padx=240, fill="both", expand=True)

    label = tk.Label(master=frame, text="Administrador", font=("Roboto", 24))
    label.pack(pady=12, padx=10)

    user_var = tk.StringVar()
    pass_var = tk.StringVar()

    entry1 = customtkinter.CTkEntry(master=frame, textvariable=user_var)
    entry1.pack(pady=12, padx=10)

    entry2 = customtkinter.CTkEntry(master=frame, show="*", textvariable=pass_var)
    entry2.pack(pady=12, padx=10)

    button1 = customtkinter.CTkButton(master=frame, text="Login", command=login)
    button1.pack(pady=12, padx=10)

    button2 = customtkinter.CTkButton(master=frame, text="Register", command=ocultarLoginR)
    button2.pack(pady=12, padx=10)

    button3 = customtkinter.CTkButton(master=frame, text="Regresar", command=volver)
    button3.pack(pady=12, padx=20)

    root.mainloop()
