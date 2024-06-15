import tkinter as tk
from tkinter import ttk
from Model.ProductoDAO import *  # Asumiendo que listarProductos1 y actualizarStock están definidos en ProductoDAO
from Model.VentaDAO import listarVentas  # Asumiendo que listarVentas está definido en VentaDAO


class Frame_Venta(tk.Frame):
    def __init__(self, root, width=1450, height=720):
        super().__init__(root, width=width, height=height)
        self.root = root
        self.config(bg='#BBBBBB')  # Establecer el color de fondo del frame principal
        self.pack(fill='both', expand=True)
        self.idVenta = None  # Usado para acceder a los métodos
        self.idProducto = None
        self.botones()

        # Llamadas a los métodos para configurar las tablas
        self.cargarTablaProductos()
        self.cargarTablaVentas()

        # Llamada a la función para configurar el carrito y los controles asociados
        self.configurar_carrito()

    def botones(self):
        self.svBuscar = tk.StringVar()
        self.entryBuscar = tk.Entry(self, textvariable=self.svBuscar)
        self.entryBuscar.config(width=35, font=('ARIAL', 15))
        self.entryBuscar.grid(column=2, row=0, padx=10, pady=5, columnspan=2)

        self.btnBuscar = tk.Button(self, text='Buscar', command=self.buscarProducto)
        self.btnBuscar.config(width=20, font=('ARIAL', 12, 'bold'), fg='#DAD5D6', bg='#001CCF')
        self.btnBuscar.grid(column=4, row=0, padx=10, pady=5)

    def cargarTablaProductos(self, where=""):
        if len(where) > 0:
            self.listaProductos = listarCondiciones1(where)
        else:
            self.listaProductos = listarProductos1()

        # Frame para la tabla y la barra de desplazamiento
        frame_tablaProductos = tk.Frame(self)
        frame_tablaProductos.grid(column=2, row=1, columnspan=6, sticky='nsew', padx=10, pady=10)

        # Título de la tabla de productos
        label_productos = tk.Label(frame_tablaProductos, text="Productos", font=('Arial', 16, 'bold'), bg='#BBBBBB')
        label_productos.pack(side='top')

        # Crear la tabla con barra de desplazamiento
        self.tablaProductos = ttk.Treeview(frame_tablaProductos, columns=('Codigo', 'Nombre', 'Precio', 'Stock'), show='headings')
        scrollbar = ttk.Scrollbar(frame_tablaProductos, orient='vertical', command=self.tablaProductos.yview)
        self.tablaProductos.configure(yscroll=scrollbar.set)
        self.tablaProductos.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.tablaProductos.heading('Codigo', text='Codigo', anchor='w')
        self.tablaProductos.heading('Nombre', text='Nombre', anchor='w')
        self.tablaProductos.heading('Precio', text='Precio', anchor='w')
        self.tablaProductos.heading('Stock', text='Stock', anchor='w')

        self.tablaProductos.column('Codigo', anchor='w', width=100)
        self.tablaProductos.column('Nombre', anchor='w', width=200)
        self.tablaProductos.column('Precio', anchor='w', width=100)
        self.tablaProductos.column('Stock', anchor='w', width=100)

        for p in self.listaProductos:
            self.tablaProductos.insert('', 'end', values=p)

    def buscarProducto(self):
        # Obtener el texto del Entry
        texto_busqueda = self.svBuscar.get()

        # Verificar si se proporcionó algún texto de búsqueda
        if texto_busqueda:
            # Crear la condición WHERE
            where = "WHERE codigo LIKE '%" + texto_busqueda +  "%' OR nombre LIKE '%" + texto_busqueda + "%'"
        else:
            where = ""  # Si no se proporcionó ninguna entrada, no se aplica ninguna condición WHERE

        # Llamar a la función para obtener los productos con las condiciones dadas
        self.cargarTablaProductos(where)

    def cargarTablaVentas(self, where=""):
        self.listaVentas = listarVentas()

        # Frame para la tabla y la barra de desplazamiento
        frame_tablaVentas = tk.Frame(self)
        frame_tablaVentas.grid(column=2, row=2, columnspan=6, sticky='nsew', padx=10, pady=10)

        # Título de la tabla de ventas
        label_ventas = tk.Label(frame_tablaVentas, text="Ventas", font=('Arial', 16, 'bold'), bg='#BBBBBB')
        label_ventas.pack(side='top')

        # Crear la tabla con barra de desplazamiento
        self.tablaVentas = ttk.Treeview(frame_tablaVentas, columns=('idVenta', 'total', 'fecha'), show='headings')
        scrollbar = ttk.Scrollbar(frame_tablaVentas, orient='vertical', command=self.tablaVentas.yview)
        self.tablaVentas.configure(yscroll=scrollbar.set)
        self.tablaVentas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.tablaVentas.heading('idVenta', text='ID', anchor='w')
        self.tablaVentas.heading('total', text='Total', anchor='w')
        self.tablaVentas.heading('fecha', text='Fecha', anchor='w')

        self.tablaVentas.column('idVenta', anchor='w', width=100)
        self.tablaVentas.column('total', anchor='w', width=150)
        self.tablaVentas.column('fecha', anchor='w', width=150)

        for v in self.listaVentas:
            self.tablaVentas.insert('', 'end', values=v)

    def configurar_carrito(self):
        # Crear un frame para el carrito y añadir el Treeview
        frame_carrito = tk.Frame(self)
        frame_carrito.grid(column=0, row=0, rowspan=3, sticky='nsew', padx=10, pady=10)

        # Título de la tabla de carrito
        label_carrito = tk.Label(frame_carrito, text="Carrito", font=('Arial', 16, 'bold'), bg='#BBBBBB')
        label_carrito.pack(side='top')

        self.tree_carrito = ttk.Treeview(frame_carrito, columns=("codigo", "producto", "precio"), show="headings")
        self.tree_carrito.heading("codigo", text="Codigo")
        self.tree_carrito.heading("producto", text="Producto")
        self.tree_carrito.heading("precio", text="Precio")

        self.tree_carrito.pack(expand=True, fill='both')

        # Crear un frame para los botones y añadirlos
        frame_botones = tk.Frame(self)
        frame_botones.grid(column=0, row=3, sticky='ew', padx=10, pady=10)

        boton_añadir_carrito = tk.Button(frame_botones, text="Añadir al carrito", command=self.añadir_al_carrito)
        boton_añadir_carrito.config(width=20, font=('ARIAL', 12, 'bold'), fg='#DAD5D6', bg='#001CCF')
        boton_añadir_carrito.grid(column=0, row=0, padx=10, pady=5)

        boton_quitar_carrito = tk.Button(frame_botones, text="Eliminar al carrito", command=self.quitar_al_carrito)
        boton_quitar_carrito.config(width=20, font=('ARIAL', 12, 'bold'), fg='#DAD5D6', bg='#001CCF')
        boton_quitar_carrito.grid(column=1, row=0, padx=10, pady=5)

        boton_generar_venta = tk.Button(frame_botones, text="Generar Venta", command=self.generar_venta)
        boton_generar_venta.config(width=20, font=('ARIAL', 12, 'bold'), fg='#DAD5D6', bg='#001CCF')
        boton_generar_venta.grid(column=2, row=0, padx=10, pady=5)

        # Crear un label para mostrar el total de la venta
        self.label_total = tk.Label(frame_botones, text="Total de la venta: 0")
        self.label_total.grid(column=1, row=1, padx=10, pady=5)

    def añadir_al_carrito(self):
        selected_item = self.tablaProductos.focus()
        if selected_item:
            producto = self.tablaProductos.item(selected_item)['values']
            self.tree_carrito.insert("", tk.END, values=(producto[0], producto[1], producto[2]))

    def quitar_al_carrito(self):
        selected_item = self.tree_carrito.focus()
        if selected_item:
            self.tree_carrito.delete(selected_item)


    def generar_venta(self):
        total = 0
        for item in self.tree_carrito.get_children():
            valores = self.tree_carrito.item(item, "values")
            total += float(valores[2])  # Suponiendo que el precio está en la tercera posición
            actualizar_stock_db(valores[0], -1.0)  # Actualizar el stock del producto restando 1 por cada venta

        self.label_total.config(text=f"Total de la venta: {total}")
        self.cargarTablaProductos() 
        