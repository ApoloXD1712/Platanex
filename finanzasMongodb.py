from tkinter import *
from tkinter import ttk
import pymongo
from conexionMongodb import *
import customtkinter


def mostrarFinanzas(on_return):
    # Conexión a MongoDB
    cliente = pymongo.MongoClient("mongodb://localhost:27017/")
    db = cliente["platanex"]
    coleccion = db["finanzas"]

    # Función para calcular el pago
    def calcular_pago():
        tarifa = float(entry_tarifa.get())
        horas = float(entry_horas.get())
        pago = tarifa * horas
        entry_pago.delete(0, END)
        entry_pago.insert(0, str(pago))

    # Función para agregar un trabajador
    def agregar_trabajador():
        cedula = int(entry_cedula.get())
        nombre = entry_nombre.get()
        apellido = entry_apellido.get()
        trabajo = entry_trabajo.get()
        tarifa = float(entry_tarifa.get())
        horas = float(entry_horas.get())
        pago = float(entry_pago.get())

        trabajador = {
            "cedula": cedula,
            "nombreTrabajador": nombre,
            "apellido": apellido,
            "nombreTrabajo": trabajo,
            "tarifa": tarifa,
            "horas": horas,
            "pago": pago
        }

        coleccion.insert_one(trabajador)
        limpiar_campos()
        mostrar_trabajadores()

    # Función para mostrar los trabajadores en la tabla
    def mostrar_trabajadores():
        registros = treeview.get_children()
        for registro in registros:
            treeview.delete(registro)

        for trabajador in coleccion.find():
            cedula = trabajador["cedula"]
            nombre = trabajador["nombreTrabajador"]
            apellido = trabajador["apellido"]
            trabajo = trabajador["nombreTrabajo"]
            tarifa = trabajador["tarifa"]
            horas = trabajador["horas"]
            pago = trabajador["pago"]

            treeview.insert("", "end", text="", values=(cedula, nombre, apellido, trabajo, tarifa, horas, pago))

    # Función para limpiar los campos de entrada
    def limpiar_campos():
        entry_cedula.delete(0, END)
        entry_nombre.delete(0, END)
        entry_apellido.delete(0, END)
        entry_trabajo.delete(0, END)
        entry_tarifa.delete(0, END)
        entry_horas.delete(0, END)
        entry_pago.delete(0, END)

    # Crear la ventana principal
    # Crear la ventana principal
    ventana = Toplevel()
    ventana.title("PLATANEX")
    ventana.geometry("1366x900")

    # Establecer la imagen de fondo
    imagen = PhotoImage(file="fondo1.png")
    fondo = Label(ventana, image=imagen)
    fondo.place(x=0, y=0, relwidth=1, relheight=1)
    # Marco para los campos de entrada
    marco_entrada = LabelFrame(ventana, text="Datos del Trabajador")
    marco_entrada.pack(pady=20)

    # Campos de entrada
    label_cedula = Label(marco_entrada, text="Cédula:")
    label_cedula.grid(row=0, column=0, padx=5, pady=5)
    entry_cedula = customtkinter.CTkEntry(marco_entrada)
    entry_cedula.grid(row=0, column=1, padx=5, pady=5)

    label_nombre = Label(marco_entrada, text="Nombre:")
    label_nombre.grid(row=1, column=0, padx=5, pady=5)
    entry_nombre = customtkinter.CTkEntry(marco_entrada)
    entry_nombre.grid(row=1, column=1, padx=5, pady=5)

    label_apellido = Label(marco_entrada, text="Apellido:")
    label_apellido.grid(row=2, column=0, padx=5, pady=5)
    entry_apellido = customtkinter.CTkEntry(marco_entrada)
    entry_apellido.grid(row=2, column=1, padx=5, pady=5)

    label_trabajo = Label(marco_entrada, text="Trabajo:")
    label_trabajo.grid(row=3, column=0, padx=5, pady=5)
    entry_trabajo = customtkinter.CTkEntry(marco_entrada)
    entry_trabajo.grid(row=3, column=1, padx=5, pady=5)

    label_tarifa = Label(marco_entrada, text="Tarifa:")
    label_tarifa.grid(row=4, column=0, padx=5, pady=5)
    entry_tarifa = customtkinter.CTkEntry(marco_entrada)
    entry_tarifa.grid(row=4, column=1, padx=5, pady=5)

    label_horas = Label(marco_entrada, text="Horas:")
    label_horas.grid(row=5, column=0, padx=5, pady=5)
    entry_horas = customtkinter.CTkEntry(marco_entrada)
    entry_horas.grid(row=5, column=1, padx=5, pady=5)

    label_pago = Label(marco_entrada, text="Pago:")
    label_pago.grid(row=6, column=0, padx=5, pady=5)
    entry_pago = customtkinter.CTkEntry(marco_entrada)
    entry_pago.grid(row=6, column=1, padx=5, pady=5)

    # Botones
    boton_calcular = customtkinter.CTkButton(ventana, text="Calcular Pago", command=calcular_pago)
    boton_calcular.pack(pady=10)

    boton_agregar = customtkinter.CTkButton(ventana, text="Agregar Trabajador", command=agregar_trabajador)
    boton_agregar.pack(pady=10)

    # Marco para la tabla
    marco_tabla = LabelFrame(ventana, text="Trabajadores")
    marco_tabla.pack(padx=20, pady=10)

    # Tabla
    treeview = ttk.Treeview(marco_tabla, columns=("Cédula", "Nombre", "Apellido", "Trabajo", "Tarifa", "Horas", "Pago"))
    treeview.pack()
    treeview.column("#0", width=0, stretch=NO)
    treeview.column("Cédula", width=100, anchor=CENTER)
    treeview.column("Nombre", width=100, anchor=CENTER)
    treeview.column("Apellido", width=100, anchor=CENTER)
    treeview.column("Trabajo", width=100, anchor=CENTER)
    treeview.column("Tarifa", width=100, anchor=CENTER)
    treeview.column("Horas", width=100, anchor=CENTER)
    treeview.column("Pago", width=100, anchor=CENTER)

    treeview.heading("#0", text="")
    treeview.heading("Cédula", text="Cédula", anchor=W)
    treeview.heading("Nombre", text="Nombre", anchor=W)
    treeview.heading("Apellido", text="Apellido", anchor=W)
    treeview.heading("Trabajo", text="Trabajo", anchor=W)
    treeview.heading("Tarifa", text="Tarifa", anchor=W)
    treeview.heading("Horas", text="Horas", anchor=W)
    treeview.heading("Pago", text="Pago", anchor=W)

    # Mostrar los trabajadores al iniciar la aplicación
    mostrar_trabajadores()

    # Función para seleccionar una fila de la tabla
    def seleccionar_fila(event):
        fila_seleccionada = treeview.selection()
        if fila_seleccionada:
            valores = treeview.item(fila_seleccionada)['values']

            entry_cedula.delete(0, END)
            entry_cedula.insert(0, str(valores[0]))
            entry_nombre.delete(0, END)
            entry_nombre.insert(0, valores[1])
            entry_apellido.delete(0, END)
            entry_apellido.insert(0, valores[2])
            entry_trabajo.delete(0, END)
            entry_trabajo.insert(0, valores[3])
            entry_tarifa.delete(0, END)
            entry_tarifa.insert(0, str(valores[4]))
            entry_horas.delete(0, END)
            entry_horas.insert(0, str(valores[5]))
            entry_pago.delete(0, END)
            entry_pago.insert(0, str(valores[6]))

    # Asociar la función de selección de fila con el evento de clic en la tabla
    treeview.bind("<<TreeviewSelect>>", seleccionar_fila)

    # Función para cambiar/actualizar los datos en la base de datos y en la interfaz
    def actualizar_datos():
        fila_seleccionada = treeview.selection()[0]
        valores = treeview.item(fila_seleccionada, 'values')

        cedula = int(entry_cedula.get())
        nombre = entry_nombre.get()
        apellido = entry_apellido.get()
        trabajo = entry_trabajo.get()
        tarifa = float(entry_tarifa.get())
        horas = float(entry_horas.get())
        pago = float(entry_pago.get())

        trabajador_actualizado = {
            "cedula": cedula,
            "nombreTrabajador": nombre,
            "apellido": apellido,
            "nombreTrabajo": trabajo,
            "tarifa": tarifa,
            "horas": horas,
            "pago": pago
        }

        coleccion.update_one({"cedula": int(valores[0])}, {"$set": trabajador_actualizado})
        mostrar_trabajadores()
        limpiar_campos()

    boton_actualizar = customtkinter.CTkButton(ventana, text="Actualizar Datos", command=actualizar_datos)
    boton_actualizar.pack(pady=10)

    def eliminar_datos():
        fila_seleccionada = treeview.selection()[0]
        valores = treeview.item(fila_seleccionada, 'values')
        coleccion.delete_one({"cedula": int(valores[0])})
        mostrar_trabajadores()
        limpiar_campos()

    def volver():
        ventana.destroy()
        on_return()

    boton_eliminar = customtkinter.CTkButton(ventana, text="Eliminar Datos", command=eliminar_datos)
    boton_eliminar.pack(pady=10)
    boton_volver = customtkinter.CTkButton(ventana, text="Volver", command=volver)
    boton_volver.pack(pady=10)

    ventana.mainloop()