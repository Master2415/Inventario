import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from Model.ProveedorDAO import listarProveedores

class Frame_Proveedor(tk.Frame):

    def __init__(self, root, width=1745, height=750):
        super().__init__(root, width=width, height=height)
        self.root = root
        self.config(bg='#f0f0f0')  # Color de fondo del frame principal
        self.pack(fill='both', expand=True)
        self.idProveedor = None 
        self.formulario_frame = None  # Inicializa la variable aquí
        self.mostrar_formulario_agregar()

        self.populate_providers()

    def mostrar_formulario_agregar(self):
        if self.formulario_frame:
            self.formulario_frame.destroy()

        self.formulario_frame = tk.Frame(self, bg='#f0f0f0')
        self.formulario_frame.pack(pady=20, padx=20, anchor='n')  # Centrado verticalmente en la parte superior

        self.lblnombreEmpresa = tk.Label(self.formulario_frame, text='Empresa')
        self.lblnombreEmpresa.config(font=('Arial', 15, 'bold'), bg='#f0f0f0')
        self.lblnombreEmpresa.grid(column=0, row=0, padx=10, pady=5, sticky='w')

        self.lblTipo = tk.Label(self.formulario_frame, text='Tipo')
        self.lblTipo.config(font=('Arial', 15, 'bold'), bg='#f0f0f0')
        self.lblTipo.grid(column=0, row=1, padx=10, pady=5, sticky='w')

        self.lblTelefono = tk.Label(self.formulario_frame, text='Teléfono')
        self.lblTelefono.config(font=('Arial', 15, 'bold'), bg='#f0f0f0')
        self.lblTelefono.grid(column=0, row=2, padx=10, pady=5, sticky='w')

        self.lblDireccion = tk.Label(self.formulario_frame, text='Dirección')
        self.lblDireccion.config(font=('Arial', 15, 'bold'), bg='#f0f0f0')
        self.lblDireccion.grid(column=0, row=3, padx=10, pady=5, sticky='w')

        self.lblCorreo = tk.Label(self.formulario_frame, text='Correo')
        self.lblCorreo.config(font=('Arial', 15, 'bold'), bg='#f0f0f0')
        self.lblCorreo.grid(column=0, row=4, padx=10, pady=5, sticky='w')

        entry_bg = '#ffffff'

        self.svNombre = tk.StringVar()
        self.entryNombre = tk.Entry(self.formulario_frame, textvariable=self.svNombre)
        self.entryNombre.config(width=40, font=('Arial', 15), bg=entry_bg)
        self.entryNombre.grid(column=1, row=0, padx=10, pady=5, sticky='w')

        self.svTipo = tk.StringVar()
        self.entryTipo = tk.Entry(self.formulario_frame, textvariable=self.svTipo)
        self.entryTipo.config(width=40, font=('Arial', 15), bg=entry_bg)
        self.entryTipo.grid(column=1, row=1, padx=10, pady=5, sticky='w')

        self.svTelefono = tk.StringVar()
        self.entryTelefono = tk.Entry(self.formulario_frame, textvariable=self.svTelefono)
        self.entryTelefono.config(width=40, font=('Arial', 15), bg=entry_bg)
        self.entryTelefono.grid(column=1, row=2, padx=10, pady=5, sticky='w')

        self.svDireccion = tk.StringVar()
        self.entryDireccion = tk.Entry(self.formulario_frame, textvariable=self.svDireccion)
        self.entryDireccion.config(width=40, font=('Arial', 15), bg=entry_bg)
        self.entryDireccion.grid(column=1, row=3, padx=10, pady=5, sticky='w')

        self.svCorreo = tk.StringVar()
        self.entryCorreo = tk.Entry(self.formulario_frame, textvariable=self.svCorreo)
        self.entryCorreo.config(width=40, font=('Arial', 15), bg=entry_bg)
        self.entryCorreo.grid(column=1, row=4, padx=10, pady=5, sticky='w')

        self.btnBuscar = tk.Button(self.formulario_frame, text='Buscar')
        self.btnBuscar.config(width=20, font=('Arial', 12, 'bold'), fg='#ffffff', bg='#007ACC')
        self.btnBuscar.grid(column=0, row=5, columnspan=2, pady=(10, 0))

        self.tablaProveedores = ttk.Treeview(self, columns=('ID', 'Empresa', 'Tipo', 'Teléfono', 'Dirección', 'Correo'))
        self.tablaProveedores.pack(padx=20, pady=(20, 0), anchor='n')  # Centrado verticalmente debajo del formulario

        self.scrollProveedor = ttk.Scrollbar(self, orient='vertical', command=self.tablaProveedores.yview)
        self.scrollProveedor.pack(side='right', fill='y')

        self.tablaProveedores.configure(yscrollcommand=self.scrollProveedor.set)
        self.tablaProveedores.tag_configure('evenrow', background='#E8E8E8')

        self.tablaProveedores.heading('#0', text='ID')
        self.tablaProveedores.heading('#1', text='Empresa')
        self.tablaProveedores.heading('#2', text='Tipo')
        self.tablaProveedores.heading('#3', text='Teléfono')
        self.tablaProveedores.heading('#4', text='Dirección')
        self.tablaProveedores.heading('#5', text='Correo')

        self.tablaProveedores.column('#0', anchor=tk.W, width=50)
        self.tablaProveedores.column('#1', anchor=tk.W, width=250)
        self.tablaProveedores.column('#2', anchor=tk.W, width=150)
        self.tablaProveedores.column('#3', anchor=tk.W, width=170)
        self.tablaProveedores.column('#4', anchor=tk.W, width=250)
        self.tablaProveedores.column('#5', anchor=tk.W, width=200)

        # Botones debajo de la tabla
        self.btnNuevo = tk.Button(self, text='Agregar Proveedor')
        self.btnNuevo.config(width=20, font=('Arial', 12, 'bold'), fg='#ffffff', bg='#5CB85C')
        self.btnNuevo.pack(pady=(20, 10))

        self.btnEditar = tk.Button(self, text='Editar Proveedor')
        self.btnEditar.config(width=20, font=('Arial', 12, 'bold'), fg='#ffffff', bg='#007ACC')
        self.btnEditar.pack()

        self.btnEliminar = tk.Button(self, text='Eliminar Proveedor')
        self.btnEliminar.config(width=20, font=('Arial', 12, 'bold'), fg='#ffffff', bg='#D9534F')
        self.btnEliminar.pack(pady=(10, 20))

    def populate_providers(self):
        try:
            self.listaProveedores = listarProveedores()
            for i, p in enumerate(self.listaProveedores):
                tags = ('evenrow',) if i % 2 == 0 else ()
                self.tablaProveedores.insert('', 'end', text=p[0], values=(p[1], p[2], p[3], p[4], p[5]), tags=tags)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo mostrar el proveedor: {e}")

