import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import os
from datetime import date, datetime
import re

def get_all_prestamos():
    prestamos = []
    try:
        if not os.path.exists("prestamos.txt"):
            return []
        with open("prestamos.txt", "r") as file:
            for line in file:
                data = line.strip().split("\t")
                prestamos.append(data)
        return prestamos
    except Exception as e:
        print("Error al leer el archivo ", e)

def get_lista_for_listbox( tipo ):
    libros_prestados = []
    try:
        if os.path.exists("prestamos.txt"):
            with open("prestamos.txt", "r") as file:
                for line in file:
                    data = line.strip().split("\t")
                    libros_prestados.append(data[0])
    except Exception as e:
        print("Error al leer el archivo ", e)

    try:
        result = []
        if not os.path.exists( f"{tipo}.txt"):
            return result
        with open( f"{tipo}.txt", "r" ) as file:
            for line in file:
                data = line.strip().split("\t")
                if data[1] not in libros_prestados:
                    result.append( data[1] )
        return result  
    except Exception as e:
        print("Error al leer el archivo ", e)

def window_agregar_prestamo( actualizar_prestamos ):
    def Guardar_prestamo():
        libro = opc_isbn.get()
        usuario = opc_usuarios.get()
        fecha_prestamo = date.today().strftime('%d/%m/%Y')
        fecha_devolucion = cal.get_date().strftime('%d/%m/%Y')
        if libro == "" or usuario == "":
            messagebox.showerror("Error", "Por favor Seleccione un libro y un usuario")
            return
        try:
            with open("prestamos.txt", "a") as file:
                file.write(f"{libro}\t{usuario}\t{fecha_prestamo}\t{fecha_devolucion}\n")
            messagebox.showinfo("Exito", "Prestamo agregado con exito")
            principal_window.destroy()
            actualizar_prestamos()
        except Exception as e:
            print("Error al guardar el prestamo", e)
            messagebox.showerror("Error", "No se pudo guardar el prestamo ")

    principal_window = tk.Toplevel( background='#e8cb9a')
    principal_window.title("Agregar Prestamo")
    principal_window.geometry("380x200")

    lbl_margin = tk.Label( principal_window, text="" , background='#e8cb9a' )
    lbl_margin.pack()

    frame1 = tk.Frame( principal_window,  background='#e8cb9a' )
    frame1.pack( anchor=tk.W, padx=25, fill=tk.X )
    lbl_isbn1 = tk.Label( frame1, text="Libro: ",background='#e8cb9a'  )   
    lbl_isbn1.pack(side=tk.LEFT, padx=(0, 13))
    lista_isbn = get_lista_for_listbox( "libros" )
    opc_isbn = tk.StringVar( frame1 )
    if len(lista_isbn) == 0:
        lista_isbn.append("No hay libros")
    checklist_isbn = tk.OptionMenu( frame1, opc_isbn, *lista_isbn )
    checklist_isbn.pack(side=tk.LEFT, fill=tk.X, expand=True)

    frame2 = tk.Frame( principal_window,  background='#e8cb9a' )
    frame2.pack( anchor=tk.W, padx=25, fill=tk.X, pady=6 )
    lbl_usuario = tk.Label( frame2, text="Usuario: ", background='#e8cb9a'  )   
    lbl_usuario.pack(side=tk.LEFT)
    lista_usuarios = get_lista_for_listbox( "usuarios" )
    opc_usuarios = tk.StringVar( frame2 )
    if len(lista_usuarios) == 0:
        lista_usuarios.append("No hay usuarios")
    checklist_usuarios = tk.OptionMenu( frame2, opc_usuarios, *lista_usuarios )
    checklist_usuarios.pack(side=tk.LEFT, fill=tk.X, expand=True)

    frame3 = tk.Frame( principal_window,  background='#e8cb9a' )
    frame3.pack( anchor=tk.W, padx=25, fill=tk.X, pady=6 )
    lbl_fecha = tk.Label( frame3, text="Fecha de entrega: " , background='#e8cb9a' )
    lbl_fecha.pack(side=tk.LEFT)
    cal = DateEntry( frame3, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/MM/yyyy', mindate=date.today() )
    cal.pack(side=tk.LEFT, fill=tk.X, expand=True)

    btn_agregar = tk.Button( principal_window, text="Agregar", command=Guardar_prestamo )
    btn_agregar.pack(side=tk.LEFT, padx=25, expand=False)
    btn_cancelar = tk.Button( principal_window, text="Cancelar", command=principal_window.destroy )
    btn_cancelar.pack( side=tk.RIGHT, padx=25 )

def window_editar_prestamo( actualizar_tabla, pos_libro, pos_usuario, fecha_devolucion ):
    def actualizar_prestamo():
        libro = opc_isbn.get()
        usuario = opc_usuarios.get()
        fecha_devolucion = cal.get_date().strftime('%d/%m/%Y')
        if libro == "" or usuario == "":
            messagebox.showerror("Error", "Por favor Seleccione un libro y un usuario")
            return
        try:
            prestamos = get_all_prestamos()
            with open("prestamos.txt", "w") as file:
                for prestamo in prestamos:
                    if prestamo[0] == libro:
                        file.write(f"{libro}\t{usuario}\t{prestamo[2]}\t{fecha_devolucion}\n")
                    else:
                        file.write("\t".join(prestamo) + "\n")
            messagebox.showinfo("Exito", "Prestamo actualizado con exito")
            principal_window.destroy()
            actualizar_tabla()
        except Exception as e:
            print("Error al guardar el prestamo", e)
            messagebox.showerror("Error", "No se pudo guardar el prestamo ")

    principal_window = tk.Toplevel(background='#e8cb9a')
    principal_window.title("Editar Prestamo")
    principal_window.geometry("380x200")

    lbl_margin = tk.Label( principal_window, text="" , background='#e8cb9a' )
    lbl_margin.pack()

    frame1 = tk.Frame( principal_window, background='#e8cb9a'  )
    frame1.pack( anchor=tk.W, padx=25, fill=tk.X )
    lbl_isbn1 = tk.Label( frame1, text="Libro: ", background='#e8cb9a'  )   
    lbl_isbn1.pack(side=tk.LEFT, padx=(0, 13))
    lista_isbn = get_lista_for_listbox( "libros" )
    opc_isbn = tk.StringVar( frame1 )
    for i, titulo_libro in enumerate(get_all_prestamos(),start=0):
        if titulo_libro[0] == pos_libro:
            opc_isbn.set(get_all_prestamos()[i][0])
            break
    if len(lista_isbn) == 0:
        lista_isbn.append("No hay libros")
    checklist_isbn = tk.OptionMenu( frame1, opc_isbn, *lista_isbn )
    checklist_isbn.pack(side=tk.LEFT, fill=tk.X, expand=True)

    frame2 = tk.Frame( principal_window, background='#e8cb9a'  )
    frame2.pack( anchor=tk.W, padx=25, fill=tk.X, pady=6 )
    lbl_usuario = tk.Label( frame2, text="Usuario: ", background='#e8cb9a'   )   
    lbl_usuario.pack(side=tk.LEFT)
    lista_usuarios = get_lista_for_listbox( "usuarios" )
    opc_usuarios = tk.StringVar( frame2 )
    if len(lista_usuarios) == 0:
        lista_usuarios.append("No hay usuarios")
##REVISA ESTO ESTA MALO-------------------------------------------------------
    for i, nombre_usuario in enumerate(get_all_prestamos(),start=0):
        if nombre_usuario[1] == pos_usuario:
            opc_usuarios.set(get_all_prestamos()[i][1])
            break
##---------------------------------------------------------------------------
    checklist_usuarios = tk.OptionMenu( frame2, opc_usuarios, *lista_usuarios )
    checklist_usuarios.pack(side=tk.LEFT, fill=tk.X, expand=True)

    frame3 = tk.Frame( principal_window, background='#e8cb9a'  )
    frame3.pack( anchor=tk.W, padx=25, fill=tk.X, pady=6 )
    lbl_fecha = tk.Label( frame3, text="Fecha de entrega: ", background='#e8cb9a'  )
    lbl_fecha.pack(side=tk.LEFT)
    cal = DateEntry( frame3, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/MM/yyyy', mindate=date.today() )
    cal.pack(side=tk.LEFT, fill=tk.X, expand=True)
    cal.set_date(fecha_devolucion)

    btn_agregar = tk.Button( principal_window, text="Editar Prestamos", command=actualizar_prestamo )
    btn_agregar.pack(side=tk.LEFT, padx=25, expand=False)
    btn_cancelar = tk.Button( principal_window, text="Cancelar", command=principal_window.destroy )
    btn_cancelar.pack( side=tk.RIGHT, padx=25 )

def frame_pretamos( root:tk.Tk ):
    def buscar_prestamos(variable):
        print( variable.get() )
        if variable.get() == "":
            load_prestamos()
            return
        else:
            tree_prestamos.tag_configure( 'diaEntrega', background='#E89351' )
            tree_prestamos.tag_configure( 'fechaVencida' , background='#E86051' )
            tree_prestamos.delete(*tree_prestamos.get_children())
            prestamos = get_all_prestamos()
            for prestamo in prestamos:
                if re.search(variable.get(), prestamo[0], re.IGNORECASE):
                    entrega = datetime.strptime(prestamo[3] , "%d/%m/%Y")
                    hoy = datetime.strptime( date.today().strftime('%d/%m/%Y') , "%d/%m/%Y" )
                    if ( hoy == entrega ):
                        tree_prestamos.insert("", tk.END, values=prestamo, tags=("diaEntrega",))
                    elif ( entrega < hoy ):
                        tree_prestamos.insert("", tk.END, values=prestamo, tags=("fechaVencida",))
                    else:
                        tree_prestamos.insert("", tk.END, values=prestamo)
                    #tree_prestamos.insert("", tk.END, values=prestamo)

    def devolver_prestamos():
        try:
            seleccion = tree_prestamos.selection()
            if len(seleccion) == 0:
                messagebox.showerror("Error", "Por favor seleccione un prestamo")
                return
            for i in seleccion:
                item = tree_prestamos.item(i)
                libro = item['values'][0]
                tree_prestamos.delete(i)
                prestamos = get_all_prestamos()
                with open("prestamos.txt", "w") as file:
                    for prestamo in prestamos:
                        if prestamo[0] != libro:
                            file.write("\t".join(prestamo) + "\n")
        except Exception as e:
            messagebox.showerror("Error", "No se pudo devolver el prestamo")

    def load_prestamos():
        try:
            if not os.path.exists("prestamos.txt"):
                return
            tree_prestamos.delete(*tree_prestamos.get_children())
            tree_prestamos.tag_configure( 'diaEntrega', background='#E89351' )
            tree_prestamos.tag_configure( 'fechaVencida' , background='#E86051' )
            with open("prestamos.txt", "r") as file:
                for line in file:
                    data = line.strip().split("\t")
                    entrega = datetime.strptime(data[3] , "%d/%m/%Y")
                    hoy = datetime.strptime( date.today().strftime('%d/%m/%Y') , "%d/%m/%Y" )
                    #hoy = datetime.strptime( "13/03/2025" , "%d/%m/%Y" )
                    if ( hoy == entrega ):
                        tree_prestamos.insert("", tk.END, values=data, tags=("diaEntrega",))
                    elif ( entrega < hoy ):
                        tree_prestamos.insert("", tk.END, values=data, tags=("fechaVencida",))
                    else:
                        tree_prestamos.insert("", tk.END, values=data)

        except Exception as e:
            print("Error al cargar los prestamos", e)
            messagebox.showerror("Error", "No se pudo cargar los prestamos")

    def seleccionar_y_editar_prestamos():
        tree_prestamos.selection()
        seleccion = tree_prestamos.selection()
        if len(seleccion) == 0:
            messagebox.showerror("Error", "Por favor seleccione un prestamo")
            return
        item = tree_prestamos.item(seleccion)
        libro = item['values'][0]
        usuario = item['values'][1]
        fecha_devolucion = item['values'][3]
        window_editar_prestamo( load_prestamos, libro, usuario, fecha_devolucion )

    frame_prestamos = tk.Frame(root, background='#e8cb9a')
    frame_prestamos.place( x=0, y=98, width=1150, height=452 )

    lbl_titulo_prestamos = tk.Label( frame_prestamos,text="Gestion de Prestamo", font=('italic', 20), background='#e8cb9a')
    lbl_titulo_prestamos.pack( side=tk.TOP, pady=5 )

    frame_buscar_prestamos = tk.Frame( frame_prestamos, background='#e8cb9a' )
    frame_buscar_prestamos.pack(side=tk.TOP,pady=15)
    lbl_buscar_prestamos = tk.Label( frame_buscar_prestamos, text="Buscar prestamo: ", background='#e8cb9a')
    lbl_buscar_prestamos.pack( side=tk.LEFT, padx=5 )
    ##METODO LISENING PARA BUSCAR
    string_listener = tk.StringVar()
    string_listener.trace("w", lambda neme, index, mode, string_listener=string_listener: buscar_prestamos(string_listener))
    input_buscar_prestamos = tk.Entry( frame_buscar_prestamos, textvariable=string_listener )
    input_buscar_prestamos.pack( side=tk.LEFT, padx=5 )

    columnas_prestamos = ('libro', 'usuario', 'fecha_prestamo', 'fecha_devolucion')
    frame_tabla_prestamos = tk.Frame(frame_prestamos )
    frame_tabla_prestamos.pack(side=tk.TOP, fill=tk.X , padx=4)
    tree_prestamos = ttk.Treeview(frame_tabla_prestamos, columns=columnas_prestamos, show='headings')
    tree_prestamos.heading( 'libro', text='Libro' )
    tree_prestamos.heading( 'usuario', text='Usuario' )
    tree_prestamos.heading( 'fecha_prestamo', text='Fecha del Prestamo' )
    tree_prestamos.heading( 'fecha_devolucion', text='Fecha de Devolucion')
    tree_prestamos.pack(side=tk.LEFT, fill=tk.X, expand=True)
    scrollbar_prestamos = ttk.Scrollbar( frame_tabla_prestamos, orient='vertical', command=tree_prestamos.yview )
    tree_prestamos.config(yscrollcommand=scrollbar_prestamos.set)
    scrollbar_prestamos.pack(side=tk.LEFT)

    icon_prestamo = tk.PhotoImage( file="img/prestamo.png").subsample(25)
    icon_devolucion = tk.PhotoImage( file="img/devolver.png").subsample(25)
    icon_editar = tk.PhotoImage( file="img/editarPrestamo.png").subsample(3)

    frame_gestion_prestamos = tk.Frame(frame_prestamos,background='#e8cb9a')
    frame_gestion_prestamos.pack( side=tk.TOP, pady= 15 )
    btn_ingresar_prestamos = tk.Button( frame_gestion_prestamos, text="Prestar Libro", font=( 'Verdana', 10 ) ,image=icon_prestamo, compound=tk.LEFT , bg="#22fa04" , bd=1 ,command=lambda: window_agregar_prestamo( load_prestamos ))
    btn_ingresar_prestamos.image = icon_prestamo
    btn_ingresar_prestamos.pack(side=tk.LEFT, padx=10, ipadx=5, ipady=5)

    btn_editar_prestamos = tk.Button( frame_gestion_prestamos, text="Editar Prestamo", font=('Verdana',10), image=icon_editar, compound=tk.LEFT, bg="#ebfa04", bd=1 ,command=seleccionar_y_editar_prestamos )
    btn_editar_prestamos.image = icon_editar
    btn_editar_prestamos.pack(side=tk.LEFT, padx=10, ipadx=5, ipady=5)

    btn_eliminar_prestamos = tk.Button( frame_gestion_prestamos, text="Devolucion de Libro",font=('Verdana',10), image=icon_devolucion, compound=tk.LEFT, bd=1 ,bg="#51B6E8" , command=devolver_prestamos )
    btn_eliminar_prestamos.image = icon_devolucion
    btn_eliminar_prestamos.pack(side=tk.LEFT,padx=10, ipadx=5, ipady=5)

    load_prestamos()
    return frame_prestamos
