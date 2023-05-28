import customtkinter
from tkinter import *
from tkinter import ttk
from conexionDB import *

def mostrarFinanzas(on_return):

    ventana = Toplevel()
    ventana.title("PLATANEX")
    ventana.geometry("1366x768")
    imagen= PhotoImage(file="backgroundAdmin.png")
    Label(ventana, image=imagen, bd=0).pack()

    db = DataBase()
    cedula = StringVar()
    nombre = StringVar()
    apellido = StringVar()
    horas = IntVar()
    pago = DoubleVar()
    idtrabajo = IntVar()

    marco1 =  LabelFrame(ventana)
    marco1.place(x=350,y=270, width=615, height=300)

    #Tabla lista trabajo

    tvTrabajo = ttk.Treeview(marco1)
    tvTrabajo.grid(column=1, row=0, padx=5 )
    tvTrabajo["columns"] = ("Cedula","Nombre","Apellido", "Horas", "Pago", "IdTrabajo")
    tvTrabajo.column("#0", width=0, stretch=NO)
    tvTrabajo.column("Cedula", width=100, anchor=CENTER)
    tvTrabajo.column("Nombre", width=100, anchor=CENTER)
    tvTrabajo.column("Apellido", width=100, anchor=CENTER)
    tvTrabajo.column("Horas", width=100, anchor=CENTER)
    tvTrabajo.column("Pago", width=100, anchor=CENTER)
    tvTrabajo.column("IdTrabajo", width=100, anchor=CENTER)

    tvTrabajo.heading("#0", text="")
    tvTrabajo.heading("Cedula", text="Cedula", anchor=CENTER)
    tvTrabajo.heading("Nombre", text="Nombre", anchor=CENTER)
    tvTrabajo.heading("Apellido", text="Apellido", anchor=CENTER)
    tvTrabajo.heading("Horas", text="Horas", anchor=CENTER)
    tvTrabajo.heading("Pago", text="Pago", anchor=CENTER)
    tvTrabajo.heading("IdTrabajo", text="IdTrabajo", anchor=CENTER)

    btnvolver = customtkinter.CTkButton(marco1, text="volver", command=lambda:volver())
    btnvolver.grid(column=1, row=1, padx=10, pady=10,  )

        #Funciones

    #Volver
    def volver():
        ventana.destroy()
        on_return()

        #Limpiar
    def limpiar():
        cedula.set("")
        nombre.set("")
        apellido.set("")
        horas.set("")
        pago.set("")
        idtrabajo.set("")

        #Vaciar Tabla trabajo
    def vaciar_tablatrabajo():
        filas = tvTrabajo.get_children()
        for fila in filas:
            tvTrabajo.delete(fila)



        #Llenar Tabla trabajo
    def llenar_tablatrabajo():
        vaciar_tablatrabajo()
        sql = "SELECT trabajador.cedula, trabajador.nombreTrabajador, trabajador.apellido, trabajo.horas, pagos.pago, trabajo.idtrabajo FROM trabajador JOIN trabajo ON trabajo.trabajador_cedula = trabajador.cedula JOIN pagos ON pagos.trabajo_idtrabajo = trabajo.idtrabajo;"
        db.cursor.execute(sql)
        filas = db.cursor.fetchall()
        for fila in filas:
            cedula = fila[0]
            nombre = fila[1]
            apellido = fila[2]
            horas = fila[3]
            pago = fila[4]
            id_trabajo = fila[5]
            tvTrabajo.insert("", END, id_trabajo, text=id_trabajo, values=(cedula, nombre, apellido, horas, pago, id_trabajo))
            

    llenar_tablatrabajo()


    ventana.mainloop()
