from tkinter import *
from tkinter import ttk
import customtkinter
import pymongo
from conexionMongodb import *


def mostrarEmbarque(on_return):
    ventana = Toplevel()
    ventana.title("PLATANEX")
    ventana.geometry("1366x768")
    imagen= PhotoImage(file="Usuario.png")
    Label(ventana, image=imagen, bd=0).pack()


    db = cliente
    cantidad = DoubleVar()
    precio = IntVar()
    calidad = StringVar()

    marco = LabelFrame(ventana, text="Embarque", font=("Roboto", 24))
    marco.place(x=200,y=150, width=1020, height=110)
    #marco.configure(background=color_rgb)

    #labels y entrys

    #Cantidad
    lblCantidad = customtkinter.CTkLabel(marco, text="CANTIDAD").grid(column=0, row=0, padx=5, pady=5)
    txtCantidad = customtkinter.CTkEntry(marco, textvariable=cantidad)
    txtCantidad.grid(column=1, row=0)

    #cantidad
    lblcalidad = Label(marco, text="CALIDAD").grid(column=0, row=1, padx=5, pady=5)
    txtcalidad = customtkinter.CTkEntry(marco, textvariable=calidad)
    txtcalidad.grid(column=1, row=1)

    #precio
    lblprecio = Label(marco, text="PRECIO").grid(column=2, row=0, padx=5, pady=5)
    txtprecio = customtkinter.CTkEntry(marco, textvariable=precio)
    txtprecio.grid(column=3, row=0)

    #Cedula
    lblcedula = customtkinter.CTkLabel(marco, text="CEDULA").grid(column=2, row=1, padx=5, pady=5)
    comboCedula = ttk.Combobox(marco, state="readonly")
    comboCedula.grid(column=3, row=1)



    #Tabla lista cosechas
    marco1 = LabelFrame(ventana)
    marco1.place(x=200,y=270, width=600, height=250)

        

    tvEmbarque = ttk.Treeview(marco1, selectmode=NONE)
    tvEmbarque.grid(column=1, row=0 )
    tvEmbarque["columns"] = ("idEmbarque", "Cantidad","Precio","Calidad", "Cedula")
    tvEmbarque.column("#0", width=0, stretch=NO)
    tvEmbarque.column("idEmbarque", width=100, anchor=CENTER)
    tvEmbarque.column("Cantidad", width=100, anchor=CENTER)
    tvEmbarque.column("Precio", width=100, anchor=CENTER)
    tvEmbarque.column("Calidad", width=100, anchor=CENTER)
    tvEmbarque.column("Cedula", width=100, anchor=CENTER)
    tvEmbarque.heading("#0", text="")
    tvEmbarque.heading("idEmbarque", text="idEmbarque", anchor=CENTER)
    tvEmbarque.heading("Cantidad", text="Cantidad", anchor=CENTER)
    tvEmbarque.heading("Precio", text="Precio", anchor=CENTER)
    tvEmbarque.heading("Calidad", text="Calidad", anchor=CENTER)
    tvEmbarque.heading("Cedula", text="Cedula", anchor=CENTER)
    tvEmbarque.config(selectmode=BROWSE)


    #Botones y Acciones

    marco2 =  LabelFrame(ventana)
    marco2.place(x=718,y=270, width=500, height=250)

    lblmensajes = Label(marco2, text="", fg="green")
    lblmensajes.grid(column=0, row=4, columnspan=6)



    def mostrarDatos(tvEmbarque):

        try:
            cliente = pymongo.MongoClient(url, serverSelectionTimeoutMS = tiempoFuera)
            baseDatos = cliente[mongoBaseDatos]
            coleccion = baseDatos[mongoColeccion1]
            for documento in coleccion.find():
                id = documento["idEmbarque"]
                cantidad = documento["cantidad"]
                precio = documento["precio"]
                calidad = documento["calidad"]
                cedula = documento["cedula"]

                tvEmbarque.insert('', 'end', text = id, values=(id, cantidad, precio, calidad, cedula))

                print(documento)
            
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
        calidad.set("")  # Limpiar campo de calidad
        cantidad.set("")  # Limpiar campo de cantidad
        precio.set("")  # Limpiar campo de ubicación
        comboCedula.set("")  # Limpiar ComboBox de cédula

    def eliminarFila():
        item_seleccionado = tvEmbarque.selection()
        if item_seleccionado:
            id = tvEmbarque.item(item_seleccionado)['text']

            try:
                cliente = pymongo.MongoClient(url, serverSelectionTimeoutMS=tiempoFuera)
                baseDatos = cliente[mongoBaseDatos]
                coleccion = baseDatos[mongoColeccion1]

                # Eliminar el documento de la colección
                coleccion.delete_one({"idEmbarque": int(id)})

                # Eliminar la fila de la interfaz
                tvEmbarque.delete(item_seleccionado)

                lblmensajes.config(text="Fila eliminada", fg="green")

                cliente.close()
            except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
                print("Tiempo excedido")
            except pymongo.errors.ConnectionFailure as errorConexion:
                print("La conexión ha fallado")
        else:
            lblmensajes.config(text="Selecciona una fila para eliminar", fg="red")


    def seleccionarFila(event):
        item_seleccionado = tvEmbarque.selection()
        if item_seleccionado:
            id = tvEmbarque.item(item_seleccionado)['text']
            valores = tvEmbarque.item(item_seleccionado)['values']
            
            cantidad.set(valores[1])
            calidad.set(valores[3])
            precio.set(valores[2])
        else:
            lblmensajes.config(text="Selecciona una fila", fg="red")

    tvEmbarque.bind("<<TreeviewSelect>>", seleccionarFila)

    def actualizarDatos():
        # Obtener el ID del elemento seleccionado en la combobox
        nuevo_id = int(comboCedula.get())
        
        # Obtener el ID del elemento seleccionado en la tabla
        item_seleccionado = tvEmbarque.selection()
        if item_seleccionado:
            id = tvEmbarque.item(item_seleccionado)['text']
            
            # Obtener los nuevos valores de los campos
            nueva_cantidad = cantidad.get()
            nuevo_calidad = calidad.get()
            nueva_precio = precio.get()
            
            try:
                cliente = pymongo.MongoClient(url, serverSelectionTimeoutMS=tiempoFuera)
                baseDatos = cliente[mongoBaseDatos]
                coleccion = baseDatos[mongoColeccion1]
                
                # Obtener el valor actual de la columna "idEmbarque"
                valor_idEmbarque = tvEmbarque.item(item_seleccionado)['values'][0]
                
                # Actualizar los campos en el documento de la colección
                coleccion.update_one(
                    {"idEmbarque": valor_idEmbarque},
                    {"$set": {
                        "cantidadCinta": nueva_cantidad,
                        "cantidadCinta": nuevo_calidad,
                        "precio": nueva_precio,
                        "cedula": nuevo_id
                    }}
                )
                
                # Actualizar los valores en la interfaz
                tvEmbarque.item(item_seleccionado, values=(valor_idEmbarque, nueva_cantidad, nueva_precio, nuevo_calidad, nuevo_id))
                
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
        nuevo_calidad = calidad.get()
        nueva_precio = precio.get()
        nuevo_id = int(comboCedula.get())

        try:
            cliente = pymongo.MongoClient(url, serverSelectionTimeoutMS=tiempoFuera)
            baseDatos = cliente[mongoBaseDatos]
            coleccion = baseDatos[mongoColeccion1]

            # Obtener el valor máximo actual de la columna "idEmbarque" en la base de datos
            valor_max_idEmbarque = coleccion.find_one(sort=[("idEmbarque", -1)])["idEmbarque"]

            # Generar el nuevo valor de la columna "idEmbarque"
            nuevo_valor_idEmbarque = valor_max_idEmbarque + 1

            # Insertar los nuevos datos en la colección
            coleccion.insert_one({
                "idEmbarque": nuevo_valor_idEmbarque,
                "cantidadCinta": nueva_cantidad,
                "calidadCinta": nuevo_calidad,
                "precio": nueva_precio,
                "cedula": nuevo_id
            })

            # Insertar la nueva fila en la interfaz
            tvEmbarque.insert('', 'end', text=nuevo_valor_idEmbarque,
                            values=(nuevo_valor_idEmbarque, nueva_cantidad, nueva_precio, nuevo_calidad, nuevo_id))

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


    mostrarDatos(tvEmbarque)

    ventana.mainloop()
