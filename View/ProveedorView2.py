import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from Model.ProveedorDAO import *
from Model.StockDAO import obtener_Productos_combobox

class Frame_Proveedor(tk.Frame):

    def __init__(self, root, width=1745, height=750):
        super().__init__(root, width=width, height=height)
        self.root = root
        self.config(bg='#f0f2f5')  # Color de fondo del frame principal
        self.pack(fill='both', expand=True)
        self.idProveedor = None 
        self.frameBuscar()
        self.create_table()
        self.deshabilitar()
        #self.cargar_productos()
        self.btnBuscar.config(command=self.buscarProducto)  # Asignar el método de búsqueda al botón

    def frameBuscar(self):
        self.buscar_frame = tk.Frame(self, bg='#f0f2f5')
        self.buscar_frame.pack(pady=10)

        self.svBuscar = tk.StringVar()
        self.entryBuscar = tk.Entry(self.buscar_frame, textvariable=self.svBuscar)
        self.entryBuscar.config(width=40, font=('Segoe UI', 15), bg='#ffffff')
        self.entryBuscar.grid(column=0, row=0, padx=10, pady=5)

        self.btnBuscar = tk.Button(self.buscar_frame, text='Buscar')
        self.btnBuscar.config(width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#3498db', relief='flat', cursor='hand2')
        self.btnBuscar.grid(column=1, row=0, padx=10, pady=5)

    def create_table(self, where=""):
        if hasattr(self, 'tablaProveedores'):
            self.tablaProveedores.delete(*self.tablaProveedores.get_children())

        if len(where) > 0:
            self.listaProveedores = listarProveedorCondicion(where)
        else:
            self.listaProveedores = listarProveedores()

        if not hasattr(self, 'frame_tabla'):
            self.frame_tabla = tk.Frame(self)
            self.frame_tabla.pack(fill='x', expand=False)

            self.tablaProveedores = ttk.Treeview(self.frame_tabla, height=10, columns=('ID', 'Empresa', 'Tipo', 'Teléfono', 'Dirección', 'Correo'))
            self.scrollbar = ttk.Scrollbar(self.frame_tabla, orient='vertical', command=self.tablaProveedores.yview)
            self.tablaProveedores.configure(yscroll=self.scrollbar.set)
            self.tablaProveedores.pack(side='left', fill='both', expand=True)
            self.scrollbar.pack(side='right', fill='y')

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
        if not hasattr(self, 'botones_frame'):
            self.botones_frame = tk.Frame(self, bg='#f0f2f5')
            self.botones_frame.pack(pady=10)

            self.btnNuevo = tk.Button(self.botones_frame, text='Agregar Proveedor', command=self.habilitar)
            self.btnNuevo.config(width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#27ae60', relief='flat', cursor='hand2')
            self.btnNuevo.grid(column=0, row=0, padx=10, pady=5)

            self.btnEditar = tk.Button(self.botones_frame, text='Editar Proveedor', command=self.editarProducto)
            self.btnEditar.config(width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#3498db', relief='flat', cursor='hand2')
            self.btnEditar.grid(column=1, row=0, padx=10, pady=5)

            self.btnEliminar = tk.Button(self.botones_frame, text='Eliminar Proveedor', command=self.eliminarProveedorView)
            self.btnEliminar.config(width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#c0392b', relief='flat', cursor='hand2')
            self.btnEliminar.grid(column=2, row=0, padx=10, pady=5)

        # Frame para el formulario de ingreso de proveedor
        if not hasattr(self, 'formulario_frame'):
            self.formulario_frame = tk.Frame(self, bg='#f0f2f5')
            self.formulario_frame.pack(fill='x', padx=20, pady=10)

            self.lblnombreEmpresa = tk.Label(self.formulario_frame, text='Empresa')
            self.lblnombreEmpresa.config(font=('Segoe UI', 15, 'bold'), bg='#f0f2f5')
            self.lblnombreEmpresa.grid(column=0, row=0, padx=10, pady=5, sticky='e')

            self.lblTipo = tk.Label(self.formulario_frame, text='Tipo')
            self.lblTipo.config(font=('Segoe UI', 15, 'bold'), bg='#f0f2f5')
            self.lblTipo.grid(column=0, row=1, padx=10, pady=5, sticky='e')

            self.lblTelefono = tk.Label(self.formulario_frame, text='Telefono')
            self.lblTelefono.config(font=('Segoe UI', 15, 'bold'), bg='#f0f2f5')
            self.lblTelefono.grid(column=0, row=2, padx=10, pady=5, sticky='e')

            self.lblDireccion = tk.Label(self.formulario_frame, text='Direccion')
            self.lblDireccion.config(font=('Segoe UI', 15, 'bold'), bg='#f0f2f5')
            self.lblDireccion.grid(column=0, row=3, padx=10, pady=5, sticky='e')

            self.lblCorreo = tk.Label(self.formulario_frame, text='Correo')
            self.lblCorreo.config(font=('Segoe UI', 15, 'bold'), bg='#f0f2f5')
            self.lblCorreo.grid(column=0, row=4, padx=10, pady=5, sticky='e')

            """
            self.lblProveedor = tk.Label(self.formulario_frame, text='Producto')
            self.lblProveedor.config(font=('Arial', 15, 'bold'), bg='#BBBBBB')
            self.lblProveedor.grid(column=0, row=5, padx=10, pady=5)
            """

            # Entrys
            self.svNombre = tk.StringVar()
            self.entryNombre = tk.Entry(self.formulario_frame, textvariable=self.svNombre)
            self.entryNombre.config(width=40, font=('Segoe UI', 15))
            self.entryNombre.grid(column=1, row=0, padx=10, pady=5, columnspan=2, sticky='w')

            self.svTipo = tk.StringVar()
            self.entryTipo = tk.Entry(self.formulario_frame, textvariable=self.svTipo)
            self.entryTipo.config(width=40, font=('Segoe UI', 15))
            self.entryTipo.grid(column=1, row=1, padx=10, pady=5, columnspan=2, sticky='w')

            self.svTelefono = tk.StringVar()
            self.entryTelefono = tk.Entry(self.formulario_frame, textvariable=self.svTelefono)
            self.entryTelefono.config(width=40, font=('Segoe UI', 15))
            self.entryTelefono.grid(column=1, row=2, padx=10, pady=5, columnspan=2, sticky='w')

            self.svDireccion = tk.StringVar()
            self.entryDireccion = tk.Entry(self.formulario_frame, textvariable=self.svDireccion)
            self.entryDireccion.config(width=40, font=('Segoe UI', 15))
            self.entryDireccion.grid(column=1, row=3, padx=10, pady=5, columnspan=2, sticky='w')

            self.svCorreo = tk.StringVar()
            self.entryCorreo = tk.Entry(self.formulario_frame, textvariable=self.svCorreo)
            self.entryCorreo.config(width=40, font=('Segoe UI', 15))
            self.entryCorreo.grid(column=1, row=4, padx=10, pady=5, columnspan=2, sticky='w')

            """
            self.boxProductos = ttk.Combobox(self.formulario_frame, state='readonly')
            self.boxProductos.config(width=40, font=('Arial', 12))
            self.boxProductos.grid(column=1, row=5, padx=10, pady=5, columnspan=2)
            """

            self.btnGuardar = tk.Button(self.formulario_frame, text='Guardar Nuevo', command=self.ingresar_proveedor)
            self.btnGuardar.config(width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#27ae60', relief='flat', cursor='hand2')
            self.btnGuardar.grid(column=1, row=6, padx=10, pady=5)

            self.btnCancelar = tk.Button(self.formulario_frame, text='Cancelar', command=self.deshabilitar)
            self.btnCancelar.config(width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#c0392b', relief='flat', cursor='hand2')
            self.btnCancelar.grid(column=2, row=6, padx=10, pady=5)
    
    def eliminarProveedorView(self):
        try:
            self.idProveedor = self.tablaProveedores.item(self.tablaProveedores.selection())['text']
            eliminarProveedor(self.idProveedor)
            
            self.create_table()

        except:
            title = 'Eliminar Proveedor'
            mensaje = 'No se pudo eliminar Proveedor'
            messagebox.showinfo(title, mensaje)


    def cargar_productos(self):
        try:
            lista_productos = obtener_Productos_combobox()  # Obtener los proveedores
            self.boxProductos['values'] = lista_productos  # Asignar la lista de nombres de proveedores al Combobox
            if lista_productos:
                self.boxProductos.current(0)  # Establecer la selección inicial, si hay proveedores cargados
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar los proveedores: {e}")
    
    def ingresar_proveedor(self): 
        #producto_seleccionado = self.boxProductos.get()
        producto_seleccionado = None
        proveedor = Proveedor(self.svNombre.get(), self.svTipo.get(), self.svTelefono.get(), self.svDireccion.get(), self.svCorreo.get())

        try:
            if self.idProveedor == None:
                agregarProveedorOnly(proveedor,producto_seleccionado)
            else:
                editarProveedorOnly(proveedor,self.idProveedor, producto_seleccionado)
        except:
            title = 'Agregar Proveedor'
            mensaje = 'Error al agregar Proveedor'
            messagebox.showerror(title, mensaje)

        self.create_table()
        self.deshabilitar()


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
