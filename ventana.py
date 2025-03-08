import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from libros import frame_libros

# MENU GENERAL
root = tk.Tk()
root.title("Biblioteca")
root.geometry("1150x620")

def ocultar_indicador_menu():
    lbl_indicador_libros.config(background='#8e582c')

def cambiar_pagina(lbl_indicador, frame):
    ocultar_indicador_menu()
    lbl_indicador.config(background='#F28F79')
    frame.tkraise()

encabezado = tk.Frame(root, background='#623307')
encabezado.pack(side=tk.TOP, fill=tk.X)

icono = tk.PhotoImage(file="biblioteca_linea.png").subsample(5)


lbl_encabezado = tk.Label(encabezado, text="La Biblioteca", font=('Verdana', 24), background='#623307', fg="white", anchor='center', image=icono, compound='left')
lbl_encabezado.pack(side=tk.TOP, pady=10)

menu_botones = tk.Frame(root, background='#8e582c')
menu_botones.pack(side=tk.TOP, fill=tk.X)
menu_botones.pack_propagate(False)
menu_botones.configure(height=40)

btn_libros = tk.Button(menu_botones, text='Libros', bd=0, background="#8e582c", fg="white", command=lambda: cambiar_pagina(lbl_indicador_libros, frame_libros))
btn_libros.pack(side=tk.LEFT, padx=2, fill=tk.Y, ipadx=20)

lbl_indicador_libros = tk.Label(menu_botones, text="", background="#ffedba")
lbl_indicador_libros.place(x=2, y=35, width=79, height=5)

frame_libros, tree_libros = frame_libros(root)
frame_libros.pack(fill=tk.BOTH, expand=True)

frame_libros.tkraise()

root.mainloop()

