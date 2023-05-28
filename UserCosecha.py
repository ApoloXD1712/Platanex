from tkinter import *
from tkinter import ttk
from conexionDB import *
import customtkinter

def mostrarCosecha(on_return):

    ventana = Toplevel()
    ventana.title("PLATANEX")
    ventana.geometry("1366x768")
    imagen= PhotoImage(file="Usuario.png")
    Label(ventana, image=imagen, bd=0).pack()

    
    #Variables
    db = DataBase()
    modificar = False
    cantidad = DoubleVar()
    color = StringVar()
    ubicacion = IntVar()

    marco = LabelFrame(ventana, text="Cosecha")
    marco.place(x=200,y=150, width=1020, height=100)
    #marco.configure(background=color_rgb)

    #labels y entrys

    #Cantidad
    lblCantidad = Label(marco, text="CANTIDAD").grid(column=0, row=0, padx=5, pady=5)
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

    #Pago
    lblpago = Label(marco, text="PAGO").grid(column=2, row=1, padx=5, pady=5)



    #Tabla lista cosechas
    marco1 =  LabelFrame(ventana)
    marco1.place(x=200,y=270, width=520, height=250)


    tvCosechas = ttk.Treeview(marco1, selectmode=NONE)
    tvCosechas.grid(column=1, row=0 )
    tvCosechas["columns"] = ("Semana","Color","Ubicacion","Cantidad","Trabajo")
    tvCosechas.column("#0", width=0, stretch=NO)
    tvCosechas.column("Semana", width=100, anchor=CENTER)
    tvCosechas.column("Color", width=100, anchor=CENTER)
    tvCosechas.column("Ubicacion", width=100, anchor=CENTER)
    tvCosechas.column("Cantidad", width=100, anchor=CENTER)
    tvCosechas.heading("#0", text="")
    tvCosechas.heading("Semana", text="Semana", anchor=CENTER)
    tvCosechas.heading("Color", text="Color", anchor=CENTER)
    tvCosechas.heading("Ubicacion", text="Ubicacion", anchor=CENTER)
    tvCosechas.heading("Cantidad", text="Cantidad", anchor=CENTER)
    tvCosechas.config(selectmode=BROWSE)


    #Botones y Acciones

    marco2 =  LabelFrame(ventana)
    marco2.place(x=718,y=270, width=500, height=250)

    lblmensajes = Label(marco2, text="", fg="green")
    lblmensajes.grid(column=0, row=4, columnspan=6)

    btnInsertar = customtkinter.CTkButton(marco2, text="Insertar", command=lambda:insertar())
    btnInsertar.grid(column=1, row=1, padx=10, pady=10)
    
    btnEliminar = customtkinter.CTkButton(marco2, text="volver", command=lambda:volver())
    btnEliminar.grid(column=1, row=4, padx=10, pady=10,  )

    #Funciones

    #Volver
    def volver():
        ventana.destroy()
        on_return()

    #Seleccionar
    def seleccionar(event):
        id = tvCosechas.selection()[0]

        if int(id)>0:
            cantidad.set(tvCosechas.item(id, "values")[3])
            color.set(tvCosechas.item(id, "values")[1])
            ubicacion.set(tvCosechas.item(id, "values")[2])

    tvCosechas.bind("<<TreeviewSelect>>", seleccionar)


    

    #Limpiar
    def limpiar():
        cantidad.set("")
        color.set("")
        ubicacion.set("")

    #Vaciar Tabla
    def vaciar_tabla():
        filas = tvCosechas.get_children()
        for fila in filas:
            tvCosechas.delete(fila)

    #Llenar Tabla
    def llenar_tabla():
        vaciar_tabla()
        sql = "select semana, colorCinta, ubicacion, cantidadCinta from cosecha"
        db.cursor.execute(sql)
        filas = db.cursor.fetchall()
        for fila in filas:
            id = fila[0]
            tvCosechas.insert("", END, id, text=id, values= fila)


    #Eliminar Datos
    def eliminar():
        id = tvCosechas.selection()[0]
        if int(id) > 0:
            sql = "delete from cosecha where semana="+id
            db.cursor.execute(sql)
            db.connection.commit()
            tvCosechas.delete(id)
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
      

            val = (color.get(),ubicacion.get(),cantidad.get(),comboColumna.get() )
            sql = "insert into cosecha (colorCinta, ubicacion, cantidadCinta, pagos_idpago) values(%s, %s, %s, %s)"
            db.cursor.execute(sql, val)
            db.connection.commit()
            lblmensajes.config(text="se ha guardado un registro correctamente")
            llenar_tabla()
            limpiar()
       


    #Actualizar Datos
    def actualizar():
      
            id = tvCosechas.selection()[0]
            val = (color.get(),ubicacion.get(),cantidad.get(),comboColumna.get())
            sql = "update cosecha set colorCinta=%s, ubicacion=%s, cantidadCinta=%s, pagos_idpago=%s where semana="+id
            db.cursor.execute(sql, val)
            db.connection.commit()
            lblmensajes.config(text="se ha actualizado el registro correctamente")
            llenar_tabla()
            limpiar()
        

        

    llenar_tabla()
    ventana.mainloop()

