from tkinter import *
from tkinter import ttk
import mysql.connector
import tkinter as tk
from PIL import ImageTk, Image
import customtkinter

def mostrarCalculo(on_return):

    # Configura la conexión a la base de datos
    db = mysql.connector.connect(
        host="localhost",
                user="root",
                password="12345678",
                database="platanex"
    )

    # Función para calcular el ratio y estimación, y guardar los datos en la tabla "calculos"
    def calcular_ratio_estimacion():
        semana_actual = int(semana_entry.get())

        # Consulta para obtener la cantidad de cinta y cajas
        cursor = db.cursor()
        cursor.execute(f"""
            SELECT cantidadCinta, cantidad
            FROM cosecha
            INNER JOIN caja ON cosecha.semana = caja.idEmbarque
            WHERE cosecha.semana = {semana_actual}
        """)
        result = cursor.fetchone()

        if result:
            cantidad_cinta = result[0]
            cantidad_caja = result[1]

            if cantidad_caja != 0:
                ratio = cantidad_cinta / cantidad_caja

                # Consulta para obtener la cantidad de cinta para la semana siguiente
                cursor.execute(f"""
                    SELECT cantidadCinta
                    FROM cosecha
                    WHERE semana = {semana_actual + 1}
                """)
                siguiente_cosecha = cursor.fetchone()

                if siguiente_cosecha:
                    cantidad_cinta_siguiente = siguiente_cosecha[0]
                    estimacion = cantidad_cinta_siguiente / ratio
                else:
                    estimacion = 0
            else:
                ratio = 0
                estimacion = 0

            # Insertar los datos calculados en la tabla "calculos"
            insert_query = "INSERT INTO calculos (semana, cantidadCinta, cantidadCaja, ratio, estimacion) VALUES (%s, %s, %s, %s, %s)"
            data = (semana_actual, cantidad_cinta, cantidad_caja, ratio, estimacion)
            cursor.execute(insert_query, data)
            db.commit()

            # Actualizar la tabla de datos guardados
            mostrar_calculos()

        cursor.close() 


    # Función para mostrar los datos guardados en la tabla "calculos"
    def mostrar_calculos():
        cursor = db.cursor()
        cursor.execute("SELECT semana, cantidadCinta, cantidadCaja, ratio, estimacion FROM calculos")
        results = cursor.fetchall()

        # Limpiar el contenido anterior de la tabla
        tabla_calculos.delete(*tabla_calculos.get_children())

        # Mostrar los resultados en la tabla
        for row in results:
            tabla_calculos.insert("", END, values=row)

        cursor.close()

    # Función para eliminar el registro seleccionado de la tabla "calculos"
    def eliminar_registro():
        seleccionado = tabla_calculos.selection()
        if seleccionado:
            item = tabla_calculos.item(seleccionado)
            semana = item['values'][0]

            # Eliminar el registro de la tabla "calculos"
            delete_query = f"DELETE FROM calculos WHERE semana = {semana}"
            cursor = db.cursor()
            cursor.execute(delete_query)
            db.commit()

            # Actualizar la tabla de datos guardados
            mostrar_calculos()

            cursor.close()

    # Crear la ventana principal
    window = Toplevel()
    window.title("Cálculo de Ratio y Estimación")
    window.geometry("720x500")

        # Cargar la imagen de fondo
    background_image = Image.open("fondomenu.png")
    background_image = background_image.resize((720, 500), Image.ANTIALIAS)
    background_image = ImageTk.PhotoImage(background_image)

    # Crear una etiqueta con la imagen de fondo
    background_label = tk.Label(window, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Mover la etiqueta de fondo detrás de los demás widgets
    background_label.lower()


    frame = tk.Frame(master=window)
    frame.place(x=120,y=50, width=520, height=440)
    

    # Crear los widgets de la interfaz
    semana_label = Label(frame, text="Semana actual:")
    semana_label.pack()

    semana_entry = customtkinter.CTkEntry(frame)
    semana_entry.pack(pady=14, padx=10)

    calcular_button = customtkinter.CTkButton(frame, text="Calcular Ratio y Estimación", command=calcular_ratio_estimacion)
    calcular_button.pack(pady=14, padx=10)

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

    def volver():
        window.destroy()
        on_return()

    eliminar_button = customtkinter.CTkButton(frame, text="Eliminar Registro", command=eliminar_registro)
    eliminar_button.pack()
    volverbutton = customtkinter.CTkButton(frame, text="volver", command=volver)
    volverbutton.pack(pady=14, padx=10)

    

    # Ejecutar la aplicación
    mostrar_calculos()
    window.mainloop()
