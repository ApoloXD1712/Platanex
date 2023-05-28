import customtkinter
import tkinter as tk
import UserCosechaMongo
import UserEmabrqueMongo
import UserFinanzasMongo
import UserCalculosMongo
from PIL import ImageTk, Image

def mostrarBotones(on_return):


    root = tk.Toplevel()
    root.geometry("720x500")
    # Cargar la imagen de fondo
    background_image = Image.open("fondomenu.png")
    background_image = background_image.resize((720, 500), Image.ANTIALIAS)
    background_image = ImageTk.PhotoImage(background_image)

    # Crear una etiqueta con la imagen de fondo
    background_label = tk.Label(root, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

        #funciones para abrir frames

    def mostrarBot():
        root.deiconify()

    def ocultarBotonesco():
        root.withdraw() 
        UserCosechaMongo.mostrarCosecha(mostrarBot)

    def ocultarBotonesca():
        root.withdraw()
        UserEmabrqueMongo.mostrarEmbarque(mostrarBot)

    def ocultarBotonesfi():
        root.withdraw()
        UserFinanzasMongo.mostrarFinanzas(mostrarBot)

    def ocultarBotonescalc():
        root.withdraw()
        UserCalculosMongo.mostrarCalculos(mostrarBot)
            
    def volver():
        root.destroy()
        on_return()


    #botones para abrir frames
    frame = tk.Frame(master=root)
    frame.pack(pady=85, padx=245, fill="both", expand= True)

    label = tk.Label(master=frame, text="Administrador", font=("Roboto",24))
    label.pack(pady=12,padx=10)

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