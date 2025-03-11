import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import re

# Función para verificar el formato del ISBN
def es_isbn_valido(isbn):
    # Verificar ISBN-10
    if re.match(r'^\d{9}[\dX]$', isbn):  # 9 dígitos + 1 dígito o 'X'
        return True
    # Verificar ISBN-13
    elif re.match(r'^\d{13}$', isbn):  # 13 dígitos
        return True
    return False

def window_agregar_libro(root, tree_libros):
    def agregar_libro(event=None):
        isbn = input_isbn.get()
        titulo = input_titulo.get()
        autor = input_autor.get()

        if isbn == "" or titulo == "" or autor == "":
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if not es_isbn_valido(isbn):
            messagebox.showerror("Error", "El ISBN debe ser un ISBN-10 (9 dígitos + 'X') o un ISBN-13 (13 dígitos).")
            return

        for item in tree_libros.get_children():
            if tree_libros.item(item, 'values')[0] == isbn:
                messagebox.showerror("Error", "El ISBN ya existe.")
                return

        with open('libros.txt', 'a') as file:
            file.write(f"{isbn}\t{titulo}\t{autor}\n")

        tree_libros.insert("", "end", values=(isbn, titulo, autor))
        messagebox.showinfo("Éxito", "El libro se agregó correctamente.")
        principal_window.destroy()

    principal_window = tk.Toplevel(root, background='#e8cb9a')
    principal_window.title("Agregar Libro")
    principal_window.geometry("350x300")

    lbl_margin = tk.Label(principal_window, background='#e8cb9a')
    lbl_margin.pack(pady=3)

    lbl_isbn = tk.Label(principal_window, text="Ingrese ISBN: ", background='#e8cb9a', font=('Verdana', 13))
    lbl_isbn.pack(anchor=tk.W, padx=25)
    input_isbn = tk.Entry(principal_window)
    input_isbn.pack(anchor=tk.W, padx=25, fill=tk.X, pady=5)

    lbl_titulo = tk.Label(principal_window, text="Ingrese Titulo: ", background='#e8cb9a', font=('Verdana', 13))
    lbl_titulo.pack(anchor=tk.W, padx=25)
    input_titulo = tk.Entry(principal_window)
    input_titulo.pack(anchor=tk.W, padx=25, fill=tk.X, pady=5)

    lbl_autor = tk.Label(principal_window, text="Ingrese Autor: ", background='#e8cb9a', font=('Verdana', 13))
    lbl_autor.pack(anchor=tk.W, padx=25)
    input_autor = tk.Entry(principal_window)
    input_autor.pack(anchor=tk.W, padx=25, fill=tk.X, pady=10)

    input_autor.bind('<Return>', agregar_libro)

    btn_agregar = tk.Button(principal_window, text="Agregar", font=('Verdana', 10), bg="#ffedba", command=agregar_libro)
    btn_agregar.pack(side=tk.LEFT, padx=25, pady=10)

    btn_cancelar = tk.Button(principal_window, text="Cancelar", font=('Verdana', 10), bg="#ffedba", command=principal_window.destroy)
    btn_cancelar.pack(side=tk.RIGHT, padx=25, pady=10)

def cargar_libros(tree_libros):
    try:
        with open('libros.txt', 'r') as file:
            for line in file:
                isbn, titulo, autor = line.strip().split("\t")
                tree_libros.insert("", "end", values=(isbn, titulo, autor))
    except FileNotFoundError:
        pass

def eliminar_libro(tree_libros):
    selected_item = tree_libros.selection()

    if not selected_item:
        messagebox.showerror("Error", "Debe seleccionar un libro para eliminar.")
        return

    isbn_seleccionado = tree_libros.item(selected_item, "values")[0]

    respuesta = messagebox.askyesno("Eliminar Libro", f"¿Está seguro de que desea eliminar el libro con ISBN {isbn_seleccionado}?")

    if respuesta:
        tree_libros.delete(selected_item)

        with open('libros.txt', 'r') as file:
            lineas = file.readlines()

        with open('libros.txt', 'w') as file:
            for linea in lineas:
                if not linea.startswith(isbn_seleccionado):
                    file.write(linea)

        messagebox.showinfo("Eliminado", f"El libro con ISBN {isbn_seleccionado} ha sido eliminado.")

def window_editar_libro(root, tree_libros):
    def cargar_datos_editar():
        selected_item = tree_libros.selection()
        if not selected_item:
            messagebox.showerror("Error", "Debe seleccionar un libro para editar.")
            return

        isbn_seleccionado = tree_libros.item(selected_item, "values")[0]
        with open('libros.txt', 'r') as file:
            for line in file:
                if line.startswith(isbn_seleccionado):
                    isbn, titulo, autor = line.strip().split("\t")
                    input_isbn.delete(0, tk.END)
                    input_isbn.insert(0, isbn)
                    input_titulo.delete(0, tk.END)
                    input_titulo.insert(0, titulo)
                    input_autor.delete(0, tk.END)
                    input_autor.insert(0, autor)
                    break

    def editar_libro(event=None):
        isbn = input_isbn.get()
        titulo = input_titulo.get()
        autor = input_autor.get()

        if isbn == "" or titulo == "" or autor == "":
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if not es_isbn_valido(isbn):
            messagebox.showerror("Error", "El ISBN debe ser un ISBN-10 (9 dígitos + 'X') o un ISBN-13 (13 dígitos).")
            return

        selected_item = tree_libros.selection()
        original_item = tree_libros.item(selected_item, "values")

        if (isbn, titulo, autor) == original_item:
            messagebox.showinfo("Éxito", "No se realizaron cambios.")
            principal_window.destroy()
            return


        with open('libros.txt', 'r') as file:
            libros = file.readlines()

        for line in libros:
            if line.startswith(isbn) and line.strip() != f"{isbn}\t{titulo}\t{autor}":
                if original_item[0] != isbn:
                    messagebox.showerror("Error", "El ISBN ya existe.")
                    return

        with open('libros.txt', 'w') as file:
            for line in libros:
                if line.startswith(original_item[0]):
                    file.write(f"{isbn}\t{titulo}\t{autor}\n")
                else:
                    file.write(line)

        # Actualizar el árbol
        for item in tree_libros.get_children():
            if tree_libros.item(item, "values")[0] == original_item[0]:
                tree_libros.item(item, values=(isbn, titulo, autor))

        messagebox.showinfo("Éxito", "Libro actualizado correctamente.")
        principal_window.destroy()

    principal_window = tk.Toplevel(root, background='#e8cb9a')
    principal_window.title("Editar Libro")
    principal_window.geometry("350x300")

    lbl_margin = tk.Label(principal_window, background='#e8cb9a')
    lbl_margin.pack(pady=3)

    lbl_isbn = tk.Label(principal_window, text="Ingrese ISBN: ", background='#e8cb9a', font=('Verdana', 13))
    lbl_isbn.pack(anchor=tk.W, padx=25)
    input_isbn = tk.Entry(principal_window)
    input_isbn.pack(anchor=tk.W, padx=25, fill=tk.X, pady=5)

    lbl_titulo = tk.Label(principal_window, text="Ingrese Titulo: ", background='#e8cb9a', font=('Verdana', 13))
    lbl_titulo.pack(anchor=tk.W, padx=25)
    input_titulo = tk.Entry(principal_window)
    input_titulo.pack(anchor=tk.W, padx=25, fill=tk.X, pady=5)

    lbl_autor = tk.Label(principal_window, text="Ingrese Autor: ", background='#e8cb9a', font=('Verdana', 13))
    lbl_autor.pack(anchor=tk.W, padx=25)
    input_autor = tk.Entry(principal_window)
    input_autor.pack(anchor=tk.W, padx=25, fill=tk.X, pady=10)

    input_autor.bind('<Return>', editar_libro)

    btn_editar = tk.Button(principal_window, text="Guardar Cambios", font=('Verdana', 10), bg="#ffedba", command=editar_libro)
    btn_editar.pack(side=tk.LEFT, padx=25, pady=10)

    btn_cancelar = tk.Button(principal_window, text="Cancelar", font=('Verdana', 10), bg="#ffedba", command=principal_window.destroy)
    btn_cancelar.pack(side=tk.RIGHT, padx=25, pady=10)

    cargar_datos_editar()


def buscar_libros(tree_libros, input_buscar_libro):
    search_text = input_buscar_libro.get().lower()
    for item in tree_libros.get_children():
        tree_libros.delete(item)

    with open('libros.txt', 'r') as file:
        for line in file:
            isbn, titulo, autor = line.strip().split("\t")
            if (search_text in isbn.lower() or
                    search_text in titulo.lower() or
                    search_text in autor.lower()):
                tree_libros.insert("", "end", values=(isbn, titulo, autor))

    if search_text == "":
        cargar_libros(tree_libros)


def frame_libros(root):
    frame_libros = tk.Frame(root, bg="#e8cb9a")
    frame_libros.place(x=0, y=98, width=1150, height=452)

    lbl_titulo_libros = tk.Label(frame_libros, text="Gestion de Libros", font=('Verdana', 20), bg="#e8cb9a",
                                 fg="#0b0639")
    lbl_titulo_libros.pack(side=tk.TOP, pady=5)

    icono_buscar = tk.PhotoImage(file="img/icono_buscar.png").subsample(15)

    frame_buscar_libro = tk.Frame(frame_libros, bg="#e8cb9a")
    frame_buscar_libro.pack(side=tk.TOP, pady=15)
    lbl_buscar_libro = tk.Label(frame_buscar_libro, text="Buscar Libro: ", bg="#e8cb9a", font=('bold', 13))
    lbl_buscar_libro.pack(side=tk.LEFT, padx=5)
    input_buscar_libro = tk.Entry(frame_buscar_libro)
    input_buscar_libro.pack(side=tk.LEFT, padx=5)
    btn_buscar_libro = tk.Button(frame_buscar_libro, image=icono_buscar, bg="#e8cb9a", relief="flat",
                                 command=lambda: buscar_libros(tree_libros, input_buscar_libro))
    btn_buscar_libro.image = icono_buscar
    btn_buscar_libro.pack(side=tk.LEFT, padx=5)

    columnas_libros = ('ISBN', 'Titulo', 'Autor',)
    frame_tabla_libros = tk.Frame(frame_libros)
    frame_tabla_libros.pack(side=tk.TOP, fill=tk.X, padx=4)
    tree_libros = ttk.Treeview(frame_tabla_libros, columns=columnas_libros, show='headings')
    tree_libros.heading('ISBN', text='ISBN')
    tree_libros.heading('Titulo', text='Titulo')
    tree_libros.heading('Autor', text='Autor')
    tree_libros.pack(side=tk.LEFT, fill=tk.X, expand=True)
    scrollbar_libros = ttk.Scrollbar(frame_tabla_libros, orient='vertical', command=tree_libros.yview)
    tree_libros.config(yscrollcommand=scrollbar_libros.set)
    scrollbar_libros.pack(side=tk.RIGHT, fill=tk.Y)

    frame_gestion_libros = tk.Frame(frame_libros, bg="#e8cb9a")
    frame_gestion_libros.pack(side=tk.TOP, pady=15)

    icono_agregar = tk.PhotoImage(file="img/agregar_libro.png").subsample(10)
    icono_editar = tk.PhotoImage(file="img/editar_libro.png").subsample(10)
    icono_eliminar = tk.PhotoImage(file="img/delete_book.png").subsample(10)

    btn_ingresar_libro = tk.Button(frame_gestion_libros, text="Agregar Libro", font=('Verdana', 10),
                                   image=icono_agregar,
                                   compound="left", bg="#22fa04",
                                   command=lambda: window_agregar_libro(root, tree_libros))
    btn_ingresar_libro.image = icono_agregar
    btn_ingresar_libro.pack(side=tk.LEFT, padx=10)

    btn_editar_libro = tk.Button(frame_gestion_libros, text="Editar Libro", font=('Verdana', 10), image=icono_editar,
                                 compound="left", bg="#ebfa04", command=lambda: window_editar_libro(root, tree_libros))
    btn_editar_libro.image = icono_editar
    btn_editar_libro.pack(side=tk.LEFT, padx=10)

    btn_eliminar_libro = tk.Button(frame_gestion_libros, text="Eliminar Libro", font=('Verdana', 10),
                                   image=icono_eliminar,
                                   compound="left", bg="#f72b0b", command=lambda: eliminar_libro(tree_libros))
    btn_eliminar_libro.image = icono_eliminar
    btn_eliminar_libro.pack(side=tk.LEFT, padx=10)

    cargar_libros(tree_libros)

    return frame_libros, tree_libros