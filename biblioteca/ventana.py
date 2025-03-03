import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

root = tk.Tk()
root.title("Biblioteca")
root.geometry("1150x550")

#Funcion para indicador del menu_________________________________________________________________________________
def ocultar_indicador_menu():
    lbl_indicador_libros.config(background='#93D973')
    lbl_indicador_usuarios.config(background="#93D973")
    lbl_indicador_prestamos.config(background='#93D973')

#Funcion para cambiar de frame o pagina___________________________________________________________________________
def cambiar_pagina( lbl_indicador, frame ):
    ocultar_indicador_menu()
    lbl_indicador.config(background='#F28F79')
    frame.tkraise()
    pass

#Titulo del encabezado_____________________________________________________________________________________________
encabezado  = tk.Frame(root, background='#43AED9')
encabezado.pack( side=tk.TOP, fill=tk.X )
lbl_encabezado = tk.Label( encabezado, text="La Biblioteca", font=('bolt', 20), background='#43AED9' )
lbl_encabezado.pack( side=tk.LEFT, pady=10, padx=10 )

#Menu de Botones____________________________________________________________________________________________________
menu_botones = tk.Frame( root, background='#93D973' )
menu_botones.pack( side=tk.TOP, fill=tk.X )
menu_botones.pack_propagate(False)
menu_botones.configure(height=40)

btn_libros = tk.Button( menu_botones, text='Libros' , bd=0 , background="#93D973", command=lambda: cambiar_pagina( lbl_indicador_libros, frame_libros ))
btn_libros.pack(side=tk.LEFT, padx=2, fill=tk.Y, ipadx=20)
lbl_indicador_libros = tk.Label( menu_botones, text="", background="#F28F79" )
lbl_indicador_libros.place( x=2, y=35, width=79, height=5 )

btn_usuarios  = tk.Button( menu_botones, text='Usuarios' , width=10, bd=0 , background='#93D973', command=lambda: cambiar_pagina( lbl_indicador_usuarios, frame_usuarios ) )
btn_usuarios.pack( side=tk.LEFT, padx=2, fill=tk.Y)
lbl_indicador_usuarios = tk.Label( menu_botones, text="", background="#93D973" )
lbl_indicador_usuarios.place( x=85, y=35, width=76, height=5 )

btn_prestmos = tk.Button( menu_botones, text="Prestamos" , width=10, bd=0 , background='#93D973', command=lambda: cambiar_pagina( lbl_indicador_prestamos, frame_prestamos) )
btn_prestmos.pack( side=tk.LEFT, padx=2, fill=tk.Y)
lbl_indicador_prestamos = tk.Label( menu_botones, text="", background="#93D973" )
lbl_indicador_prestamos.place( x=165, y=35, width=76, height=5 )

btn_utilidades = tk.Button( menu_botones, text="Utilidades", width=10, bd=0 , background='#93D973' )
btn_utilidades.pack( side=tk.LEFT, padx=2, fill=tk.Y )
lbl_indicador_utilidades = tk.Label( menu_botones, text="", background="#93D973" )
lbl_indicador_utilidades.place( x=249, y=35, width=72, height=5 )

#Panel para Gestionar libros___________________________________________________________________________________________
#Funcion para agregar un libro
def window_agregar_libro():
    def agregar_libro( event=None ):
        #FUNCION PARA AGREGAR EL LIBRO AL ARCHIVO TXT

        if input_isbn.get()=="" or input_titulo.get()=="" or input_autor.get()=="":
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        respuesta = messagebox.askyesno("Agregar Libro", "¿Desea agregar otro libro?")
        if respuesta:
            input_isbn.delete(0,tk.END)
            input_titulo.delete(0,tk.END)
            input_autor.delete(0,tk.END)
            input_isbn.focus_set()
        else:
            principal_window.destroy()

        pass

    principal_window = tk.Toplevel(root)
    principal_window.title("Agregar Libro")
    principal_window.geometry( "350x200" )

    lbl_margin = tk.Label( principal_window, text="" )
    lbl_margin.pack(pady=3)
    lbl_isbn = tk.Label( principal_window, text="Ingrese ISBN: " )
    lbl_isbn.pack(anchor=tk.W, padx=25)
    input_isbn = tk.Entry( principal_window )
    input_isbn.pack(anchor=tk.W, padx=25, fill=tk.X )
    lbl_titulo = tk.Label( principal_window, text="Ingrese Titulo: " )
    lbl_titulo.pack(anchor=tk.W, padx=25)
    input_titulo = tk.Entry( principal_window )
    input_titulo.pack(anchor=tk.W, padx=25, fill=tk.X)
    lbl_autor = tk.Label( principal_window, text="Ingrese Autor: " )
    lbl_autor.pack(anchor=tk.W, padx=25)
    input_autor = tk.Entry( principal_window )
    input_autor.pack(anchor=tk.W, padx=25, fill=tk.X)
    input_autor.bind('<Return>',agregar_libro)
    btn_agregar = tk.Button( principal_window, text="Agregar", command=agregar_libro )
    btn_agregar.pack(side=tk.LEFT, padx=25, expand=False)
    btn_cancelar = tk.Button( principal_window, text="Cancelar", command=principal_window.destroy )
    btn_cancelar.pack( side=tk.RIGHT, padx=25 )


frame_libros = tk.Frame( root )
frame_libros.place( x=0, y=98, width=1150, height=452 )

lbl_titulo_libros = tk.Label( frame_libros,text="Gestion de Libros", font=('italic', 20))
lbl_titulo_libros.pack( side=tk.TOP, pady=5 )

frame_buscar_libro = tk.Frame( frame_libros )
frame_buscar_libro.pack(side=tk.TOP,pady=15)
lbl_buscar_libro = tk.Label( frame_buscar_libro, text="Buscar Libro: ")
lbl_buscar_libro.pack( side=tk.LEFT, padx=5 )
input_buscar_libro = tk.Entry( frame_buscar_libro )
input_buscar_libro.pack( side=tk.LEFT, padx=5 )
btn_buscar_libro = tk.Button( frame_buscar_libro, text="Buscar" )
btn_buscar_libro.pack(side=tk.LEFT , padx=5)

columnas_libros = ('ISBN', 'Titulo', 'Autor')
frame_tabla_libros = tk.Frame(frame_libros )
frame_tabla_libros.pack(side=tk.TOP, fill=tk.X , padx=4)
tree_libros = ttk.Treeview(frame_tabla_libros, columns=columnas_libros, show='headings')
tree_libros.heading( 'ISBN', text='ISBN' )
tree_libros.heading( 'Titulo', text='Titulo' )
tree_libros.heading( 'Autor', text='Autor' )
tree_libros.pack(side=tk.LEFT, fill=tk.X, expand=True)
scrollbar_libros = ttk.Scrollbar( frame_tabla_libros, orient='vertical', command=tree_libros.yview )
tree_libros.config(yscrollcommand=scrollbar_libros.set)
scrollbar_libros.pack(side=tk.LEFT)

frame_gestion_libros = tk.Frame(frame_libros)
frame_gestion_libros.pack( side=tk.TOP, pady= 15 )
btn_ingresar_libro = tk.Button( frame_gestion_libros, text="Agregar Libro", command=window_agregar_libro)
btn_ingresar_libro.pack(side=tk.LEFT, padx=10)
btn_editar_libro = tk.Button( frame_gestion_libros, text="Editar Libro" )
btn_editar_libro.pack(side=tk.LEFT,padx=10)
btn_eliminar_libro = tk.Button( frame_gestion_libros, text="Eliminar Libro" )
btn_eliminar_libro.pack(side=tk.LEFT,padx=10)

#Panel para Gestionar usuario___________________________________________________________________________________________
#Funcion para agregar un usuario
def window_agregar_usuario():
    def agregar_usuario( event=None ):
        #FUNCION PARA AGREGAR EL Usuario AL ARCHIVO TXT

        if input_isbn.get()=="" or input_titulo.get()=="":
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        respuesta = messagebox.askyesno("Agregar Libro", "¿Desea agregar otro usuario?")
        if respuesta:
            input_isbn.delete(0,tk.END)
            input_titulo.delete(0,tk.END)
            input_isbn.focus_set()
        else:
            principal_window.destroy()

        pass
    principal_window = tk.Toplevel(root)
    principal_window.title("Agregar Usuario")
    principal_window.geometry( "350x150" )

    lbl_margin = tk.Label( principal_window, text="" )
    lbl_margin.pack(pady=1)
    lbl_isbn = tk.Label( principal_window, text="Ingrese Id: " )
    lbl_isbn.pack(anchor=tk.W, padx=25)
    input_isbn = tk.Entry( principal_window )
    input_isbn.pack(anchor=tk.W, padx=25, fill=tk.X )
    lbl_titulo = tk.Label( principal_window, text="Ingrese Nombre : " )
    lbl_titulo.pack(anchor=tk.W, padx=25)
    input_titulo = tk.Entry( principal_window )
    input_titulo.pack(anchor=tk.W, padx=25, fill=tk.X)
    input_titulo.bind('<Return>', agregar_usuario)
    btn_agregar = tk.Button( principal_window, text="Agregar" , command=agregar_usuario )
    btn_agregar.pack(side=tk.LEFT, padx=25, expand=False)
    btn_cancelar = tk.Button( principal_window, text="Cancelar", command=principal_window.destroy )
    btn_cancelar.pack( side=tk.RIGHT, padx=25 )

frame_usuarios = tk.Frame( root )
frame_usuarios.place( x=0, y=98, width=1150, height=452 )

lbl_titulo_usuarios = tk.Label( frame_usuarios,text="Gestion de Usuarios", font=('italic', 20))
lbl_titulo_usuarios.pack( side=tk.TOP, pady=5 )

frame_buscar_usuario = tk.Frame( frame_usuarios )
frame_buscar_usuario.pack(side=tk.TOP,pady=15)
lbl_buscar_usuario = tk.Label( frame_buscar_usuario, text="Buscar Usuario: ")
lbl_buscar_usuario.pack( side=tk.LEFT, padx=5 )
input_buscar_usuario = tk.Entry( frame_buscar_usuario )
input_buscar_usuario.pack( side=tk.LEFT, padx=5 )
btn_buscar_usuario = tk.Button( frame_buscar_usuario, text="Buscar" )
btn_buscar_usuario.pack(side=tk.LEFT , padx=5)

columnas_usuarios = ('id_usuario', 'Nombre')
frame_tabla_usuarios = tk.Frame(frame_usuarios )
frame_tabla_usuarios.pack(side=tk.TOP, fill=tk.X , padx=4)
tree_usuarios = ttk.Treeview(frame_tabla_usuarios, columns=columnas_usuarios, show='headings')
tree_usuarios.heading( 'id_usuario', text='Id Usuario' )
tree_usuarios.heading( 'Nombre', text='Nombre' )
tree_usuarios.pack(side=tk.LEFT, fill=tk.X, expand=True)
scrollbar_usuarios = ttk.Scrollbar( frame_tabla_usuarios, orient='vertical', command=tree_usuarios.yview )
tree_usuarios.config(yscrollcommand=scrollbar_usuarios.set)
scrollbar_usuarios.pack(side=tk.LEFT)

frame_gestion_usuarios = tk.Frame(frame_usuarios)
frame_gestion_usuarios.pack( side=tk.TOP, pady= 15 )
btn_ingresar_usuario = tk.Button( frame_gestion_usuarios, text="Agregar Usuario", command=window_agregar_usuario)
btn_ingresar_usuario.pack(side=tk.LEFT, padx=10)
btn_eliminar_usuario = tk.Button( frame_gestion_usuarios, text="Eliminar Usuario" )
btn_eliminar_usuario.pack(side=tk.LEFT,padx=10)

#Panel de Prestamos de libros______________________________________________________________________________________________
#Buscar Libro para la la funcion agregar prestamo
def seleccionar_libro( entry_isbn:any=None, entry_titulo:any=None, tipo_busqueda=0 , str_tipo_busqueda = ""):
    tabla_usuarios_prestamo = tk.Toplevel()
    tabla_usuarios_prestamo.title(f"Seleccionar {str_tipo_busqueda}")
    tabla_usuarios_prestamo.geometry("700x400")

    frame_buscar_libro_prestamo = tk.Frame( tabla_usuarios_prestamo )
    frame_buscar_libro_prestamo.pack(side=tk.TOP,pady=15)
    lbl_buscar_libro_pres = tk.Label( frame_buscar_libro_prestamo, text=f"Buscar {str_tipo_busqueda}: ")
    lbl_buscar_libro_pres.pack( side=tk.LEFT, padx=5 )
    input_buscar_libro_pres = tk.Entry( frame_buscar_libro_prestamo )
    input_buscar_libro_pres.pack( side=tk.LEFT, padx=5 )
    btn_buscar_libro_pres = tk.Button( frame_buscar_libro_prestamo, text="Buscar" )
    btn_buscar_libro_pres.pack(side=tk.LEFT , padx=5)

    #columnas_libros_prestamo = ('ISBN', 'Titulo', 'Autor')
    columnas_tabla_selecionar_datos = ()
    aux_columnas = []
    if ( tipo_busqueda == 1 ):
        aux_columnas.append("ISBN")
        aux_columnas.append("Titulo")
        aux_columnas.append("Autor")
        columnas_tabla_selecionar_datos = tuple(aux_columnas)
    elif (tipo_busqueda == 2):
        aux_columnas.append("ID")
        aux_columnas.append("Nombre")
        columnas_tabla_selecionar_datos = tuple(aux_columnas)
    frame_tabla_libros_prestamo = tk.Frame(tabla_usuarios_prestamo )
    frame_tabla_libros_prestamo.pack(side=tk.TOP, fill=tk.X , padx=4)
    tree_libros_prestamo = ttk.Treeview(frame_tabla_libros_prestamo, columns=columnas_tabla_selecionar_datos, show='headings')
    for titulo in columnas_tabla_selecionar_datos:
        tree_libros_prestamo.heading( titulo, text=titulo )
    tree_libros_prestamo.pack(side=tk.LEFT, fill=tk.X, expand=True)
    scrollbar_libros_prestamo = ttk.Scrollbar( frame_tabla_libros_prestamo, orient='vertical', command=tree_libros_prestamo.yview )
    tree_libros_prestamo.config(yscrollcommand=scrollbar_libros_prestamo.set)
    scrollbar_libros_prestamo.pack(side=tk.LEFT)

    frame_gestion_libros_prestamos = tk.Frame(tabla_usuarios_prestamo)
    frame_gestion_libros_prestamos.pack( side=tk.TOP, pady= 15 )
    btn_ingresar_libro_prestamo = tk.Button( frame_gestion_libros_prestamos, text=f"Seleccionar {str_tipo_busqueda}")
    btn_ingresar_libro_prestamo.pack(side=tk.LEFT, padx=10)

#Funcion para agregar prestamo
def window_agregar_prestamo():
    principal_window = tk.Toplevel(root)
    principal_window.title("Agregar Prestamo")
    principal_window.geometry("350x200")

    lbl_margin = tk.Label( principal_window, text="" )
    lbl_margin.pack(pady=3)
    lbl_isbn = tk.Label( principal_window, text="ISBN: " )
    lbl_isbn.pack(anchor=tk.W, padx=25)
    frame1 = tk.Frame( principal_window )
    frame1.pack( anchor=tk.W, padx=25, fill=tk.X )
    input_isbn = tk.Entry( frame1 )
    input_isbn.pack(side=tk.LEFT, fill=tk.X, expand=True )
    btn_buscar_isbn = tk.Button( frame1, text="Buscar Libro", command=lambda:seleccionar_libro(input_isbn, input_titulo,1,"libro"))
    btn_buscar_isbn.pack(side=tk.LEFT)
    lbl_titulo = tk.Label( principal_window, text="Titulo del libro: " )
    lbl_titulo.pack(anchor=tk.W, padx=25)
    input_titulo = tk.Entry( principal_window , state=tk.DISABLED )
    input_titulo.pack(anchor=tk.W, padx=25, fill=tk.X)
    lbl_usuario = tk.Label( principal_window, text="Usuario: " )
    lbl_usuario.pack(anchor=tk.W, padx=25)
    frame2 = tk.Frame( principal_window )
    frame2.pack( anchor=tk.W, padx=25, fill=tk.X )
    input_usuario = tk.Entry( frame2 )
    input_usuario.pack(side=tk.LEFT, fill=tk.X, expand=True )
    btn_buscar_usuario = tk.Button(frame2, text="Buscar Usuario", command=lambda:seleccionar_libro(input_isbn, input_titulo,2,"usuario"))
    btn_buscar_usuario.pack(side=tk.LEFT)
    btn_agregar = tk.Button( principal_window, text="Agregar" )
    btn_agregar.pack(side=tk.LEFT, padx=25, expand=False)
    btn_cancelar = tk.Button( principal_window, text="Cancelar", command=principal_window.destroy )
    btn_cancelar.pack( side=tk.RIGHT, padx=25 )

frame_prestamos = tk.Frame(root)
frame_prestamos.place( x=0, y=98, width=1150, height=452 )

lbl_titulo_prestamos = tk.Label( frame_prestamos,text="Gestion de Prestamo", font=('italic', 20))
lbl_titulo_prestamos.pack( side=tk.TOP, pady=5 )

frame_buscar_prestamos = tk.Frame( frame_prestamos )
frame_buscar_prestamos.pack(side=tk.TOP,pady=15)
lbl_buscar_prestamos = tk.Label( frame_buscar_prestamos, text="Buscar prestamo de libros: ")
lbl_buscar_prestamos.pack( side=tk.LEFT, padx=5 )
input_buscar_prestamos = tk.Entry( frame_buscar_prestamos )
input_buscar_prestamos.pack( side=tk.LEFT, padx=5 )
btn_buscar_prestamos = tk.Button( frame_buscar_prestamos, text="Buscar" )
btn_buscar_prestamos.pack(side=tk.LEFT , padx=5)

columnas_prestamos = ('isbn', 'libro', 'usuario', 'fecha_prestamo')
frame_tabla_prestamos = tk.Frame(frame_prestamos )
frame_tabla_prestamos.pack(side=tk.TOP, fill=tk.X , padx=4)
tree_prestamos = ttk.Treeview(frame_tabla_prestamos, columns=columnas_prestamos, show='headings')
tree_prestamos.heading( 'isbn', text='ISBN' )
tree_prestamos.heading( 'libro', text='Nombre del Libro' )
tree_prestamos.heading( 'usuario', text='Nombre de Usuario' )
tree_prestamos.heading( 'fecha_prestamo', text='Fecha de Prestamo')
tree_prestamos.pack(side=tk.LEFT, fill=tk.X, expand=True)
scrollbar_prestamos = ttk.Scrollbar( frame_tabla_prestamos, orient='vertical', command=tree_prestamos.yview )
tree_prestamos.config(yscrollcommand=scrollbar_prestamos.set)
scrollbar_prestamos.pack(side=tk.LEFT)

frame_gestion_prestamos = tk.Frame(frame_prestamos)
frame_gestion_prestamos.pack( side=tk.TOP, pady= 15 )
btn_ingresar_prestamos = tk.Button( frame_gestion_prestamos, text="Prestar Libro", command=window_agregar_prestamo)
btn_ingresar_prestamos.pack(side=tk.LEFT, padx=10)
btn_eliminar_prestamos = tk.Button( frame_gestion_prestamos, text="Devolucion de Libro" )
btn_eliminar_prestamos.pack(side=tk.LEFT,padx=10)

#Llamar al frame principal
frame_libros.tkraise()

root.mainloop()