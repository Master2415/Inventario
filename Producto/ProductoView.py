import tkinter as tk
import tkcalendar as tc
from tkinter import *
from tkinter import messagebox
from tkinter import ttk, Toplevel
from tkcalendar import *
from datetime import datetime, date


class Frame_Producto(tk.Frame):

    def __init__(self, root):
        super().__init__(root, width=1280, height=720)
        self.root = root
        self.config(bg='#BBBBBB')  # Establecer el color de fondo del frame principal
        self.pack()

        #LABELS
        self.lblcodigo = tk.Label(self, text='Codigo: ')
        self.lblcodigo.config(font=('ARIAl',15,'bold'), bg='#BBBBBB')
        self.lblcodigo.grid(column=0, row=0, padx=10, pady=5)

        self.lblNombre = tk.Label(self, text='Nombre: ')
        self.lblNombre.config(font=('ARIAl',15,'bold'), bg='#BBBBBB')
        self.lblNombre.grid(column=0, row=1, padx=10, pady=5)

        self.lbltipo = tk.Label(self, text='Tipo: ')
        self.lbltipo.config(font=('ARIAl',15,'bold'), bg='#BBBBBB')
        self.lbltipo.grid(column=0, row=2, padx=10, pady=5)

        self.lblcantidad = tk.Label(self, text='Cantidad a ingresar: ')
        self.lblcantidad.config(font=('ARIAl',15,'bold'), bg='#BBBBBB')
        self.lblcantidad.grid(column=0, row=3, padx=10, pady=5)

        self.lblprecio = tk.Label(self, text='Precio: ')
        self.lblprecio.config(font=('ARIAl',15,'bold'), bg='#BBBBBB')
        self.lblprecio.grid(column=0, row=4, padx=10, pady=5)

        self.lblfecha = tk.Label(self, text='Fecha: ')
        self.lblfecha.config(font=('ARIAl',15,'bold'), bg='#BBBBBB')
        self.lblfecha.grid(column=0, row=5, padx=10, pady=5)

        # Entrys
        self.svCodigo = tk.StringVar()
        self.entryCodigo = tk.Entry(self, textvariable=self.svCodigo)
        self.entryCodigo.config(width=35, font=('ARIAL',15))
        self.entryCodigo.grid(column=1, row=0, padx=10, pady=5, columnspan=2)

        self.svNombre = tk.StringVar()
        self.entryNombre = tk.Entry(self, textvariable=self.svNombre)
        self.entryNombre.config(width=35, font=('ARIAL',15))
        self.entryNombre.grid(column=1, row=0, padx=10, pady=5, columnspan=2)

        self.svNombre = tk.StringVar()
        self.entryNombre = tk.Entry(self, textvariable=self.svNombre)
        self.entryNombre.config(width=35, font=('ARIAL',15))
        self.entryNombre.grid(column=1, row=0, padx=10, pady=5, columnspan=2)

        self.svNombre = tk.StringVar()
        self.entryNombre = tk.Entry(self, textvariable=self.svNombre)
        self.entryNombre.config(width=35, font=('ARIAL',15))
        self.entryNombre.grid(column=1, row=0, padx=10, pady=5, columnspan=2)

        self.svNombre = tk.StringVar()
        self.entryNombre = tk.Entry(self, textvariable=self.svNombre)
        self.entryNombre.config(width=35, font=('ARIAL',15))
        self.entryNombre.grid(column=1, row=0, padx=10, pady=5, columnspan=2)

        self.svNombre = tk.StringVar()
        self.entryNombre = tk.Entry(self, textvariable=self.svNombre)
        self.entryNombre.config(width=35, font=('ARIAL',15))
        self.entryNombre.grid(column=1, row=0, padx=10, pady=5, columnspan=2)

        #Botones
        self.btnNuevo = tk.Button(self, text='Nuevo')
        self.btnNuevo.config(width=20, font=('ARIAL',12,'bold'), fg='#DAD5D6', bg='#158645')
        self.btnNuevo.grid(column=0, row=9, padx=10, pady=5)