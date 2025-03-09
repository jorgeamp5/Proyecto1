import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from libros import frame_libros
from usuarios import frame_usuarios

# MENU GENERAL
root = tk.Tk()
root.title("Biblioteca")
root.geometry("1150x620")

def ocultar_indicador_menu():
    lbl_indicador_libros.config(background='#623307')
    lbl_indicador_usuarios.config(background='#623307')

def cambiar_pagina(lbl_indicador, frame):
    ocultar_indicador_menu()
    lbl_indicador.config(background='#623307')
    # Ocultar todos los frames antes de mostrar el seleccionado
    frame_libros.pack_forget()
    frame_usuarios.pack_forget()

    # Mostrar el frame seleccionado
    frame.pack(fill=tk.BOTH, expand=True)

#--------------------diseno encabezado
encabezado = tk.Frame(root, background='#623307')
encabezado.pack(side=tk.TOP, fill=tk.X)

icono = tk.PhotoImage(file="img/biblioteca_linea.png").subsample(5)

lbl_encabezado = tk.Label(encabezado, text="La Biblioteca", font=('Verdana', 24), background='#623307', fg="white", anchor='center', image=icono, compound='left')
lbl_encabezado.pack(side=tk.TOP, pady=10)

menu_botones = tk.Frame(root, background='#8e582c')
menu_botones.pack(side=tk.TOP, fill=tk.X)
menu_botones.pack_propagate(False)
menu_botones.configure(height=40)

#----------------------libros

btn_libros = tk.Button(menu_botones, text='Libros', bd=0, background="#8e582c", fg="white", command=lambda: cambiar_pagina(lbl_indicador_libros, frame_libros))
btn_libros.pack(side=tk.LEFT, padx=2, fill=tk.Y, ipadx=20)
lbl_indicador_libros = tk.Label(menu_botones, text="", background="#ffedba")
lbl_indicador_libros.place(x=2, y=35, width=79, height=5)

#----------------------usuarios

btn_usuarios = tk.Button(menu_botones, text='Usuarios', bd=0, background="#8e582c", fg="white", command=lambda: cambiar_pagina(lbl_indicador_usuarios, frame_usuarios))
btn_usuarios.pack(side=tk.LEFT, padx=2, fill=tk.Y, ipadx=20)
lbl_indicador_usuarios = tk.Label(menu_botones, text="", background="#ffedba")
lbl_indicador_usuarios.place(x=2, y=35, width=79, height=5)

#---------------------frames

frame_libros, tree_libros = frame_libros(root)
frame_libros.pack(fill=tk.BOTH, expand=True)


frame_usuarios, tree_usuarios = frame_usuarios(root)
frame_usuarios.pack(fill=tk.BOTH, expand=True)

frame_libros.tkraise()
frame_usuarios.pack_forget()

root.mainloop()

