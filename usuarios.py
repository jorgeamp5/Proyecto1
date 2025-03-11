import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import re

DATA_FILE_USUARIOS = "usuarios.txt"


# LEER, GUARDAR Y BUSCAR USUARIOS
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
            messagebox.showinfo("Éxito", "El Usuario se agregó correctamente.")
            principal_window.destroy()

    principal_window = tk.Toplevel(root, background='#e8cb9a')
    principal_window.title("Agregar Usuario")
    principal_window.geometry("350x300")

    lbl_margin = tk.Label(principal_window, background='#e8cb9a')
    lbl_margin.pack(pady=3)

    lbl_id = tk.Label(principal_window, text="ID:", fg="white", background="#2E2E2E")
    lbl_id.pack(anchor=tk.W, padx=25, )
    input_id = tk.StringVar(value=str(obtener_siguiente_id()))
    id_entry = tk.Entry(principal_window, textvariable=input_id, state="readonly")  # SOLO VISTA
    id_entry.pack(anchor=tk.W, padx=25, fill=tk.X)

    lbl_nombre = tk.Label(principal_window, text="Ingrese Nombre: ", background='#e8cb9a', font=('Verdana', 13))
    lbl_nombre.pack(anchor=tk.W, padx=25)
    input_nombre = tk.Entry(principal_window)
    input_nombre.pack(anchor=tk.W, padx=25, fill=tk.X)

    lbl_telefono = tk.Label(principal_window, text="Ingrese Telefono: ", background='#e8cb9a', font=('Verdana', 13))
    lbl_telefono.pack(anchor=tk.W, padx=25)
    input_telefono = tk.Entry(principal_window)
    input_telefono.pack(anchor=tk.W, padx=25, fill=tk.X)

    lbl_email = tk.Label(principal_window, text="Ingrese E-mail: ", background='#e8cb9a', font=('Verdana', 13))
    lbl_email.pack(anchor=tk.W, padx=25)
    input_email = tk.Entry(principal_window)
    input_email.pack(anchor=tk.W, padx=25, fill=tk.X)

    # input_email.bind('<Return>', agregar_usuarios)
    btn_agregar = tk.Button(principal_window, text="Agregar", command=agregar_usuario)
    btn_agregar.pack(side=tk.LEFT, padx=25, expand=False)

    btn_cancelar = tk.Button(principal_window, text="Cancelar", command=principal_window.destroy)
    btn_cancelar.pack(side=tk.RIGHT, padx=25)


# GESTIONAR USUARIOS Y TREE_USUARIOS VARIABLE GLOBAL
def cargar_usuarios(tree_usuarios):
    tree_usuarios.delete(*tree_usuarios.get_children())  # Limpiar tabla antes de cargar datos

    with open('usuarios.txt', 'r') as file:
        for line in file:
            datos = line.strip().split("\t")

            # Verificar que la línea tiene exactamente 4 valores
            if len(datos) == 4:
                tree_usuarios.insert("", "end", values=datos)
            else:
                print(f"Línea ignorada por formato incorrecto: {line.strip()}")  # Para depuración


def buscar_por_nombre(tree_usuarios, input_buscar_usuario):
    nombre_buscar = input_buscar_usuario.get().strip().lower()  # Convertir a minúsculas

    if not nombre_buscar:
        cargar_usuarios(tree_usuarios)  # Si el campo está vacío, recarga toda la lista
        return

    coincidencias = []
    for usuario in leer_usuarios():  # Leer usuarios desde el archivo
        if nombre_buscar in usuario[1].lower():  # Buscar coincidencias parciales
            coincidencias.append(usuario)

    # Limpiar la tabla antes de mostrar los resultados
    tree_usuarios.delete(*tree_usuarios.get_children())

    # Insertar coincidencias en la tabla
    for usuario in coincidencias:
        tree_usuarios.insert("", tk.END, values=usuario)

    if not coincidencias:
        messagebox.showinfo("Búsqueda", f"No se encontraron usuarios con el nombre '{nombre_buscar}'")


# EDITAR USUARIO
def window_editar_usuario(root, tree_usuarios):
    def cargar_datos_editar():
        selected_item = tree_usuarios.selection()

        if not selected_item:
            messagebox.showerror("Error", "Debe seleccionar un usuario para editar.")
            return

        id_seleccionado = tree_usuarios.item(selected_item, "values")[0]
        with open('usuarios.txt', 'r') as file:
            for line in file:
                if line.startswith(id_seleccionado):
                    id_entry, nombre, telefono, email = line.strip().split("\t")
                    # input_id.delete(0, tk.END)
                    # input_id.insert(0, id_entry)
                    input_nombre.delete(0, tk.END)
                    input_nombre.insert(0, nombre)
                    input_telefono.delete(0, tk.END)
                    input_telefono.insert(0, telefono)
                    input_email.delete(0, tk.END)
                    input_email.insert(0, email)
                    break

    def editar_usuario(event=None):
        selected_item = tree_usuarios.selection()

        if not selected_item:
            messagebox.showerror("Error", "Debe seleccionar un usuario para editar.")
            return

        id_seleccionado = tree_usuarios.item(selected_item, "values")[0]
        nombre = input_nombre.get()
        telefono = input_telefono.get()
        email = input_email.get()

        if nombre == "" or telefono == "" or email == "":
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        with open('usuarios.txt', 'r') as file:
            usuarios = file.readlines()

        # Actualizar el archivo sin perder el ID
        with open('usuarios.txt', 'w') as file:
            for line in usuarios:
                datos = line.strip().split("\t")
                if datos[0] == id_seleccionado:
                    file.write(f"{id_seleccionado}\t{nombre}\t{telefono}\t{email}\n")
                else:
                    file.write(line)

                    # Actualizar la tabla (Treeview)
        for item in tree_usuarios.get_children():
            if tree_usuarios.item(item, "values")[0] == id_seleccionado:
                tree_usuarios.item(item, values=(id_seleccionado, nombre, telefono, email))

        messagebox.showinfo("Éxito", "Usuario actualizado correctamente.")
        principal_window.destroy()

    principal_window = tk.Toplevel(root, background='#e8cb9a')
    principal_window.title("Editar Usuario")
    principal_window.geometry("350x300")

    lbl_margin = tk.Label(principal_window, background='#e8cb9a')
    lbl_margin.pack(pady=3)

    lbl_nombre = tk.Label(principal_window, text="Ingrese Nombre: ", background='#e8cb9a', font=('Verdana', 13))
    lbl_nombre.pack(anchor=tk.W, padx=25)
    input_nombre = tk.Entry(principal_window)
    input_nombre.pack(anchor=tk.W, padx=25, fill=tk.X, pady=5)

    lbl_telefono = tk.Label(principal_window, text="Ingrese Telefono: ", background='#e8cb9a', font=('Verdana', 13))
    lbl_telefono.pack(anchor=tk.W, padx=25)
    input_telefono = tk.Entry(principal_window)
    input_telefono.pack(anchor=tk.W, padx=25, fill=tk.X, pady=10)

    lbl_email = tk.Label(principal_window, text="Ingrese E-mail: ", background='#e8cb9a', font=('Verdana', 13))
    lbl_email.pack(anchor=tk.W, padx=25)
    input_email = tk.Entry(principal_window)
    input_email.pack(anchor=tk.W, padx=25, fill=tk.X, pady=15)

    input_email.bind('<Return>', editar_usuario)

    # Botones con más espacio y tamaño ajustado
    btn_editar = tk.Button(principal_window, text="Guardar Cambios", font=('Verdana', 10), bg="#ffedba",
                           command=editar_usuario)
    btn_editar.pack(side=tk.LEFT, padx=25, pady=10)

    btn_cancelar = tk.Button(principal_window, text="Cancelar", font=('Verdana', 10), bg="#ffedba",
                             command=principal_window.destroy)
    btn_cancelar.pack(side=tk.RIGHT, padx=25, pady=10)

    cargar_datos_editar()


def eliminar_usuario(tree_usuarios):
    selected_item = tree_usuarios.selection()

    if not selected_item:
        messagebox.showerror("Error", "Debe seleccionar un usuario para eliminar.")
        return

    input_id_seleccionado = tree_usuarios.item(selected_item, "values")[0]

    respuesta = messagebox.askyesno("Eliminar Usuario",
                                    f"¿Está seguro de que desea eliminar el usuario con el ID: {input_id_seleccionado}?")

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
    frame_usuarios = tk.Frame(root, bg="#e8cb9a")
    frame_usuarios.place(x=0, y=98, width=1150, height=452)

    lbl_nombre_usuarios = tk.Label(frame_usuarios, text="Gestion de Usuarios", bg="#e8cb9a", font=('italic', 20))
    lbl_nombre_usuarios.pack(side=tk.TOP, pady=5)

    # ICONO DE BUSCAR
    icono_buscar = tk.PhotoImage(file="img/icono_buscar.png").subsample(15)

    frame_buscar_usuario = tk.Frame(frame_usuarios, bg="#e8cb9a")
    frame_buscar_usuario.pack(side=tk.TOP, pady=15)
    lbl_buscar_usuario = tk.Label(frame_buscar_usuario, text="Buscar Usuario: ", bg="#e8cb9a", font=('bold', 13))
    lbl_buscar_usuario.pack(side=tk.LEFT, padx=5)
    input_buscar_usuario = tk.Entry(frame_buscar_usuario)
    input_buscar_usuario.pack(side=tk.LEFT, padx=5)
    btn_buscar_usuario = tk.Button(frame_buscar_usuario, image=icono_buscar, bg="#c9d6ce", relief="flat", command=lambda: buscar_por_nombre(tree_usuarios, input_buscar_usuario))
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
    tree_usuarios.column('ID', anchor="center")
    tree_usuarios.column('Nombre', anchor="center")
    tree_usuarios.column('Telefono', anchor="center")
    tree_usuarios.column('E-mail', anchor="center")
    tree_usuarios.pack(side=tk.LEFT, fill=tk.X, expand=True)
    scrollbar_usuarios = ttk.Scrollbar(frame_tabla_usuarios, orient='vertical', command=tree_usuarios.yview)
    tree_usuarios.config(yscrollcommand=scrollbar_usuarios.set)
    scrollbar_usuarios.pack(side=tk.RIGHT, fill=tk.Y)

    frame_gestion_usuarios = tk.Frame(frame_usuarios, bg="#e8cb9a")
    frame_gestion_usuarios.pack(side=tk.TOP, pady=15)

    icono_agregar = tk.PhotoImage(file="img/add-user.png").subsample(10)
    icono_editar = tk.PhotoImage(file="img/edit-user.png").subsample(10)
    icono_eliminar = tk.PhotoImage(file="img/delete-user.png").subsample(10)

    btn_ingresar_usuario = tk.Button(frame_gestion_usuarios, text="Agregar Usuario", font=('Verdana', 10), image=icono_agregar,
                                     compound="left", bg="#22fa04",
                                     command=lambda: window_agregar_usuario(root, tree_usuarios))
    btn_ingresar_usuario.image = icono_agregar
    btn_ingresar_usuario.pack(side=tk.LEFT, padx=10)

    btn_editar_usuario = tk.Button(frame_gestion_usuarios, text="Editar Usuario", font=('Verdana', 10), image=icono_editar, compound="left",
                                   bg="#ebfa04", command=lambda: window_editar_usuario(root, tree_usuarios))
    btn_editar_usuario.image = icono_editar
    btn_editar_usuario.pack(side=tk.LEFT, padx=10)

    btn_eliminar_usuario = tk.Button(frame_gestion_usuarios, text="Eliminar Usuario", font=('Verdana', 10), image=icono_eliminar,
                                     compound="left", bg="#f72b0b", command=lambda: eliminar_usuario(tree_usuarios))
    btn_eliminar_usuario.image = icono_eliminar
    btn_eliminar_usuario.pack(side=tk.LEFT, padx=10)

    cargar_usuarios(tree_usuarios)

    return frame_usuarios, tree_usuarios