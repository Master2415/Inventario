import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from Model.ProveedorDAO import *

class Frame_Proveedor(tk.Frame):

    def __init__(self, root, width=1745, height=750):
        super().__init__(root, width=width, height=height)
        self.root = root
        self.config(bg='#f0f0f0')  # Color de fondo del frame principal
        self.pack(fill='both', expand=True)
        self.idProveedor = None 
        self.mostrar_formulario_agregar()
        self.create_table()
        self.deshabilitar()
        self.btnBuscar.config(command=self.buscarProducto)  # Asignar el método de búsqueda al botón

    def mostrar_formulario_agregar(self):
        self.buscar_frame = tk.Frame(self, bg='#f0f0f0')
        self.buscar_frame.pack(pady=10)

        self.svBuscar = tk.StringVar()
        self.entryBuscar = tk.Entry(self.buscar_frame, textvariable=self.svBuscar)
        self.entryBuscar.config(width=40, font=('Arial', 15), bg='#ffffff')
        self.entryBuscar.grid(column=0, row=0, padx=10, pady=5)

        self.btnBuscar = tk.Button(self.buscar_frame, text='Buscar')
        self.btnBuscar.config(width=20, font=('Arial', 12, 'bold'), fg='#ffffff', bg='#007ACC')
        self.btnBuscar.grid(column=1, row=0, padx=10, pady=5)

    def create_table(self, where=""):

        if len(where) > 0:
            self.listaProveedores = listarProveedorCondicion(where)
        else:
            self.listaProveedores = listarProveedores()

        # Frame para la tabla y la barra de desplazamiento
        self.frame_tabla = tk.Frame(self)
        self.frame_tabla.pack(fill='x', expand=False)

        # Crear la tabla con barra de desplazamiento
        self.tablaProveedores = ttk.Treeview(self.frame_tabla, height=10, columns=('ID', 'Empresa', 'Tipo', 'Teléfono', 'Dirección', 'Correo'))
        scrollbar = ttk.Scrollbar(self.frame_tabla, orient='vertical', command=self.tablaProveedores.yview)
        self.tablaProveedores.configure(yscroll=scrollbar.set)
        self.tablaProveedores.pack(side='left', fill='both')
        scrollbar.pack(side='right', fill='y')

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

        for p in self.listaProveedores:            
            self.tablaProveedores.insert('', 'end', text=p[0], values=(p[1], p[2], p[3], p[4], p[5]), tags=('evenrow',))

        # Botones debajo de la tabla
        self.botones_frame = tk.Frame(self, bg='#f0f0f0')
        self.botones_frame.pack(pady=10)

        self.btnNuevo = tk.Button(self.botones_frame, text='Agregar Proveedor', command=self.habilitar)
        self.btnNuevo.config(width=20, font=('Arial', 12, 'bold'), fg='#ffffff', bg='#5CB85C')
        self.btnNuevo.grid(column=0, row=0, padx=10, pady=5)

        self.btnEditar = tk.Button(self.botones_frame, text='Editar Proveedor', command=self.editarProducto)
        self.btnEditar.config(width=20, font=('Arial', 12, 'bold'), fg='#ffffff', bg='#007ACC')
        self.btnEditar.grid(column=1, row=0, padx=10, pady=5)

        self.btnEliminar = tk.Button(self.botones_frame, text='Eliminar Proveedor')
        self.btnEliminar.config(width=20, font=('Arial', 12, 'bold'), fg='#ffffff', bg='#D9534F')
        self.btnEliminar.grid(column=2, row=0, padx=10, pady=5)

        # Frame para el formulario de ingreso de proveedor
        self.formulario_frame = tk.Frame(self, bg='#BBBBBB')
        self.formulario_frame.pack(fill='x', padx=20, pady=10)

        self.lblnombreEmpresa = tk.Label(self.formulario_frame, text='Empresa')
        self.lblnombreEmpresa.config(font=('Arial', 15, 'bold'), bg='#BBBBBB')
        self.lblnombreEmpresa.grid(column=0, row=0, padx=10, pady=5)

        self.lblTipo = tk.Label(self.formulario_frame, text='Tipo')
        self.lblTipo.config(font=('Arial', 15, 'bold'), bg='#BBBBBB')
        self.lblTipo.grid(column=0, row=1, padx=10, pady=5)

        self.lblTelefono = tk.Label(self.formulario_frame, text='Telefono')
        self.lblTelefono.config(font=('Arial', 15, 'bold'), bg='#BBBBBB')
        self.lblTelefono.grid(column=0, row=2, padx=10, pady=5)

        self.lblDireccion = tk.Label(self.formulario_frame, text='Direccion')
        self.lblDireccion.config(font=('Arial', 15, 'bold'), bg='#BBBBBB')
        self.lblDireccion.grid(column=0, row=3, padx=10, pady=5)

        self.lblCorreo = tk.Label(self.formulario_frame, text='Correo')
        self.lblCorreo.config(font=('Arial', 15, 'bold'), bg='#BBBBBB')
        self.lblCorreo.grid(column=0, row=4, padx=10, pady=5)

        # Entrys
        self.svNombre = tk.StringVar()
        self.entryNombre = tk.Entry(self.formulario_frame, textvariable=self.svNombre)
        self.entryNombre.config(width=40, font=('Arial', 15))
        self.entryNombre.grid(column=1, row=0, padx=10, pady=5, columnspan=2)

        self.svTipo = tk.StringVar()
        self.entryTipo = tk.Entry(self.formulario_frame, textvariable=self.svTipo)
        self.entryTipo.config(width=40, font=('Arial', 15))
        self.entryTipo.grid(column=1, row=1, padx=10, pady=5, columnspan=2)

        self.svTelefono = tk.StringVar()
        self.entryTelefono = tk.Entry(self.formulario_frame, textvariable=self.svTelefono)
        self.entryTelefono.config(width=40, font=('Arial', 15))
        self.entryTelefono.grid(column=1, row=2, padx=10, pady=5, columnspan=2)

        self.svDireccion = tk.StringVar()
        self.entryDireccion = tk.Entry(self.formulario_frame, textvariable=self.svDireccion)
        self.entryDireccion.config(width=40, font=('Arial', 15))
        self.entryDireccion.grid(column=1, row=3, padx=10, pady=5, columnspan=2)

        self.svCorreo = tk.StringVar()
        self.entryCorreo = tk.Entry(self.formulario_frame, textvariable=self.svCorreo)
        self.entryCorreo.config(width=40, font=('Arial', 15))
        self.entryCorreo.grid(column=1, row=4, padx=10, pady=5, columnspan=2)

        self.btnGuardar = tk.Button(self.formulario_frame, text='Guardar Nuevo')
        self.btnGuardar.config(width=20, font=('Arial', 12, 'bold'), fg='#ffffff', bg='#5CB85C')
        self.btnGuardar.grid(column=1, row=5, padx=10, pady=5)

        self.btnCancelar = tk.Button(self.formulario_frame, text='Cancelar')
        self.btnCancelar.config(width=20, font=('Arial',12, 'bold'), fg='#ffffff', bg='#D9534F')
        self.btnCancelar.grid(column=2, row=5, padx=10, pady=5)

    def populate_providers(self, proveedores):
        # Limpiar la tabla antes de llenarla
        for row in self.tablaProveedores.get_children():
            self.tablaProveedores.delete(row)
        
        for i, p in enumerate(proveedores):
            tags = ('evenrow',) if i % 2 == 0 else ()
            self.tablaProveedores.insert('', 'end', text=p[0], values=(p[1], p[2], p[3], p[4], p[5]), tags=tags)

    def buscarProducto(self):
        texto_busqueda = self.svBuscar.get()
        if texto_busqueda:
            where = f"AND (nombre LIKE '%{texto_busqueda}%' OR tipo_proveedor LIKE '%{texto_busqueda}%' OR correo LIKE '%{texto_busqueda}%')"           
        else:
            where = ""  # Si no se proporcionó ninguna entrada, no se aplica ninguna condición WHERE
        
        # Actualizar la tabla con los resultados de la búsqueda
        self.listaProveedores = listarProveedorCondicion(where)
        self.populate_providers(self.listaProveedores)

    def editarProducto(self):
        try:
            # Obtengo los datos
            self.idProveedor                 = self.tablaProveedores.item(self.tablaProveedores.selection())['text'] #Trae el ID
            self.nombre                     = self.tablaProveedores.item(self.tablaProveedores.selection())['values'][0]
            self.tipo                       = self.tablaProveedores.item(self.tablaProveedores.selection())['values'][1]
            self.telefono                     = self.tablaProveedores.item(self.tablaProveedores.selection())['values'][2]
            self.direccion                   = self.tablaProveedores.item(self.tablaProveedores.selection())['values'][3]
            self.correo                     = self.tablaProveedores.item(self.tablaProveedores.selection())['values'][4]
            
            self.habilitarEditar()

            # Se agregan los datos obtenidos en el entry
            self.entryNombre.insert(0, self.nombre)
            self.entryTipo.insert(0, self.tipo)
            self.entryTelefono.insert(0, self.telefono)
            self.entryDireccion.insert(0, self.direccion)
            self.entryCorreo.insert(0, self.correo)
      
        except:
            title = 'Editar Producto'
            mensaje = 'Error al editar Producto'
            messagebox.showerror(title, mensaje)

    def habilitarEditar(self):
        self.svNombre.set('')
        self.svTipo.set('')
        self.svTelefono.set('')
        self.svDireccion.set('')
        self.svCorreo.set('')

        self.entryNombre.config(state='normal')
        self.entryTipo.config(state='normal')
        self.entryTelefono.config(state='normal')
        self.entryDireccion.config(state='normal')
        self.entryCorreo.config(state='normal')
 
        self.btnGuardar.config(state='normal')
        self.btnCancelar.config(state='normal')  
    
    def habilitar(self):
        self.svNombre.set('')
        self.svTipo.set('')
        self.svTelefono.set('')
        self.svDireccion.set('')
        self.svCorreo.set('')

        self.entryNombre.config(state='normal')
        self.entryTipo.config(state='normal')
        self.entryTelefono.config(state='normal')
        self.entryDireccion.config(state='normal')
        self.entryCorreo.config(state='normal')
 
        self.btnGuardar.config(state='normal')
        self.btnCancelar.config(state='normal') 

    def deshabilitar(self):
        self.svNombre.set('')
        self.svTipo.set('')
        self.svTelefono.set('')
        self.svDireccion.set('')
        self.svCorreo.set('')

        self.entryNombre.config(state='disabled')
        self.entryTipo.config(state='disabled')
        self.entryTelefono.config(state='disabled')
        self.entryDireccion.config(state='disabled')
        self.entryCorreo.config(state='disabled')
 
        self.btnGuardar.config(state='disabled')
        self.btnCancelar.config(state='disabled') 
