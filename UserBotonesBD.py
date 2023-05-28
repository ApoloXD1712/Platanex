
from tkinter import *
import customtkinter
import UserCosecha
import UserCaja
import Userfinanzas
import Usercalculos_estimaciones

def mostrarBotones(on_return):

    customtkinter.set_appearance_mode("light")

    customtkinter.set_default_color_theme("dark-blue")

    root = customtkinter.CTk()
    root.geometry("800x768")
    #funciones para abrir frames

    def mostrarBot():
            root.deiconify()

    def ocultarBotonesco():
            root.withdraw()
            UserCosecha.mostrarCosecha(mostrarBot) 

    def ocultarBotonesca():
            root.withdraw()
            UserCaja.mostrarCaja(mostrarBot)

    def ocultarBotonesfi():
            root.withdraw()
            Userfinanzas.mostrarFinanzas(mostrarBot)

    def ocultarBotonescalc():
            root.withdraw()
            Usercalculos_estimaciones.mostrarCalculo(mostrarBot)
            
    def volver():
            root.destroy()
            on_return()
 
    #botones para abrir frames
    frame = customtkinter.CTkFrame(master=root)
    frame.pack(pady=20, padx=60, fill="both", expand= True)

    label = customtkinter.CTkLabel(master=frame, text="Usuario", font=("Roboto",24))
    label.pack(pady=100,padx=10)

    button1= customtkinter.CTkButton(master=frame, text="Cosecha", command=ocultarBotonesco)
    button1.pack(pady=12,padx=10)

    button2= customtkinter.CTkButton(master=frame, text="Embarque", command=ocultarBotonesca)
    button2.pack(pady=12,padx=10)

    button3= customtkinter.CTkButton(master=frame, text="Finanzas", command=ocultarBotonesfi)
    button3.pack(pady=12,padx=10)

    button4= customtkinter.CTkButton(master=frame, text="Calculo y estimaciones", command=ocultarBotonescalc)
    button4.pack(pady=12,padx=10)

    button5= customtkinter.CTkButton(master=frame, text="volver", command=volver)
    button5.pack(pady=12,padx=10)

    root.mainloop()
