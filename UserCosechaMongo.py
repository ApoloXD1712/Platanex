from tkinter import *
from tkinter import ttk
import tkinter.messagebox
from conexionMongodb import *
import customtkinter
import pymongo


def mostrarCosecha(on_return):
    ventana = Toplevel()
    ventana.title("PLATANEX")
    ventana.geometry("1366x768")
    imagen= PhotoImage(file="Usuario.png")
    Label(ventana, image=imagen, bd=0).pack()

    db = cliente
    cantidad = DoubleVar()
    color = StringVar()
    ubicacion = IntVar()
    cedula = StringVar()

    mongoColeccion = "cosecha"

    marco = LabelFrame(ventana, text="Cosecha", font=("Roboto", 24))
    marco.place(x=200,y=150, width=1020, height=110)
    #marco.configure(background=color_rgb)

    #labels y entrys

    #Cantidad
    lblCantidad = customtkinter.CTkLabel(marco, text="CANTIDAD", font=("Roboto", 11)).grid(column=0, row=0, padx=5, pady=5)
    txtCantidad = customtkinter.CTkEntry(marco, textvariable=cantidad)
    txtCantidad.grid(column=1, row=0)

    #Color
    lblColor = Label(marco, text="COLOR").grid(column=0, row=1, padx=5, pady=5)
    txtColor = customtkinter.CTkEntry(marco, textvariable=color)
    txtColor.grid(column=1, row=1)

    #ubicacion
    lblUbicacion = Label(marco, text="UBICACION").grid(column=2, row=0, padx=5, pady=5)
    txtUbicacion = customtkinter.CTkEntry(marco, textvariable=ubicacion)
    txtUbicacion.grid(column=3, row=0)

    #Cedula
    lblcedula = customtkinter.CTkLabel(marco, text="CEDULA").grid(column=2, row=1, padx=5, pady=5)
    comboCedula = ttk.Combobox(marco, state="readonly")
    comboCedula.grid(column=3, row=1)



    #Tabla lista cosechas
    marco1 = LabelFrame(ventana)
    marco1.place(x=200,y=270, width=600, height=250)

        

    tvCosechas = ttk.Treeview(marco1, selectmode=NONE)
    tvCosechas.grid(column=1, row=0 )
    tvCosechas["columns"] = ("Semana", "Color","Ubicacion","Cantidad", "Cedula")
    tvCosechas.column("#0", width=0, stretch=NO)
    tvCosechas.column("Semana", width=100, anchor=CENTER)
    tvCosechas.column("Color", width=100, anchor=CENTER)
    tvCosechas.column("Ubicacion", width=100, anchor=CENTER)
    tvCosechas.column("Cantidad", width=100, anchor=CENTER)
    tvCosechas.column("Cedula", width=100, anchor=CENTER)
    tvCosechas.heading("#0", text="")
    tvCosechas.heading("Semana", text="Semana", anchor=CENTER)
    tvCosechas.heading("Color", text="Color", anchor=CENTER)
    tvCosechas.heading("Ubicacion", text="Ubicacion", anchor=CENTER)
    tvCosechas.heading("Cantidad", text="Cantidad", anchor=CENTER)
    tvCosechas.heading("Cedula", text="Cedula", anchor=CENTER)
    tvCosechas.config(selectmode=BROWSE)


    #Botones y Acciones

    marco2 =  LabelFrame(ventana)
    marco2.place(x=718,y=270, width=500, height=250)

    lblmensajes = Label(marco2, text="", fg="green")
    lblmensajes.grid(column=0, row=4, columnspan=6)



    def mostrarDatos(tvCosechas):

        try:
            cliente = pymongo.MongoClient(url, serverSelectionTimeoutMS = tiempoFuera)
            baseDatos = cliente[mongoBaseDatos]
            coleccion = baseDatos[mongoColeccion]
            for documento in coleccion.find():
                id = documento["semana"]
                color = documento["colorCinta"]
                ubicacion = documento["ubicacion"]
                cantidad = documento["cantidadCinta"]
                cedula = documento["cedula"]

                tvCosechas.insert('', 'end', text = id, values=(id, color, ubicacion, cantidad, cedula))
            
            cliente.close()

        except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
            print("tiempo excedido")
        except pymongo.errors.ConnectionFailure as errorConexion:
            print("La conexion ha fallado")

    def cargarCedulas():
        try:
            cliente = pymongo.MongoClient(url, serverSelectionTimeoutMS=tiempoFuera)
            baseDatos = cliente[mongoBaseDatos]
            coleccion_finanzas = baseDatos["finanzas"]
            
            cedulas = coleccion_finanzas.distinct("cedula")
            
            comboCedula["values"] = cedulas
            
            cliente.close()
        except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
            print("Tiempo excedido")
        except pymongo.errors.ConnectionFailure as errorConexion:
            print("La conexión ha fallado")

    cargarCedulas()

    def limpiarCampos():
        cantidad.set("")  # Limpiar campo de cantidad
        color.set("")  # Limpiar campo de color
        ubicacion.set("")  # Limpiar campo de ubicación
        comboCedula.set("")  # Limpiar ComboBox de cédula

    def eliminarFila():
        item_seleccionado = tvCosechas.selection()
        if item_seleccionado:
            id = tvCosechas.item(item_seleccionado)['text']

            try:
                cliente = pymongo.MongoClient(url, serverSelectionTimeoutMS=tiempoFuera)
                baseDatos = cliente[mongoBaseDatos]
                coleccion = baseDatos[mongoColeccion]

                # Eliminar el documento de la colección
                coleccion.delete_one({"semana": int(id)})

                # Eliminar la fila de la interfaz
                tvCosechas.delete(item_seleccionado)

                lblmensajes.config(text="Fila eliminada", fg="green")

                cliente.close()
            except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
                print("Tiempo excedido")
            except pymongo.errors.ConnectionFailure as errorConexion:
                print("La conexión ha fallado")
        else:
            lblmensajes.config(text="Selecciona una fila para eliminar", fg="red")


    def seleccionarFila(event):
        item_seleccionado = tvCosechas.selection()
        if item_seleccionado:
            id = tvCosechas.item(item_seleccionado)['text']
            valores = tvCosechas.item(item_seleccionado)['values']
            
            cantidad.set(valores[3])
            color.set(valores[1])
            ubicacion.set(valores[2])
        else:
            lblmensajes.config(text="Selecciona una fila", fg="red")

    tvCosechas.bind("<<TreeviewSelect>>", seleccionarFila)

    def actualizarDatos():
        # Obtener el ID del elemento seleccionado en la combobox
        nuevo_id = int(comboCedula.get())
        
        # Obtener el ID del elemento seleccionado en la tabla
        item_seleccionado = tvCosechas.selection()
        if item_seleccionado:
            id = tvCosechas.item(item_seleccionado)['text']
            
            # Obtener los nuevos valores de los campos
            nueva_cantidad = cantidad.get()
            nuevo_color = color.get()
            nueva_ubicacion = ubicacion.get()
            
            try:
                cliente = pymongo.MongoClient(url, serverSelectionTimeoutMS=tiempoFuera)
                baseDatos = cliente[mongoBaseDatos]
                coleccion = baseDatos[mongoColeccion]
                
                # Obtener el valor actual de la columna "Semana"
                valor_semana = tvCosechas.item(item_seleccionado)['values'][0]
                
                # Actualizar los campos en el documento de la colección
                coleccion.update_one(
                    {"semana": valor_semana},
                    {"$set": {
                        "cantidadCinta": nueva_cantidad,
                        "colorCinta": nuevo_color,
                        "ubicacion": nueva_ubicacion,
                        "cedula": nuevo_id
                    }}
                )
                
                # Actualizar los valores en la interfaz
                tvCosechas.item(item_seleccionado, values=(valor_semana, nuevo_color, nueva_ubicacion, nueva_cantidad, nuevo_id))
                
                lblmensajes.config(text="Datos actualizados", fg="green")
                
                cliente.close()
            except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
                print("Tiempo excedido")
            except pymongo.errors.ConnectionFailure as errorConexion:
                print("La conexión ha fallado")
        else:
            lblmensajes.config(text="Selecciona una fila para actualizar", fg="red")


    def insertarDatos():
        nueva_cantidad = cantidad.get()
        nuevo_color = color.get()
        nueva_ubicacion = ubicacion.get()
        nuevo_id = int(comboCedula.get())

        try:
            cliente = pymongo.MongoClient(url, serverSelectionTimeoutMS=tiempoFuera)
            baseDatos = cliente[mongoBaseDatos]
            coleccion = baseDatos[mongoColeccion]

            # Obtener el valor máximo actual de la columna "Semana" en la base de datos
            valor_max_semana = coleccion.find_one(sort=[("semana", -1)])["semana"]

            # Generar el nuevo valor de la columna "Semana"
            nuevo_valor_semana = valor_max_semana + 1

            # Insertar los nuevos datos en la colección
            coleccion.insert_one({
                "semana": nuevo_valor_semana,
                "cantidadCinta": nueva_cantidad,
                "colorCinta": nuevo_color,
                "ubicacion": nueva_ubicacion,
                "cedula": nuevo_id
            })

            # Insertar la nueva fila en la interfaz
            tvCosechas.insert('', 'end', text=nuevo_valor_semana,
                            values=(nuevo_valor_semana, nuevo_color, nueva_ubicacion, nueva_cantidad, nuevo_id))

            lblmensajes.config(text="Datos insertados", fg="green")

            cliente.close()
        except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
            print("Tiempo excedido")
        except pymongo.errors.ConnectionFailure as errorConexion:
            print("La conexión ha fallado")

    def volver():
        ventana.destroy()
        on_return()


    btnInsertar = customtkinter.CTkButton(marco2, text="Insertar", command=insertarDatos)
    btnInsertar.grid(column=1, row=1, padx=10, pady=10)
    btnvolver = customtkinter.CTkButton(marco2, text="Volver", command=volver)
    btnvolver.grid(column=1, row=4, padx=10, pady=10)




    mostrarDatos(tvCosechas)

    ventana.mainloop()