import customtkinter
from tkinter import *
from tkinter import ttk
from conexionDB import *

def mostrarCaja(on_return):

    ventana = Toplevel()
    ventana.title("PLATANEX")
    ventana.geometry("1366x768")
    imagen= PhotoImage(file="backgroundAdmin.png")
    Label(ventana, image=imagen, bd=0).pack()

    db = DataBase()
    modificar = False
    IdEmbarque = StringVar()
    Cantidad = StringVar()
    Idcalidad = StringVar()
    Precio = StringVar()

    marco =  LabelFrame(ventana, text="Embarque")
    marco.place(x=200,y=150, width=1020, height=100)

    #labels y entrys


    #Cantidad
    lblCantidad = Label(marco, text="Cantidad").grid(column=0, row=0, padx=5, pady=5)
    txtCantidad = customtkinter.CTkEntry(marco, textvariable=Cantidad)
    txtCantidad.grid(column=1, row=0)

    #uIdcalidad
    lblCalidad= Label(marco, text="ID Calidad").grid(column=2, row=0, padx=5, pady=5)
    txtCalidad = customtkinter.CTkEntry(marco, textvariable=Idcalidad)
    txtCalidad.grid(column=3, row=0)

    #precio
    lblPrecio = Label(marco, text="Precio").grid(column=0, row=1, padx=5, pady=5)
    txtPrecio = customtkinter.CTkEntry(marco, textvariable=Precio)
    txtPrecio.grid(column=1, row=1)

    #Pago
    lblpago = customtkinter.CTkLabel(marco, text="Pago").grid(column=2, row=1, padx=5, pady=5)

    marco1 =  LabelFrame(ventana)
    marco1.place(x=200,y=270, width=520, height=250)


    #Tabla lista caja

    tvCajas = ttk.Treeview(marco1)
    tvCajas.grid(column=1, row=0, padx=5 )
    tvCajas["columns"] = ("idEmbarque","cantidad","precio","calidad_idcalidad")
    tvCajas.column("#0", width=0, stretch=NO)
    tvCajas.column("idEmbarque", width=100, anchor=CENTER)
    tvCajas.column("cantidad", width=100, anchor=CENTER)
    tvCajas.column("precio", width=100, anchor=CENTER)
    tvCajas.column("calidad_idcalidad", width=100, anchor=CENTER)

    tvCajas.heading("#0", text="")
    tvCajas.heading("idEmbarque", text="IdEmbarque", anchor=CENTER)
    tvCajas.heading("cantidad", text="Cantidad", anchor=CENTER)
    tvCajas.heading("precio", text="Precio", anchor=CENTER)
    tvCajas.heading("calidad_idcalidad", text="IdCalidad", anchor=CENTER)
    tvCajas.config(selectmode=BROWSE)

    #Botones y Acciones

    marco2 =  LabelFrame(ventana)
    marco2.place(x=718,y=270, width=500, height=250)

    lblmensajes = Label(marco2, text="", fg="green")
    lblmensajes.grid(column=0, row=4, columnspan=6)

    btnInsertar = customtkinter.CTkButton(marco2, text="Insertar", command=lambda:insertar())
    btnInsertar.grid(column=1, row=1, padx=10, pady=10)
    btnActualizar = customtkinter.CTkButton(marco2, text="Actualizar", command=lambda:actualizar())
    btnActualizar.grid(column=1, row=2, padx=10, pady=10)
    btnEliminar = customtkinter.CTkButton(marco2, text="Eliminar", command=lambda:eliminar())
    btnEliminar.grid(column=1, row=3, padx=10, pady=10)
    btnvolver = customtkinter.CTkButton(marco2, text="volver", command=lambda:volver())
    btnvolver.grid(column=1, row=4, padx=10, pady=10,  )

    #Funciones

    #Volver
    def volver():
        ventana.destroy()
        on_return()

    #Seleccionar
    def seleccionar(event):
        id = tvCajas.selection()[0]

        if int(id)>0:
            Cantidad.set(tvCajas.item(id, "values")[1])
            Precio.set(tvCajas.item(id, "values")[2])
            Idcalidad.set(tvCajas.item(id, "values")[3])

    tvCajas.bind("<<TreeviewSelect>>", seleccionar)


   

    #Validar
    def validar():
        return len(Cantidad.get()) and len(Precio.get()) and len(Idcalidad.get())


    #Limpiar
    def limpiar():
        Cantidad.set("")
        Precio.set("")
        Idcalidad.set("")

    #Vaciar Tabla
    def vaciar_tabla():
        filas = tvCajas.get_children()
        for fila in filas:
            tvCajas.delete(fila)


    #Llenar Tabla
    def llenar_tabla():
        vaciar_tabla()
        sql = "select idEmbarque, cantidad, precio, calidad_idcalidad from caja"
        db.cursor.execute(sql)
        filas = db.cursor.fetchall()
        for fila in filas:
            id = fila[0]
            tvCajas.insert("", END, id, text=id, values= fila)


    #Eliminar Datos
    def eliminar():
        id = tvCajas.selection()[0]
        if int(id) > 0:
            sql = "delete from caja where idEmbarque="+id
            db.cursor.execute(sql)
            db.connection.commit()
            tvCajas.delete(id)
            lblmensajes.config(text="El registro se ha eliminado correctamente")
        else:
            lblmensajes.config(text="Seleccione un registro")
        limpiar()

        

    #Obtener Llave Foranea
    def obtenerforanea():
        # Realiza una consulta a la base de datos para obtener los valores de la columna
        sql = "SELECT idpago FROM pagos" 
        db.cursor.execute(sql)
        resultados = db.cursor.fetchall()
        
        # Extrae los valores de los resultados de la consulta
        valores = [resultado[0] for resultado in resultados]
        
        return valores

    #Combobox Llave Foranea

    # Crea un ComboBox
    comboColumna = ttk.Combobox(marco, state="readonly")

    # Obtén los elementos de la columna desde la base de datos
    valores_columna = obtenerforanea()  

    # Asigna los elementos al ComboBox
    comboColumna["values"] = valores_columna

    # Configura el ComboBox para que no permita editar manualmente los valores
    comboColumna["state"] = "readonly"

    # Ubica el ComboBox en la interfaz
    comboColumna.grid(column=3, row=1)


    #Insertar Datos
    def insertar():

            val = (Cantidad.get(),Precio.get(),comboColumna.get(), Idcalidad.get())
            sql = "insert into caja (cantidad, precio, pagos_idpago, calidad_idcalidad) values(%s, %s, %s, %s)"
            db.cursor.execute(sql, val)
            db.connection.commit()
            lblmensajes.config(text="se hs guardado un registro correctamente")
            llenar_tabla()
            limpiar()
       

    def actualizar():
            id = tvCajas.selection()[0]
            val = (Cantidad.get(),Precio.get(),comboColumna.get(), Idcalidad.get())
            sql = "update caja set cantidad=%s, precio=%s, pagos_idpago=%s, calidad_idcalidad=%s where idEmbarque="+id
            db.cursor.execute(sql, val)
            db.connection.commit()
            lblmensajes.config(text="se ha actualizado el registro correctamente")
            llenar_tabla()
            limpiar()

    llenar_tabla() 

    ventana.mainloop()