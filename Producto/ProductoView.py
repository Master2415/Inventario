import tkinter as tk
import tkcalendar as tc
from tkinter import *
from tkinter import messagebox
from tkinter import ttk, Toplevel
from tkcalendar import *
from datetime import datetime, date
from Producto.ProductoDAO import *


class Frame_Producto(tk.Frame):

    def __init__(self, root):
        super().__init__(root, width=1280, height=720)
        self.root = root
        self.config(bg='#BBBBBB')  # Establecer el color de fondo del frame principal
        self.pack()
        self.tablaProductos()

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
        self.entryNombre.grid(column=1, row=1, padx=10, pady=5, columnspan=2)

        self.svTipo = tk.StringVar()
        self.entryTipo = tk.Entry(self, textvariable=self.svTipo)
        self.entryTipo.config(width=35, font=('ARIAL',15))
        self.entryTipo.grid(column=1, row=2, padx=10, pady=5, columnspan=2)

        self.svCantidad = tk.StringVar()
        self.entryCantidad = tk.Entry(self, textvariable=self.svCantidad)
        self.entryCantidad.config(width=35, font=('ARIAL',15))
        self.entryCantidad.grid(column=1, row=3, padx=10, pady=5, columnspan=2)

        self.svPrecio = tk.StringVar()
        self.entryPrecio = tk.Entry(self, textvariable=self.svPrecio)
        self.entryPrecio.config(width=35, font=('ARIAL',15))
        self.entryPrecio.grid(column=1, row=4, padx=10, pady=5, columnspan=2)

        self.svFecha = tk.StringVar()
        self.entryFecha = tk.Entry(self, textvariable=self.svFecha)
        self.entryFecha.config(width=35, font=('ARIAL',15))
        self.entryFecha.grid(column=1, row=5, padx=10, pady=5, columnspan=2)

        #TRAER FECHA Y HORA ACTUAL
        fecha_actual = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

        # Asignar la fecha formateada a la variable svFecha
        self.svFecha.set(fecha_actual)

        #Botones
        self.btnNuevo = tk.Button(self, text='Nuevo', command=self.ingresarProducto)
        self.btnNuevo.config(width=20, font=('ARIAL',12,'bold'), fg='#DAD5D6', bg='#158645')
        self.btnNuevo.grid(column=0, row=9, padx=10, pady=5)

    def ingresarProducto(self):
        producto = Producto(self.svCodigo.get(), self.svTipo.get(), self.svNombre.get(), self.svCantidad.get(), self.svPrecio.get(), self.svFecha.get())
        guardarProducto(producto)

    def tablaProductos(self):
        
        self.listaProductos = listarProductos()

        self.tabla = ttk.Treeview(self, column=('Codigo', 'Tipo', 'Nombre','Cantidad disponible','Precio','Fecha de Ingreso'))
        self.tabla.grid(column=0, row=10, columnspan=10, sticky='nsew')  
        
        self.scroll = ttk.Scrollbar(self, orient='vertical', command=self.tabla.yview)
        self.scroll.grid(column=11, row=10, sticky='nse')

        self.tabla.configure(yscrollcommand=self.scroll.set)
        self.tabla.tag_configure('evenrow', background='#D7D7D7')

        self.tabla.heading('#0',text='Codigo')
        self.tabla.heading('#1',text='Tipo')
        self.tabla.heading('#2',text='Nombre')
        self.tabla.heading('#3',text='Cantidad disponible')
        self.tabla.heading('#4',text='Precio')
        self.tabla.heading('#5',text='Fecha de Ingreso')


        self.tabla.column("#0", anchor=W, width=70)
        self.tabla.column("#1", anchor=W, width=150)
        self.tabla.column("#2", anchor=W, width=120)
        self.tabla.column("#3", anchor=W, width=120)
        self.tabla.column("#4", anchor=W, width=120)
        self.tabla.column("#5", anchor=W, width=100)


        for p in self.listaProductos:
            self.tabla.insert('',0,text=p[0], values=(p[1],p[2],p[3],p[4],p[5]), tags=('evenrow',))