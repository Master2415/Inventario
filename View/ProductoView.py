import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import *
from datetime import datetime
from Model.ProductoDAO import *
from Model.ProveedorDAO import *
from View.ProveedorView import *

class Frame_Producto(tk.Frame):

    def __init__(self, root, width=1280, height=720):
        super().__init__(root, width=width, height=height)
        self.root = root
        self.config(bg='#BBBBBB')  # Establecer el color de fondo del frame principal
        self.pack(fill='both', expand=True)
        self.idProducto = None # Usado para acceder a los metodos
        self.idProductoProveedor = None
        self.lebels_Entrys()
        self.tablaProductos()
        self.deshabilitar()
        

    def lebels_Entrys(self):
        #LABELS
        self.lblcodigo = tk.Label(self, text='Codigo')
        self.lblcodigo.config(font=('ARIAl',15,'bold'), bg='#BBBBBB')
        self.lblcodigo.grid(column=0, row=0, padx=10, pady=5)

        self.lblNombre = tk.Label(self, text='Nombre')
        self.lblNombre.config(font=('ARIAl',15,'bold'), bg='#BBBBBB')
        self.lblNombre.grid(column=0, row=1, padx=10, pady=5)

        self.lbltipo = tk.Label(self, text='Tipo')
        self.lbltipo.config(font=('ARIAl',15,'bold'), bg='#BBBBBB')
        self.lbltipo.grid(column=0, row=2, padx=10, pady=5)

        self.lblcantidad = tk.Label(self, text='Cant de ingreso en Kg')
        self.lblcantidad.config(font=('ARIAl',15,'bold'), bg='#BBBBBB')
        self.lblcantidad.grid(column=0, row=3, padx=10, pady=5)

        self.lblprecio = tk.Label(self, text='Precio')
        self.lblprecio.config(font=('ARIAl',15,'bold'), bg='#BBBBBB')
        self.lblprecio.grid(column=0, row=4, padx=10, pady=5)

        self.lblfecha = tk.Label(self, text='Fecha')
        self.lblfecha.config(font=('ARIAl',15,'bold'), bg='#BBBBBB')
        self.lblfecha.grid(column=0, row=5, padx=10, pady=5)

        # Entrys
        self.svCodigo = tk.StringVar()
        self.entryCodigo = tk.Entry(self, textvariable=self.svCodigo)
        self.entryCodigo.config(width=40, font=('ARIAL',15))
        self.entryCodigo.grid(column=1, row=0, padx=10, pady=5, columnspan=2)

        self.svNombre = tk.StringVar()
        self.entryNombre = tk.Entry(self, textvariable=self.svNombre)
        self.entryNombre.config(width=40, font=('ARIAL',15))
        self.entryNombre.grid(column=1, row=1, padx=10, pady=5, columnspan=2)

        self.svTipo = tk.StringVar()
        self.entryTipo = tk.Entry(self, textvariable=self.svTipo)
        self.entryTipo.config(width=40, font=('ARIAL',15))
        self.entryTipo.grid(column=1, row=2, padx=10, pady=5, columnspan=2)

        self.svCantidad = tk.StringVar()
        self.entryCantidad = tk.Entry(self, textvariable=self.svCantidad)
        self.entryCantidad.config(width=40, font=('ARIAL',15))
        self.entryCantidad.grid(column=1, row=3, padx=10, pady=5, columnspan=2)

        self.svPrecio = tk.StringVar()
        self.entryPrecio = tk.Entry(self, textvariable=self.svPrecio)
        self.entryPrecio.config(width=40, font=('ARIAL',15))
        self.entryPrecio.grid(column=1, row=4, padx=10, pady=5, columnspan=2)

        self.svFecha = tk.StringVar()
        self.entryFecha = tk.Entry(self, textvariable=self.svFecha)
        self.entryFecha.config(width=40, font=('ARIAL',15))
        self.entryFecha.grid(column=1, row=5, padx=10, pady=5, columnspan=2)

        self.svBuscar = tk.StringVar()
        self.entryBuscar = tk.Entry(self, textvariable=self.svBuscar)
        self.entryBuscar.config(width=40, font=('ARIAL',15))
        self.entryBuscar.grid(column=1, row=6, padx=10, pady=5, columnspan=2)

        #Botones
        self.btnNuevo = tk.Button(self, text='Nuevo Producto', command=self.habilitar)
        self.btnNuevo.config(width=20, font=('ARIAL',12,'bold'), fg='#DAD5D6', bg='#158645')
        self.btnNuevo.grid(column=3, row=0, padx=10, pady=5)

        self.btnGuardar = tk.Button(self, text='Guardar Nuevo', command=self.ingresarProducto)
        self.btnGuardar.config(width=20, font=('ARIAL',12,'bold'), fg='#DAD5D6', bg='#158645')
        self.btnGuardar.grid(column=3, row=1, padx=10, pady=5)

        self.btnEditar = tk.Button(self, text='Editar Producto', command=self.editarProducto)
        self.btnEditar.config(width=20, font=('ARIAL',12,'bold'), fg='#DAD5D6', bg='#158645')
        self.btnEditar.grid(column=3, row=4, padx=10, pady=5)

        self.btnCancelar = tk.Button(self, text='Cancelar Nuevo', command=self.deshabilitar)
        self.btnCancelar.config(width=20, font=('ARIAL',12,'bold'), fg='#DAD5D6', bg='#CF0000')
        self.btnCancelar.grid(column=3, row=2, padx=10, pady=5)

        self.btnEliminar = tk.Button(self, text='Eliminar Produto', command=self.eliminarProductoView)
        self.btnEliminar.config(width=20, font=('ARIAL',12,'bold'), fg='#DAD5D6', bg='#CF0000')
        self.btnEliminar.grid(column=3, row=12, padx=10, pady=5)

        self.btnProveedor = tk.Button(self, text='Proveedor',command=self.ver_proveedor)
        self.btnProveedor.config(width=20, font=('ARIAL',12,'bold'), fg='#DAD5D6', bg='#CF0000')
        self.btnProveedor.grid(column=3, row=5, padx=10, pady=5)

        self.btnBuscar = tk.Button(self, text='Buscar', command=self.buscarProducto)
        self.btnBuscar.config(width=20, font=('ARIAL',12,'bold'), fg='#DAD5D6', bg='#001CCF')
        self.btnBuscar.grid(column=3, row=6, padx=10, pady=5)

    def ver_proveedor(self):
        self.idProducto = self.get_selected_product_id()
        if self.idProducto:
            ProveedorView(self, self.idProducto)
        else:
            messagebox.showerror("Error", "Seleccione un producto")

    def get_selected_product_id(self):
        selected_item = self.tabla.selection()
        if selected_item:
            return self.tabla.item(selected_item)['text']
        else:
            return None

    def buscarProducto(self):
        # Obtener el texto del Entry
        texto_busqueda = self.svBuscar.get()

        # Verificar si se proporcionó algún texto de búsqueda
        if texto_busqueda:
            # Crear la condición WHERE
            where = "WHERE codigo LIKE '%" + texto_busqueda + "%' OR tipoProducto LIKE '%" + texto_busqueda + "%' OR nombre LIKE '%" + texto_busqueda + "%'"
        else:
            where = ""  # Si no se proporcionó ninguna entrada, no se aplica ninguna condición WHERE

        # Llamar a la función para obtener los productos con las condiciones dadas
        self.tablaProductos(where)


    def eliminarProductoView(self):
        try:
            self.idProducto = self.tabla.item(self.tabla.selection())['text']
            eliminarProducto(self.idProducto)
            
            self.tablaProductos()

        except:
            title = 'Eliminar Producto'
            mensaje = 'No se pudo eliminar Producto'
            messagebox.showinfo(title, mensaje)


    def deshabilitar(self):
        self.idProducto = None
        self.svCodigo.set('')
        self.svTipo.set('')
        self.svNombre.set('')
        self.svCantidad.set('')
        self.svPrecio.set('')
        self.svFecha.set('')

        self.entryCodigo.config(state='disabled')
        self.entryTipo.config(state='disabled')
        self.entryNombre.config(state='disabled')
        self.entryCantidad.config(state='disabled')
        self.entryPrecio.config(state='disabled')
        self.entryFecha.config(state='disabled')

        self.btnGuardar.config(state='disabled')
        self.btnCancelar.config(state='disabled') 

    def ingresarProducto(self):
        producto = Producto(self.svCodigo.get(), self.svTipo.get(), self.svNombre.get(), self.svCantidad.get(), self.svPrecio.get(), self.svFecha.get())

        if self.idProducto == None:
            guardarProducto(producto)
        else:
            editarProducto(producto, self.idProducto)

        self.deshabilitar() # Luego de guardar se desactivan los entrys, obligando al usuario a dar click en nuevo
        self.tablaProductos() # Se refresca la tabla de los productos

    def editarProducto(self):
        try:
            # Obtengo los datos
            self.idProducto                 = self.tabla.item(self.tabla.selection())['text'] #Trae el ID
            self.codigo                     = self.tabla.item(self.tabla.selection())['values'][0]
            self.tipo                       = self.tabla.item(self.tabla.selection())['values'][1]
            self.Nombre                     = self.tabla.item(self.tabla.selection())['values'][2]
            self.Cantidad                   = self.tabla.item(self.tabla.selection())['values'][3]
            self.precio                     = self.tabla.item(self.tabla.selection())['values'][4]
            self.fecha                      = self.tabla.item(self.tabla.selection())['values'][5]
            
            self.habilitarEditar()

            # Se agregan los datos obtenidos en el entry
            self.entryCodigo.insert(0, self.codigo)
            self.entryTipo.insert(0, self.tipo)
            self.entryNombre.insert(0, self.Nombre)
            self.entryCantidad.insert(0, self.Cantidad)
            self.entryPrecio.insert(0, self.precio)
            self.entryFecha.insert(0, self.fecha)
      
        except:
            title = 'Editar Producto'
            mensaje = 'Error al editar Producto'
            messagebox.showerror(title, mensaje)

    def habilitarEditar(self):
        self.svCodigo.set('')
        self.svTipo.set('')
        self.svNombre.set('')
        self.svCantidad.set('')
        self.svPrecio.set('')
        self.svFecha.set('')

        self.entryCodigo.config(state='normal')
        self.entryTipo.config(state='normal')
        self.entryNombre.config(state='normal')
        self.entryCantidad.config(state='normal')
        self.entryPrecio.config(state='normal')
        self.entryFecha.config(state='normal')

        self.btnGuardar.config(state='normal')
        self.btnCancelar.config(state='normal') 
    
    def habilitar(self):
        self.svCodigo.set('')
        self.svTipo.set('')
        self.svNombre.set('')
        self.svCantidad.set('')
        self.svPrecio.set('')
        self.svFecha.set('')

        # Asignar la fecha actual al entry de fecha
        fecha_actual = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        self.svFecha.set(fecha_actual)

        self.entryCodigo.config(state='normal')
        self.entryTipo.config(state='normal')
        self.entryNombre.config(state='normal')
        self.entryCantidad.config(state='normal')
        self.entryPrecio.config(state='normal')
        self.entryFecha.config(state='normal')

        self.btnGuardar.config(state='normal')
        self.btnCancelar.config(state='normal') 


    def tablaProductos(self,  where=""):

        if len(where) > 0:
            self.listaProductos = listarCondiciones(where)
        else:
            self.listaProductos = listarProductos()

        # Frame para la tabla y la barra de desplazamiento
        frame_tabla = tk.Frame(self)
        frame_tabla.grid(column=0, row=10, columnspan=15, sticky='nsew')

        # Crear la tabla con barra de desplazamiento
        self.tabla = ttk.Treeview(frame_tabla, columns=('idProducto', 'Codigo', 'Tipo', 'Nombre', 'Cantidad disponible', 'Precio', 'Fecha de Ingreso'))
        scrollbar = ttk.Scrollbar(frame_tabla, orient='vertical', command=self.tabla.yview)
        self.tabla.configure(yscroll=scrollbar.set)
        self.tabla.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.tabla.heading('#0', text='ID')
        self.tabla.heading('#1', text='Codigo')
        self.tabla.heading('#2', text='Tipo')
        self.tabla.heading('#3', text='Nombre')
        self.tabla.heading('#4', text='Cant. ingresada')
        self.tabla.heading('#5', text='Precio')
        self.tabla.heading('#6', text='Fecha de Ingreso')

        self.tabla.column("#0", anchor='w', width=100)
        self.tabla.column("#1", anchor='w', width=130)
        self.tabla.column("#2", anchor='w', width=150)
        self.tabla.column("#3", anchor='w', width=180)
        self.tabla.column("#4", anchor='w', width=120)
        self.tabla.column("#5", anchor='w', width=120)
        self.tabla.column("#6", anchor='w', width=170)

        for p in self.listaProductos:
            self.tabla.insert('', 'end', text=p[0], values=(p[1], p[2], p[3], p[4], p[5], p[6]), tags=('evenrow',))
