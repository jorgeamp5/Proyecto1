import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import re

DATA_FILE_USUARIOS = "usuarios.txt"

#LEER, GUARDAR Y BUSCAR USUARIOS
def leer_usuarios():
    """Lee los usuarios desde el archivo."""
    if not os.path.exists(DATA_FILE_USUARIOS):
        return []
    usuarios = []
    with open(DATA_FILE_USUARIOS, "r") as file:
        for line in file:
            datos = line.strip().split("\t")
            if len(datos) >= 4:
                usuarios.append(datos[:4])
    return usuarios

# AUTOINCREMENTO ID
def obtener_siguiente_id():
    usuarios = leer_usuarios()
    max_id = 0
    for usuario in usuarios:
        try:
            current_id = int(usuario[0])
            if current_id > max_id:
                max_id = current_id
        except ValueError:
            continue
    return max_id + 1


# AGREGAR USUARIOS
def window_agregar_usuario(root, tree_usuarios):
    def agregar_usuario(event=None):
        id_entry = input_id.get()
        nombre = input_nombre.get()
        telefono = input_telefono.get()
        email = input_email.get()

        if id_entry == "" or nombre == "" or telefono == "" or email == "":
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        with open('usuarios.txt', 'a') as file:
            file.write(f"{id_entry}\t{nombre}\t{telefono}\t{email}\n")

            tree_usuarios.insert("", "end", values=(id_entry, nombre, telefono, email))
            messagebox.showinfo("Éxito", "El libro se agregó correctamente.")
            principal_window.destroy()

    principal_window = tk.Toplevel(root)
    principal_window.title("Agregar Usuario")
    principal_window.geometry("350x300")

    lbl_margin = tk.Label(principal_window, text="")
    lbl_margin.pack(pady=3)

    lbl_id = tk.Label(principal_window, text="ID:", fg="white", background="#2E2E2E")
    lbl_id.pack(anchor=tk.W, padx=25)
    input_id = tk.StringVar(value=str(obtener_siguiente_id()))
    id_entry = tk.Entry(principal_window, textvariable=input_id, state="readonly")  # SOLO VISTA
    id_entry.pack(anchor=tk.W, padx=25, fill=tk.X)

    lbl_nombre = tk.Label(principal_window, text="Ingrese Nombre: ")
    lbl_nombre.pack(anchor=tk.W, padx=25)
    input_nombre = tk.Entry(principal_window)
    input_nombre.pack(anchor=tk.W, padx=25, fill=tk.X)

    lbl_telefono = tk.Label(principal_window, text="Ingrese Telefono: ")
    lbl_telefono.pack(anchor=tk.W, padx=25)
    input_telefono = tk.Entry(principal_window)
    input_telefono.pack(anchor=tk.W, padx=25, fill=tk.X)

    lbl_email = tk.Label(principal_window, text="Ingrese E-mail: ")
    lbl_email.pack(anchor=tk.W, padx=25)
    input_email = tk.Entry(principal_window)
    input_email.pack(anchor=tk.W, padx=25, fill=tk.X)

    #input_email.bind('<Return>', agregar_usuarios)
    btn_agregar = tk.Button(principal_window, text="Agregar", command=agregar_usuario)
    btn_agregar.pack(side=tk.LEFT, padx=25, expand=False)

    btn_cancelar = tk.Button(principal_window, text="Cancelar", command=principal_window.destroy)
    btn_cancelar.pack(side=tk.RIGHT, padx=25)



# GESTIONAR USUARIOS Y TREE_USUARIOS VARIABLE GLOBAL
def cargar_usuarios(tree_usuarios):
    try:
        with open('usuarios.txt', 'r') as file:
            for line in file:
                id_var, nombre, telefono, email = line.strip().split("\t")
                tree_usuarios.insert("", "end", values=(id_var, nombre, telefono, email))
    except FileNotFoundError:
        pass

def eliminar_usuario(tree_usuarios):
    selected_item = tree_usuarios.selection()

    if not selected_item:
        messagebox.showerror("Error", "Debe seleccionar un usuario para eliminar.")
        return

    input_id_seleccionado = tree_usuarios.item(selected_item, "values")[0]

    respuesta = messagebox.askyesno("Eliminar Usuario", f"¿Está seguro de que desea eliminar el usuario con el ID: {input_id_seleccionado}?")

    if respuesta:
        tree_usuarios.delete(selected_item)

        with open('usuarios.txt', 'r') as file:
            lineas = file.readlines()

        with open('usuarios.txt', 'w') as file:
            for linea in lineas:
                if not linea.startswith(input_id_seleccionado):
                    file.write(linea)

        messagebox.showinfo("Eliminado", f"El usuario con ID {input_id_seleccionado} ha sido eliminado.")

def frame_usuarios(root):
    frame_usuarios = tk.Frame(root)
    frame_usuarios.place(x=0, y=98, width=1150, height=452)

    lbl_nombre_usuarios = tk.Label(frame_usuarios, text="Gestion de Usuarios", font=('italic', 20))
    lbl_nombre_usuarios.pack(side=tk.TOP, pady=5)

    #ICONO DE BUSCAR
    icono_buscar = tk.PhotoImage(file="img/icono_buscar.png").subsample(15)

    frame_buscar_usuario = tk.Frame(frame_usuarios, bg="#e8cb9a")
    frame_buscar_usuario.pack(side=tk.TOP, pady=15)
    lbl_buscar_usuario = tk.Label(frame_buscar_usuario, text="Buscar Libro: ", bg="#e8cb9a", font=('bold', 13))
    lbl_buscar_usuario.pack(side=tk.LEFT, padx=5)
    input_buscar_usuario = tk.Entry(frame_buscar_usuario)
    input_buscar_usuario.pack(side=tk.LEFT, padx=5)
    btn_buscar_usuario = tk.Button(frame_buscar_usuario, image=icono_buscar, bg="#c9d6ce", relief="flat")
    btn_buscar_usuario.image = icono_buscar
    btn_buscar_usuario.pack(side=tk.LEFT, padx=5)

    columnas_usuarios = ('ID', 'Nombre', 'Telefono', 'E-mail')
    frame_tabla_usuarios = tk.Frame(frame_usuarios)
    frame_tabla_usuarios.pack(side=tk.TOP, fill=tk.X, padx=4)
    tree_usuarios = ttk.Treeview(frame_tabla_usuarios, columns=columnas_usuarios, show='headings')
    tree_usuarios.heading('ID', text='ID')
    tree_usuarios.heading('Nombre', text='Nombre')
    tree_usuarios.heading('Telefono', text='Telefono')
    tree_usuarios.heading('E-mail', text='E-mail')
    tree_usuarios.pack(side=tk.LEFT, fill=tk.X, expand=True)
    scrollbar_usuarios = ttk.Scrollbar(frame_tabla_usuarios, orient='vertical', command=tree_usuarios.yview)
    tree_usuarios.config(yscrollcommand=scrollbar_usuarios.set)
    scrollbar_usuarios.pack(side=tk.LEFT)

    frame_gestion_usuarios = tk.Frame(frame_usuarios)
    frame_gestion_usuarios.pack(side=tk.TOP, pady=15)

    icono_agregar = tk.PhotoImage(file="img/agregar_libro.png").subsample(100, 30)
    icono_editar = tk.PhotoImage(file="img/agregar_libro.png").subsample(20, 20)
    icono_eliminar = tk.PhotoImage(file="img/agregar_libro.png").subsample(20, 20)

    btn_ingresar_usuario = tk.Button(frame_gestion_usuarios, text="Agregar Usuario", image=icono_agregar, compound="left", bg="#93D973", command=lambda: window_agregar_usuario(root, tree_usuarios))
    btn_ingresar_usuario.image = icono_agregar  # Mantener una referencia al icono
    btn_ingresar_usuario.pack(side=tk.LEFT, padx=10, ipadx=20, ipady=10)


    btn_editar_usuario = tk.Button(frame_gestion_usuarios, text="Editar Usuario", image=icono_editar, compound="left", bg="#F1E69E")
    btn_editar_usuario.image = icono_editar  # Mantener una referencia al icono
    btn_editar_usuario.pack(side=tk.LEFT, padx=10)

    btn_eliminar_usuario = tk.Button(frame_gestion_usuarios, text="Eliminar Usuario", image=icono_eliminar, compound="left", bg="#F28F79", command=lambda: eliminar_usuario(tree_usuarios))
    btn_eliminar_usuario.image = icono_eliminar  # Mantener una referencia al icono
    btn_eliminar_usuario.pack(side=tk.LEFT, padx=10)

    cargar_usuarios(tree_usuarios)

    return frame_usuarios, tree_usuarios
