from tkinter import *
from tkinter import ttk
import tkinter as tk
from pymongo import MongoClient
import customtkinter


def mostrarCalculos(on_return):
    # Configura la conexión a la base de datos MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client.platanex
    # Función para calcular el ratio y estimación, y guardar los datos en la colección "calculos"
    def calcular_ratio_estimacion():
        semana_actual = int(semana_entry.get())

            # Obtener la cantidad de cinta y cajas
        cosecha = db.cosecha.find_one({"semana": semana_actual})
        if cosecha:
            cantidad_cinta = cosecha["cantidadCinta"]
            cedula = cosecha["cedula"]

            embarque = db.embarque.find_one({"cedula": cedula})
            if embarque:
                cantidad_caja = embarque["cantidad"]

                if cantidad_caja != 0:
                    ratio = cantidad_cinta / cantidad_caja

                cosecha_siguiente = db.cosecha.find_one({"semana": semana_actual + 1})
                if cosecha_siguiente:
                        cantidad_cinta_siguiente = cosecha_siguiente["cantidadCinta"]
                        estimacion = cantidad_cinta_siguiente / ratio
                else:
                        estimacion = 0
            else:
                    ratio = 0
                    estimacion = 0

                # Insertar los datos calculados en la colección "calculos"
            calculo = {
                "semana": semana_actual,
                "CantidadCinta": cantidad_cinta,
                "CantidadCaja": cantidad_caja,
                "ratio": ratio,
                "estimacion": estimacion
                }   
            db.calculos.insert_one(calculo)

                    # Actualizar la tabla de datos guardados
        mostrar_calculos()

        # Función para mostrar los datos guardados en la colección "calculos"
    def mostrar_calculos():
            resultados = db.calculos.find()

            # Limpiar el contenido anterior de la tabla
            tabla_calculos.delete(*tabla_calculos.get_children())

            # Mostrar los resultados en la tabla
            for resultado in resultados:
                semana = resultado["semana"]
                cantidad_cinta = resultado["CantidadCinta"]
                cantidad_caja = resultado["CantidadCaja"]
                ratio = resultado["ratio"]
                estimacion = resultado["estimacion"]
                tabla_calculos.insert("", END, values=(semana, cantidad_cinta, cantidad_caja, ratio, estimacion))

        # Función para eliminar el registro seleccionado de la colección "calculos"
    def eliminar_registro():
            seleccionado = tabla_calculos.selection()
            if seleccionado:
                item = tabla_calculos.item(seleccionado)
                semana = item['values'][0]

                # Eliminar el registro de la colección "calculos"
                db.calculos.delete_one({"semana": semana})

                # Actualizar la tabla de datos guardados
                mostrar_calculos()

        # Crear la ventana principal
    ventana = Tk()
    ventana.title("Cálculo de Ratio y Estimación")
    ventana.geometry("720x500")



    frame = tk.Frame(master=ventana)
    frame.place(x=120, y=50, width=520, height=400)

        # Crear los widgets de la interfaz
    semana_label = Label(frame, text="Semana actual:")
    semana_label.pack()

    semana_entry = customtkinter.CTkEntry(frame)
    semana_entry.pack()

    calcular_button = customtkinter.CTkButton(frame, text="Calcular Ratio y Estimación", command=calcular_ratio_estimacion)
    calcular_button.pack()

    tabla_calculos = ttk.Treeview(frame, columns=("semana", "cantidadCinta", "cantidadCaja", "ratio", "estimacion"))

    tabla_calculos["columns"] = ("semana", "cantidadCinta", "cantidadCaja", "ratio", "estimacion")
    tabla_calculos.column("#0", width=0, stretch=NO)
    tabla_calculos.column("semana", width=100, anchor=CENTER)
    tabla_calculos.column("cantidadCinta", width=100, anchor=CENTER)
    tabla_calculos.column("cantidadCaja", width=100, anchor=CENTER)
    tabla_calculos.column("ratio", width=100, anchor=CENTER)
    tabla_calculos.column("estimacion", width=100, anchor=CENTER)

    tabla_calculos.heading("semana", text="Semana")
    tabla_calculos.heading("cantidadCinta", text="Cant. Cinta")
    tabla_calculos.heading("cantidadCaja", text="Cant. Caja")
    tabla_calculos.heading("ratio", text="Ratio")
    tabla_calculos.heading("estimacion", text="Estimación")
    tabla_calculos.pack()


    eliminar_button = customtkinter.CTkButton(frame, text="Eliminar Registro", command=eliminar_registro)
    eliminar_button.pack()

    def volver():
        ventana.destroy()
        on_return()

    volverbutton = customtkinter.CTkButton(frame, text="volver", command=volver)
    volverbutton.pack()

        # Ejecutar la aplicación
    mostrar_calculos()
    ventana.mainloop()

