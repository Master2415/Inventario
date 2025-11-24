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
        self.config(bg='#f0f2f5')  # Color de fondo del frame principal
        self.pack(fill='both', expand=True)
        self.idProducto = None
        self.idProductoProveedor = None
        self.frameBuscar()
        self.tablaProductos()
        self.cargar_proveedores()
        self.deshabilitar()
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


    def tablaProductos(self, where=""):
        # Eliminar los elementos existentes de la tabla si ya existe
        if hasattr(self, 'tablaProducto'):
            self.tablaProducto.delete(*self.tablaProducto.get_children())
        else:
            # Si la tabla no existe, crearla junto con su frame y scrollbar
            self.frame_tablaProducto = tk.Frame(self)
            self.frame_tablaProducto.pack(fill='x', expand=False)

            # Crear la tablaProducto con barra de desplazamiento
            self.tablaProducto = ttk.Treeview(self.frame_tablaProducto, height=10, columns=('idProducto', 'Codigo', 'Producto', 'Tipo', 'Cant. ingresada', 'Precio', 'Fecha de Ingreso', 'Proveedor'))
            self.scrollbar = ttk.Scrollbar(self.frame_tablaProducto, orient='vertical', command=self.tablaProducto.yview)
            self.tablaProducto.configure(yscroll=self.scrollbar.set)
            self.tablaProducto.pack(side='left', fill='both', expand=True)
            self.scrollbar.pack(side='right', fill='y')

            self.tablaProducto.heading('#0', text='ID')
            self.tablaProducto.heading('#1', text='Codigo')
            self.tablaProducto.heading('#2', text='Producto')
            self.tablaProducto.heading('#3', text='Tipo')
            self.tablaProducto.heading('#4', text='Cant. ingresada')
            self.tablaProducto.heading('#5', text='Precio')
            self.tablaProducto.heading('#6', text='Fecha de Ingreso')
            self.tablaProducto.heading('#7', text='Proveedor')

            self.tablaProducto.column("#0", anchor='w', width=100)
            self.tablaProducto.column("#1", anchor='w', width=130)
            self.tablaProducto.column("#2", anchor='w', width=180)
            self.tablaProducto.column("#3", anchor='w', width=150)
            self.tablaProducto.column("#4", anchor='w', width=150)
            self.tablaProducto.column("#5", anchor='w', width=120)
            self.tablaProducto.column("#6", anchor='w', width=180)
            self.tablaProducto.column("#7", anchor='w', width=170)

        # Consultar y rellenar la tabla con los nuevos datos
        if len(where) > 0:
            self.listaProductos = listarCondiciones(where)
        else:
            self.listaProductos = listarProductos()

        for p in self.listaProductos:
            precio_formateado = "{:,.2f}".format(p[5])  # Asumiendo que p[5] es el precio
            self.tablaProducto.insert('', 'end', text=p[0], values=(p[1], p[2], p[3], p[4], precio_formateado, p[6], p[7]), tags=('evenrow',))


        if not hasattr(self, 'botones_frame'):
            self.botones_frame = tk.Frame(self, bg='#f0f2f5')
            self.botones_frame.pack(pady=10)

            self.btnNuevo = tk.Button(self.botones_frame, text='Agregar Producto', command=self.habilitar)
            self.btnNuevo.config(width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#27ae60', relief='flat', cursor='hand2')
            self.btnNuevo.grid(column=0, row=0, padx=10, pady=5)

            self.btnEditar = tk.Button(self.botones_frame, text='Editar Producto', command=self.editarProducto)
            self.btnEditar.config(width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#3498db', relief='flat', cursor='hand2')
            self.btnEditar.grid(column=1, row=0, padx=10, pady=5)

            self.btnEliminar = tk.Button(self.botones_frame, text='Eliminar Producto', command=self.eliminarProductoView)
            self.btnEliminar.config(width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#c0392b', relief='flat', cursor='hand2')
            self.btnEliminar.grid(column=2, row=0, padx=10, pady=5)


        # Frame para el formulario de ingreso de producto
        if not hasattr(self, 'formulario_frame'):
            self.formulario_frame = tk.Frame(self, bg='#f0f2f5')
            self.formulario_frame.pack(fill='x', padx=20, pady=10)

            # LABELS
            self.lblcodigo = tk.Label(self.formulario_frame, text='Codigo')
            self.lblcodigo.config(font=('Segoe UI', 15, 'bold'), bg='#f0f2f5')
            self.lblcodigo.grid(column=0, row=0, padx=10, pady=5)

            self.lblcantidad = tk.Label(self.formulario_frame, text='Cant de ingreso en Kg')
            self.lblcantidad.config(font=('Segoe UI', 15, 'bold'), bg='#f0f2f5')
            self.lblcantidad.grid(column=0, row=1, padx=10, pady=5)

            self.lblprecio = tk.Label(self.formulario_frame, text='Precio por Kg')
            self.lblprecio.config(font=('Segoe UI', 15, 'bold'), bg='#f0f2f5')
            self.lblprecio.grid(column=0, row=2, padx=10, pady=5)

            self.lblfecha = tk.Label(self.formulario_frame, text='Fecha')
            self.lblfecha.config(font=('Segoe UI', 15, 'bold'), bg='#f0f2f5')
            self.lblfecha.grid(column=0, row=3, padx=10, pady=5)

            self.lblProveedor = tk.Label(self.formulario_frame, text='Proveedor')
            self.lblProveedor.config(font=('Segoe UI', 15, 'bold'), bg='#f0f2f5')
            self.lblProveedor.grid(column=0, row=4, padx=10, pady=5)

            # Entrys
            self.svCodigo = tk.StringVar()
            self.entryCodigo = tk.Entry(self.formulario_frame, textvariable=self.svCodigo)
            self.entryCodigo.config(width=40, font=('Segoe UI', 15))
            self.entryCodigo.grid(column=1, row=0, padx=10, pady=5, columnspan=2)

            self.svCantidad = tk.StringVar()
            self.entryCantidad = tk.Entry(self.formulario_frame, textvariable=self.svCantidad)
            self.entryCantidad.config(width=40, font=('Segoe UI', 15))
            self.entryCantidad.grid(column=1, row=1, padx=10, pady=5, columnspan=2)

            self.svPrecio = tk.StringVar()
            self.entryPrecio = tk.Entry(self.formulario_frame, textvariable=self.svPrecio)
            self.entryPrecio.config(width=40, font=('Segoe UI', 15))
            self.entryPrecio.grid(column=1, row=2, padx=10, pady=5, columnspan=2)

            self.svFecha = tk.StringVar()
            self.entryFecha = tk.Entry(self.formulario_frame, textvariable=self.svFecha)
            self.entryFecha.config(width=40, font=('Segoe UI', 15))
            self.entryFecha.grid(column=1, row=3, padx=10, pady=5, columnspan=2)

            self.proveedores = ttk.Combobox(self.formulario_frame, state='readonly')
            self.proveedores.config(width=40, font=('Segoe UI', 12))
            self.proveedores.grid(column=1, row=4, padx=10, pady=5, columnspan=2)

            # Botones
            self.btnGuardar = tk.Button(self.formulario_frame, text='Guardar', command=self.ingresarProducto)
            self.btnGuardar.config(width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#27ae60', relief='flat', cursor='hand2')
            self.btnGuardar.grid(column=1, row=5, padx=10, pady=5)

            self.btnCancelar = tk.Button(self.formulario_frame, text='Cancelar', command=self.deshabilitar)
            self.btnCancelar.config(width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#c0392b', relief='flat', cursor='hand2')
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
            where = f"p.codigo LIKE '%{texto_busqueda}%' OR ps.tipo LIKE '%{texto_busqueda}%' OR ps.nombre LIKE '%{texto_busqueda}%'"
        else:
            where = ""  # Si no se proporcionó ninguna entrada, no se aplica ninguna condición WHERE
        self.tablaProductos(where)


    def eliminarProductoView(self):
        try:
            self.idProducto = self.tablaProducto.item(self.tablaProducto.selection())['text']
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
        self.tablaProductos()  # Actualizar la tablaProducto de productos


    def actualizar_baseDatos(self, idProducto, cantidad):
        actualizar_stock_db(idProducto, cantidad)

    def editarProducto(self):
        try:
            # Obtengo los datos
            self.idProducto                 = self.tablaProducto.item(self.tablaProducto.selection())['text'] #Trae el ID
            self.codigo                     = self.tablaProducto.item(self.tablaProducto.selection())['values'][0]
            self.Cantidad                   = self.tablaProducto.item(self.tablaProducto.selection())['values'][3]
            self.precio                     = self.tablaProducto.item(self.tablaProducto.selection())['values'][4]
            self.fecha                      = self.tablaProducto.item(self.tablaProducto.selection())['values'][5]
            self.proveedor                  = self.tablaProducto.item(self.tablaProducto.selection())['values'][6]
            
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
