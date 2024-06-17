import tkinter as tk
from tkinter import ttk
from Model.ProductoDAO import *
from Model.VentaDAO import *

class Frame_Venta(tk.Frame):
    def __init__(self, root, width=1450, height=720):
        super().__init__(root, width=width, height=height)
        self.root = root
        self.config(bg='#BBBBBB')
        self.pack(fill='both', expand=True)
        self.idVenta = None
        self.idProducto = None
        self.inventario = {}

        # Configuración inicial
        self.botones()
        self.cargarTablaProductos()
        self.cargarTablaVentas()
        self.configurar_carrito()

    def botones(self):
        self.svBuscar = tk.StringVar()
        self.entryBuscar = tk.Entry(self, textvariable=self.svBuscar, width=25, font=('ARIAL', 15))
        self.entryBuscar.grid(column=1, row=0, padx=10, pady=5, columnspan=2)

        self.svCantidad = tk.StringVar()
        self.entryCantidad = tk.Entry(self, textvariable=self.svCantidad, width=25, font=('ARIAL', 15))
        self.entryCantidad.grid(column=2, row=2, padx=10, pady=5, columnspan=2)

        self.btnBuscar = tk.Button(self, text='Buscar', command=self.buscarProducto, width=20, font=('ARIAL', 12, 'bold'), fg='#DAD5D6', bg='#001CCF')
        self.btnBuscar.grid(column=3, row=0, padx=10, pady=5)

        self.boton_añadir_carrito = tk.Button(self, text="Añadir al carrito", command=self.añadir_al_carrito, width=20, font=('ARIAL', 12, 'bold'), fg='#DAD5D6', bg='#001CCF')
        self.boton_añadir_carrito.grid(column=1, row=2, padx=10, pady=5)

        self.btn_detalleVenta = tk.Button(self, text="Detalle Venta", width=20, font=('ARIAL', 12, 'bold'), fg='#DAD5D6', bg='#001CCF')
        self.btn_detalleVenta.grid(column=1, row=4, padx=10, pady=5)

    def cargarTablaProductos(self, where=""):
        self.listaProductos = listarCondiciones1(where) if where else listarProductos1()
        self.inventario = {p[0]: p[3] for p in self.listaProductos}

        frame_tablaProductos = tk.Frame(self)
        frame_tablaProductos.grid(column=1, row=1, columnspan=6, sticky='nsew', padx=10, pady=10)

        label_productos = tk.Label(frame_tablaProductos, text="Productos", font=('Arial', 16, 'bold'))
        label_productos.pack(side='top')

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

    def cargarTablaVentas(self, where=""):
        self.listaVentas = listarVentas()

        frame_tablaVentas = tk.Frame(self)
        frame_tablaVentas.grid(column=1, row=3, columnspan=6, sticky='nsew', padx=10, pady=10)

        label_ventas = tk.Label(frame_tablaVentas, text="Ventas", font=('Arial', 16, 'bold'))
        label_ventas.pack(side='top')

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
        frame_carrito = tk.Frame(self)
        frame_carrito.grid(column=0, row=1, rowspan=1, sticky='nsew', padx=10, pady=10)

        label_carrito = tk.Label(frame_carrito, text="Carrito", font=('Arial', 16, 'bold'))
        label_carrito.pack(side='top')

        self.tree_carrito = ttk.Treeview(frame_carrito, columns=("codigo", "producto", "cantidad", "precio"), show="headings")
        self.tree_carrito.heading("codigo", text="Codigo")
        self.tree_carrito.heading("producto", text="Producto")
        self.tree_carrito.heading("cantidad", text="Cantidad")
        self.tree_carrito.heading("precio", text="Precio")
        self.tree_carrito.pack(expand=True, fill='both')

        frame_botones = tk.Frame(self)
        frame_botones.grid(column=0, row=3, sticky='ew', padx=10, pady=10)

        boton_quitar_carrito = tk.Button(frame_botones, text="Eliminar del carrito", command=self.quitar_al_carrito, width=20, font=('ARIAL', 12, 'bold'), fg='#DAD5D6', bg='#001CCF')
        boton_quitar_carrito.grid(column=1, row=0, padx=10, pady=5)

        boton_generar_venta = tk.Button(frame_botones, text="Generar Venta", command=self.generar_venta, width=20, font=('ARIAL', 12, 'bold'), fg='#DAD5D6', bg='#001CCF')
        boton_generar_venta.grid(column=2, row=0, padx=10, pady=5)

        self.label_total = tk.Label(frame_botones, text="Total de la venta: 0")
        self.label_total.grid(column=1, row=1, padx=10, pady=5)

        self.label_status = tk.Label(frame_botones, text="")
        self.label_status.grid(column=1, row=2, padx=10, pady=5)

        frame_botones_up = tk.Frame(self)
        frame_botones_up.grid(column=0, row=0, sticky='ew', padx=10, pady=10)

        self.svCedula = tk.StringVar()
        self.entryCedula = tk.Entry(frame_botones_up, textvariable=self.svCedula, width=25, font=('ARIAL', 15))
        self.entryCedula.grid(column=1, row=0, padx=10, pady=5, columnspan=2)

        self.lbltipo = tk.Label(frame_botones_up, text='Cedula del Cliente', font=('ARIAL', 15, 'bold'))
        self.lbltipo.grid(column=0, row=0, padx=10, pady=5)

    def añadir_al_carrito(self):
        selected_item = self.tablaProductos.focus()
        if selected_item:
            producto = self.tablaProductos.item(selected_item)['values']
            try:
                cantidad = float(self.svCantidad.get())
                precio_unitario = float(producto[2])  # Convertir el precio a float
                precio_total = cantidad * precio_unitario

                # Formatear el código del producto para conservar los ceros a la izquierda
                codigo_producto = str(producto[0]).zfill(3)  # Asume que el código debe tener al menos 3 dígitos
                # Insertar el producto en el carrito con los valores formateados
                self.tree_carrito.insert("", tk.END, values=(codigo_producto, producto[1], cantidad, round(precio_total, 2)))
        
            except ValueError:
                self.label_status.config(text="Por favor, ingrese un número válido")

    def quitar_al_carrito(self):
        selected_item = self.tree_carrito.focus()
        if selected_item:
            self.tree_carrito.delete(selected_item)
            self.label_status.config(text="Eliminado exitosamente")

    def buscarProducto(self):
        texto_busqueda = self.svBuscar.get()
        where = f"WHERE codigo LIKE '%{texto_busqueda}%' OR nombre LIKE '%{texto_busqueda}%'" if texto_busqueda else ""
        self.cargarTablaProductos(where)

    def generar_venta(self):
        total = 0
        # Recorrer todos los ítems del carrito
        for item in self.tree_carrito.get_children():
            # Obtener los valores del producto en el carrito
            valores = self.tree_carrito.item(item, "values")
            # Sumar el precio total del producto al total de la venta
            total += float(valores[3])
            # Obtener el código del producto
            codigo_producto = valores[0]
            # Obtener la cantidad del producto
            cantidad = float(valores[2])
            # Llamar a la función para actualizar el stock del producto
            self.actualizar_stock_salida_carrito(codigo_producto, cantidad)

        # Actualizar el label con el total de la venta
        self.label_total.config(text=f"Total de la venta: {round(total, 2)}")
        # Recargar la tabla de productos para reflejar los cambios en el stock
        self.cargarTablaProductos()
        # Limpiar el carrito después de generar la venta
        self.tree_carrito.delete(*self.tree_carrito.get_children())


    def actualizar_stock_salida_carrito(self, codigo_producto, cantidad):
        try:
            # Actualizar el stock en la base de datos restando la cantidad vendida
            actualizar_stock_db(codigo_producto, -cantidad)

            # Recorrer todos los ítems del carrito
            for item in self.tree_carrito.get_children():
                # Obtener los valores del producto en el carrito
                valores = self.tree_carrito.item(item, "values")
                # Comprobar si el código del producto en el carrito coincide con el código del producto actualizado
                if valores[0] == codigo_producto:
                    # Si coincide, eliminar ese producto del carrito
                    self.tree_carrito.delete(item)
                    # Romper el ciclo ya que el producto ha sido encontrado y eliminado
                    break

            # Actualizar el label de estado con un mensaje de éxito
            self.label_status.config(text="Salida registrada para los productos del carrito")
        except ValueError:
            # Actualizar el label de estado con un mensaje de error si la cantidad no es válida
            self.label_status.config(text="Por favor, ingrese un número válido")
        except KeyError:
            # Actualizar el label de estado con un mensaje de error si el código del producto no es válido
            self.label_status.config(text="Seleccione un producto válido")


    


