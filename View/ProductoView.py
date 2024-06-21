import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import *
from datetime import datetime
from Model.ProductoDAO import *
from Model.ProveedorDAO import obtener_Proveedores_combobox

class Frame_Producto(tk.Frame):

    def __init__(self, root, width=1280, height=720):
        super().__init__(root, width=width, height=height)
        self.root = root
        self.config(bg='#f0f0f0')  # Color de fondo del frame principal
        self.pack(fill='both', expand=True)
        self.idProducto = None
        self.idProductoProveedor = None
        self.tablaProductos()
        self.deshabilitar()
        self.cargar_proveedores()
        self.frameBuscar()
        self.btnBuscar.config(command=self.buscarProducto)  # Asignar el método de búsqueda al botón

    def frameBuscar(self):
        self.buscar_frame = tk.Frame(self, bg='#f0f0f0')
        self.buscar_frame.grid(row=9, column=0, columnspan=15, sticky='nsew', pady=10)

        self.svBuscar = tk.StringVar()
        self.entryBuscar = tk.Entry(self.buscar_frame, textvariable=self.svBuscar)
        self.entryBuscar.config(width=40, font=('Arial', 15), bg='#ffffff')
        self.entryBuscar.grid(column=0, row=0, padx=10, pady=5)

        self.btnBuscar = tk.Button(self.buscar_frame, text='Buscar')
        self.btnBuscar.config(width=20, font=('Arial', 12, 'bold'), fg='#ffffff', bg='#007ACC')
        self.btnBuscar.grid(column=1, row=0, padx=10, pady=5)


    def tablaProductos(self, where=""):
        if len(where) > 0:
            self.listaProductos = listarCondiciones(where)
        else:
            self.listaProductos = listarProductos()

        # Frame para la tabla y la barra de desplazamiento
        frame_tabla = tk.Frame(self)
        frame_tabla.grid(column=0, row=10, columnspan=15, sticky='nsew')

        # Crear la tabla con barra de desplazamiento
        self.tabla = ttk.Treeview(frame_tabla, columns=('idProducto', 'Codigo', 'Producto', 'Tipo', 'Cant. ingresada', 'Precio', 'Fecha de Ingreso', 'Proveedor'))
        scrollbar = ttk.Scrollbar(frame_tabla, orient='vertical', command=self.tabla.yview)
        self.tabla.configure(yscroll=scrollbar.set)
        self.tabla.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.tabla.heading('#0', text='ID')
        self.tabla.heading('#1', text='Codigo')
        self.tabla.heading('#2', text='Producto')
        self.tabla.heading('#3', text='Tipo')
        self.tabla.heading('#4', text='Cant. ingresada')
        self.tabla.heading('#5', text='Precio')
        self.tabla.heading('#6', text='Fecha de Ingreso')
        self.tabla.heading('#7', text='Proveedor')

        self.tabla.column("#0", anchor='w', width=100)
        self.tabla.column("#1", anchor='w', width=130)
        self.tabla.column("#2", anchor='w', width=180)
        self.tabla.column("#3", anchor='w', width=150)
        self.tabla.column("#4", anchor='w', width=150)
        self.tabla.column("#5", anchor='w', width=120)
        self.tabla.column("#6", anchor='w', width=180)
        self.tabla.column("#7", anchor='w', width=170)

        for p in self.listaProductos:
            precio_formateado = "{:,.2f}".format(p[5])  # Asumiendo que p[5] es el precio
            self.tabla.insert('', 'end', text=p[0], values=(p[1], p[2], p[3], p[4], precio_formateado, p[6], p[7]), tags=('evenrow',))

        # Botones debajo de la tabla
        self.botones_frame = tk.Frame(self, bg='#f0f0f0')
        self.botones_frame.grid(column=0, row=11, columnspan=15, sticky='nsew')  # Usar grid en lugar de pack

        self.btnNuevo = tk.Button(self.botones_frame, text='Registrar entrada', command=self.habilitar)
        self.btnNuevo.config(width=20, font=('Arial', 12, 'bold'), fg='#ffffff', bg='#5CB85C')
        self.btnNuevo.grid(column=0, row=0, padx=10, pady=5)

        self.btnEditar = tk.Button(self.botones_frame, text='Editar Registro', command=self.editarProducto)
        self.btnEditar.config(width=20, font=('Arial', 12, 'bold'), fg='#ffffff', bg='#007ACC')
        self.btnEditar.grid(column=1, row=0, padx=10, pady=5)

        self.btnEliminar = tk.Button(self.botones_frame, text='Eliminar Registro', command=self.eliminarProductoView)
        self.btnEliminar.config(width=20, font=('Arial', 12, 'bold'), fg='#ffffff', bg='#D9534F')
        self.btnEliminar.grid(column=3, row=0, padx=10, pady=5)

        # Frame para el formulario de ingreso de producto
        self.formulario_frame = tk.Frame(self, bg='#BBBBBB')
        self.formulario_frame.grid(column=0, row=12, columnspan=15, sticky='nsew')  # Usar grid en lugar de pack

        # LABELS
        self.lblcodigo = tk.Label(self.formulario_frame, text='Codigo')
        self.lblcodigo.config(font=('Arial', 15, 'bold'), bg='#BBBBBB')
        self.lblcodigo.grid(column=0, row=0, padx=10, pady=5)

        self.lblcantidad = tk.Label(self.formulario_frame, text='Cant de ingreso en Kg')
        self.lblcantidad.config(font=('Arial', 15, 'bold'), bg='#BBBBBB')
        self.lblcantidad.grid(column=0, row=1, padx=10, pady=5)

        self.lblprecio = tk.Label(self.formulario_frame, text='Precio por Kg')
        self.lblprecio.config(font=('Arial', 15, 'bold'), bg='#BBBBBB')
        self.lblprecio.grid(column=0, row=2, padx=10, pady=5)

        self.lblfecha = tk.Label(self.formulario_frame, text='Fecha')
        self.lblfecha.config(font=('Arial', 15, 'bold'), bg='#BBBBBB')
        self.lblfecha.grid(column=0, row=3, padx=10, pady=5)

        self.lblProveedor = tk.Label(self.formulario_frame, text='Proveedor')
        self.lblProveedor.config(font=('Arial', 15, 'bold'), bg='#BBBBBB')
        self.lblProveedor.grid(column=0, row=4, padx=10, pady=5)

        # Entrys
        self.svCodigo = tk.StringVar()
        self.entryCodigo = tk.Entry(self.formulario_frame, textvariable=self.svCodigo)
        self.entryCodigo.config(width=40, font=('Arial', 15))
        self.entryCodigo.grid(column=1, row=0, padx=10, pady=5, columnspan=2)

        self.svCantidad = tk.StringVar()
        self.entryCantidad = tk.Entry(self.formulario_frame, textvariable=self.svCantidad)
        self.entryCantidad.config(width=40, font=('Arial', 15))
        self.entryCantidad.grid(column=1, row=1, padx=10, pady=5, columnspan=2)

        self.svPrecio = tk.StringVar()
        self.entryPrecio = tk.Entry(self.formulario_frame, textvariable=self.svPrecio)
        self.entryPrecio.config(width=40, font=('Arial', 15))
        self.entryPrecio.grid(column=1, row=2, padx=10, pady=5, columnspan=2)

        self.svFecha = tk.StringVar()
        self.entryFecha = tk.Entry(self.formulario_frame, textvariable=self.svFecha)
        self.entryFecha.config(width=40, font=('Arial', 15))
        self.entryFecha.grid(column=1, row=3, padx=10, pady=5, columnspan=2)

        self.proveedores = ttk.Combobox(self.formulario_frame, state='readonly')
        self.proveedores.config(width=40, font=('Arial', 12))
        self.proveedores.grid(column=1, row=4, padx=10, pady=5, columnspan=2)

        # Botones
        self.btnGuardar = tk.Button(self.formulario_frame, text='Guardar', command=self.ingresarProducto)
        self.btnGuardar.config(width=20, font=('Arial', 12, 'bold'), fg='#ffffff', bg='#5CB85C')
        self.btnGuardar.grid(column=1, row=5, padx=10, pady=5)

        self.btnCancelar = tk.Button(self.formulario_frame, text='Cancelar', command=self.deshabilitar)
        self.btnCancelar.config(width=20, font=('Arial', 12, 'bold'), fg='#ffffff', bg='#D9534F')
        self.btnCancelar.grid(column=2, row=5, padx=10, pady=5)

    def cargar_proveedores(self):
        try:
            lista_proveedores = obtener_Proveedores_combobox()  # Obtener los proveedores
            self.proveedores['values'] = lista_proveedores  # Asignar la lista de nombres de proveedores al Combobox
            if lista_proveedores:
                self.proveedores.current(0)  # Establecer la selección inicial, si hay proveedores cargados
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar los proveedores: {e}")


    def buscarProducto(self):
        texto_busqueda = self.svBuscar.get()
        if texto_busqueda:
            where = f"AND (p.codigo LIKE '%{texto_busqueda}%' OR ps.tipo LIKE '%{texto_busqueda}%' OR ps.nombre LIKE '%{texto_busqueda}%')"
        else:
            where = ""  # Si no se proporcionó ninguna entrada, no se aplica ninguna condición WHERE
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


    def ingresarProducto(self):
        # Obtener el proveedor seleccionado
        proveedor_seleccionado = self.proveedores.get()

        producto = Producto(self.svCodigo.get(), self.svCantidad.get(), self.svPrecio.get(), self.svFecha.get())

        if self.idProducto == None:
            # Guardar el producto usando el proveedor seleccionado
            guardarProducto(producto, proveedor_seleccionado)
            idStock = obtener_id_por_producto(self.svCodigo.get())
            self.actualizar_baseDatos(idStock, self.svCantidad.get())
        else:
            editarProducto(producto, self.idProducto, proveedor_seleccionado)

        self.deshabilitar()  # Después de guardar, deshabilitar los campos
        self.tablaProductos()  # Actualizar la tabla de productos


    def actualizar_baseDatos(self, idProducto, cantidad):
        actualizar_stock_db(idProducto, cantidad)

    def editarProducto(self):
        try:
            # Obtengo los datos
            self.idProducto                 = self.tabla.item(self.tabla.selection())['text'] #Trae el ID
            self.codigo                     = self.tabla.item(self.tabla.selection())['values'][0]
            self.Cantidad                   = self.tabla.item(self.tabla.selection())['values'][3]
            self.precio                     = self.tabla.item(self.tabla.selection())['values'][4]
            self.fecha                      = self.tabla.item(self.tabla.selection())['values'][5]
            self.proveedor                  = self.tabla.item(self.tabla.selection())['values'][6]
            
            self.habilitarEditar()

            # Se agregan los datos obtenidos en el entry
            self.entryCodigo.insert(0, self.codigo)
            self.entryCantidad.insert(0, self.Cantidad)
            self.entryPrecio.insert(0, self.precio)
            self.entryFecha.insert(0, self.fecha)
            self.proveedores.insert(0, self.proveedor)
      
        except:
            title = 'Editar Producto'
            mensaje = 'Error al editar Producto'
            messagebox.showerror(title, mensaje)

    def habilitarEditar(self):
        self.svCodigo.set('')
        self.svCantidad.set('')
        self.svPrecio.set('')
        self.svFecha.set('')

        self.entryCodigo.config(state='normal')
        self.entryCantidad.config(state='normal')
        self.entryPrecio.config(state='normal')
        self.entryFecha.config(state='normal')
        self.proveedores.config(state='readonly')

        self.btnGuardar.config(state='normal')
        self.btnCancelar.config(state='normal') 
    
    def habilitar(self):
        self.svCodigo.set('')
        self.svCantidad.set('')
        self.svPrecio.set('')
        self.svFecha.set('')

        # Asignar la fecha actual al entry de fecha
        fecha_actual = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        self.svFecha.set(fecha_actual)

        self.entryCodigo.config(state='normal')
        self.entryCantidad.config(state='normal')
        self.entryPrecio.config(state='normal')
        self.entryFecha.config(state='normal')
        self.proveedores.config(state='readonly')

        self.btnGuardar.config(state='normal')
        self.btnCancelar.config(state='normal') 

    def deshabilitar(self):
        self.idProducto = None
        self.svCodigo.set('')
        self.svCantidad.set('')
        self.svPrecio.set('')
        self.svFecha.set('')

        self.entryCodigo.config(state='disabled')
        self.entryCantidad.config(state='disabled')
        self.entryPrecio.config(state='disabled')
        self.entryFecha.config(state='disabled')
        self.proveedores.config(state='disabled')

        self.btnGuardar.config(state='disabled')
        self.btnCancelar.config(state='disabled') 
