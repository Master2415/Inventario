import tkinter as tk
from tkinter import ttk
from datetime import datetime
from View.DetalleVentaView import *
from Model.ProductoDAO import *
from Model.VentaDAO import *
from Model.DetalleVentaDAO import listaDetalleVenta, guardarDetalle_venta
from Model.ClienteDao import buscar_y_guardar_cedula, obtener_id_por_cedula, obtener_nombre_por_cedula
from Model.UsuarioDAO import obtenerIdUsuario
from Model.CajaDAO import verificarCajaAbierta
from Model.ReciboGenerator import ReciboGenerator

class Frame_Venta(tk.Frame):
    def __init__(self, root, width=1450, height=720):
        super().__init__(root, width=width, height=height)
        self.root = root
        self.config(bg='#f0f2f5')
        self.pack(fill='both', expand=True)
        self.idVenta = None
        self.idProducto = None
        self.inventario = {}
        
        # Obtener ID del usuario actual
        if hasattr(self.root.master, 'usuario_actual'):
             self.idUsuario = obtenerIdUsuario(self.root.master.usuario_actual)
        else:
             self.idUsuario = None # Fallback or error handling

        # Configuración inicial
        self.botones()
        self.cargarTablaProductos()
        self.cargarTablaVentas()
        self.configurar_carrito()

    def botones(self):
        self.svBuscar = tk.StringVar()
        self.entryBuscar = tk.Entry(self, textvariable=self.svBuscar, width=25, font=('Segoe UI', 15))
        self.entryBuscar.grid(column=1, row=0, padx=10, pady=5, columnspan=2)

        self.svCantidad = tk.StringVar()
        self.entryCantidad = tk.Entry(self, textvariable=self.svCantidad, width=25, font=('Segoe UI', 15))
        self.entryCantidad.grid(column=2, row=2, padx=10, pady=5, columnspan=2)

        self.btnBuscar = tk.Button(self, text='Buscar', command=self.buscarProducto, width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#3498db', relief='flat', cursor='hand2')
        self.btnBuscar.grid(column=3, row=0, padx=10, pady=5)

        self.boton_añadir_carrito = tk.Button(self, text="Añadir al carrito", command=self.añadir_al_carrito, width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#3498db', relief='flat', cursor='hand2')
        self.boton_añadir_carrito.grid(column=1, row=2, padx=10, pady=5)

        self.btn_detalleVenta = tk.Button(self, text="Detalle Venta",command=self.verDetalleVenta,  width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#3498db', relief='flat', cursor='hand2')
        self.btn_detalleVenta.grid(column=1, row=4, padx=10, pady=5)
        
        self.btn_recibo = tk.Button(self, text="Generar Recibo", command=self.generar_recibo, width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#2c3e50', relief='flat', cursor='hand2')
        self.btn_recibo.grid(column=2, row=4, padx=10, pady=5)

    def verDetalleVenta(self):
        self.idVenta = self.get_selected_vent_id()
        if self.idVenta:
            DetalleVentaView(self, self.idVenta)
        else:
            messagebox.showerror("Error", "Seleccione una Venta")
            
    def generar_recibo(self):
        id_venta = self.get_selected_vent_id()
        if not id_venta:
            messagebox.showerror("Error", "Seleccione una Venta para generar el recibo")
            return
            
        # Obtener datos de la venta
        venta_info = None
        for item in self.listaVentas:
            if str(item[0]) == str(id_venta):
                venta_info = item
                break
        
        if not venta_info:
            return

        # venta_info: (idVenta, total, fecha, Cajero, Cedula Cliente)
        venta_data = {
            'id': venta_info[0],
            'total': venta_info[1],
            'fecha': venta_info[2],
            'cajero': venta_info[3]
        }
        
        cedula_cliente = venta_info[4]
        nombre_cliente = obtener_nombre_por_cedula(cedula_cliente) # Necesitamos implementar esto o obtenerlo de otra forma
        if not nombre_cliente:
            nombre_cliente = "Cliente General"

        # Obtener detalles
        detalles = listaDetalleVenta(id_venta) # Retorna lista de tuplas
        # listaDetalleVenta retorna: (id, cantidad, precio, subTotal, nombre, codigo)
        
        lista_detalles = []
        for d in detalles:
            lista_detalles.append({
                'producto': d[4], # nombre del producto
                'cantidad': d[1],
                'precio': d[2],
                'subtotal': d[3]
            })
            
        generator = ReciboGenerator(self.root, venta_data, lista_detalles, nombre_cliente)
        generator.generar_recibo_window()

    def get_selected_vent_id(self):
        selected_item = self.tablaVentas.selection()
        if selected_item:
            return self.tablaVentas.item(selected_item)['values'][0]  
        else:
            return None


    def cargarTablaProductos(self, where=""):
        self.listaProductos = listarCondicionesTabla_Productos(where) if where else listarProductos_En_Venta()
        self.inventario = {p[0]: p[3] for p in self.listaProductos}

        frame_tablaProductos = tk.Frame(self)
        frame_tablaProductos.grid(column=1, row=1, columnspan=6, sticky='nsew', padx=10, pady=10)

        label_productos = tk.Label(frame_tablaProductos, text="Productos", font=('Segoe UI', 16, 'bold'))
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

        # Insertar filas en la tabla
        for producto in self.listaProductos:
            codigo = producto[0]
            nombre = producto[1]
            precio = "{:,.2f}".format(producto[2])
            stock = producto[3]

            stock_formateado = f"{stock:.2f}"# Formatear el stock con dos decimales

            self.tablaProductos.insert('', 'end', values=(codigo, nombre, precio, stock_formateado))


    def cargarTablaVentas(self):
        self.listaVentas = listarVentas()
    
        frame_tablaVentas = tk.Frame(self)
        frame_tablaVentas.grid(column=1, row=3, columnspan=6, sticky='nsew', padx=10, pady=10)

        label_ventas = tk.Label(frame_tablaVentas, text="Ventas", font=('Segoe UI', 16, 'bold'))
        label_ventas.pack(side='top')

        self.tablaVentas = ttk.Treeview(frame_tablaVentas, columns=('idVenta', 'total', 'fecha', 'Cajero', 'Cedula Cliente'), show='headings')
        scrollbar = ttk.Scrollbar(frame_tablaVentas, orient='vertical', command=self.tablaVentas.yview)
        self.tablaVentas.configure(yscroll=scrollbar.set)
        self.tablaVentas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.tablaVentas.heading('idVenta', text='ID', anchor='w')
        self.tablaVentas.heading('total', text='Total', anchor='w')
        self.tablaVentas.heading('fecha', text='Fecha', anchor='w')
        self.tablaVentas.heading('Cajero', text='Cajero', anchor='w')
        self.tablaVentas.heading('Cedula Cliente', text='Cedula Cliente', anchor='w')

        self.tablaVentas.column('idVenta', anchor='w', width=50)
        self.tablaVentas.column('total', anchor='w', width=100)
        self.tablaVentas.column('fecha', anchor='w', width=170)
        self.tablaVentas.column('Cajero', anchor='w', width=120)
        self.tablaVentas.column('Cedula Cliente', anchor='w', width=120)

        for venta in self.listaVentas:
            id_venta = venta[0]
            total = f"{venta[1]:,.2f}"  # Formatear total a dos decimales
            fecha = venta[2]
            Cajero = venta[3]
            Cedula = venta[4]

            self.tablaVentas.insert('', 'end', values=(id_venta, total, fecha, Cajero, Cedula))


    def configurar_carrito(self):
        frame_carrito = tk.Frame(self)
        frame_carrito.grid(column=0, row=1, rowspan=1, sticky='nsew', padx=10, pady=10)

        label_carrito = tk.Label(frame_carrito, text="Carrito", font=('Segoe UI', 16, 'bold'))
        label_carrito.pack(side='top')

        self.tree_carrito = ttk.Treeview(frame_carrito, columns=("codigo", "producto", "cantidad", "precio"), show="headings")
        self.tree_carrito.heading("codigo", text="Codigo")
        self.tree_carrito.heading("producto", text="Producto")
        self.tree_carrito.heading("cantidad", text="Cantidad")
        self.tree_carrito.heading("precio", text="Precio")
        self.tree_carrito.pack(expand=True, fill='both')

        # Eliminado frame_usuario y boxUser porque ahora se usa el usuario logueado

        frame_botones = tk.Frame(self)
        frame_botones.grid(column=0, row=3, sticky='ew', padx=10, pady=10)

        boton_quitar_carrito = tk.Button(frame_botones, text="Eliminar del carrito", command=self.quitar_al_carrito, width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#c0392b', relief='flat', cursor='hand2')
        boton_quitar_carrito.grid(column=1, row=0, padx=10, pady=5)

        boton_generar_venta = tk.Button(frame_botones, text="Generar Venta", command=self.generar_venta, width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#27ae60', relief='flat', cursor='hand2')
        boton_generar_venta.grid(column=2, row=0, padx=10, pady=5)

        self.label_total = tk.Label(frame_botones, text="Total de la venta: 0")
        self.label_total.grid(column=1, row=1, padx=10, pady=5)

        self.label_status = tk.Label(frame_botones, text="")
        self.label_status.grid(column=1, row=2, padx=10, pady=5)

        frame_botones_up = tk.Frame(self)
        frame_botones_up.grid(column=0, row=0, sticky='ew', padx=10, pady=10)

        self.svCedula = tk.StringVar()
        self.entryCedula = tk.Entry(frame_botones_up, textvariable=self.svCedula, width=25, font=('Segoe UI', 15))
        self.entryCedula.grid(column=1, row=0, padx=10, pady=5, columnspan=2)

        self.lbltipo = tk.Label(frame_botones_up, text='Cedula del Cliente', font=('Segoe UI', 15, 'bold'))
        self.lbltipo.grid(column=0, row=0, padx=10, pady=5)

    def quitar_al_carrito(self):
        selected_item = self.tree_carrito.focus()
        if selected_item:
            self.tree_carrito.delete(selected_item)
            self.label_status.config(text="Eliminado exitosamente")

    def buscarProducto(self):
        texto_busqueda = self.svBuscar.get()
        if texto_busqueda:
            where = where = f"codigo LIKE '%{texto_busqueda}%' OR nombre LIKE '%{texto_busqueda}%'"
        else:
            where = ""

        self.cargarTablaProductos(where)


    def añadir_al_carrito(self):
        selected_item = self.tablaProductos.focus()
        if selected_item:
            producto = self.tablaProductos.item(selected_item)['values']
            try:
                cantidad = float(self.svCantidad.get())
                precio_unitario = float(producto[2].replace(',', ''))  # Convertir el precio a float
                precio_total = cantidad * precio_unitario
                codigo_producto = str(producto[0])  # Asume que el código debe tener al menos 3 dígitos
                self.tree_carrito.insert("", tk.END, values=(codigo_producto, producto[1], cantidad, round(precio_total, 2)))

                # Actualizar el total del carrito
                self.actualizar_total_carrito()
            
            except ValueError:
                self.label_status.config(text="Por favor, ingrese un número válido")

    def actualizar_total_carrito(self):
        total = 0
        for child in self.tree_carrito.get_children():
            item = self.tree_carrito.item(child)
            total += float(item['values'][3])  # Sumar el precio total de cada producto
        self.label_total.config(text=f"Total de la venta: {total:.2f}")



    def generar_venta(self):
        # 1. Verificar si hay usuario logueado
        if not self.idUsuario:
            messagebox.showerror("Error", "No se ha identificado al usuario actual.")
            return

        # 2. Verificar si la caja está abierta
        if not verificarCajaAbierta(self.idUsuario):
            messagebox.showwarning("Caja Cerrada", "Debe ABRIR CAJA antes de realizar ventas.")
            return

        total = 0
        detalles_venta = []  # Lista para almacenar los detalles de la venta
        # Recorrer todos los ítems del carrito
        for item in self.tree_carrito.get_children():
            # Obtener los valores del producto en el carrito
            valores = self.tree_carrito.item(item, "values")
            # Sumar el precio total del producto al total de la venta
            total += float(valores[3])
            # Obtener los detalles del producto
            codigo_producto = valores[0]  # Código del producto
            cantidad = float(valores[2])
            precio_unitario = float(valores[3]) / cantidad # el precio se toma del total del carrito, por eso se divide por la cantidad
            subtotal = cantidad * precio_unitario
            # Obtener el idProducto del producto
            id_producto = obtener_id_por_producto(codigo_producto)
            if id_producto is not None:
                # Agregar el detalle de venta a la lista
                detalles_venta.append({'cantidad': cantidad, 'precio': precio_unitario, 'subtotal': subtotal, 'idProducto': id_producto})
                # Llamar a la función para actualizar el stock del producto
                self.actualizar_stock_salida_carrito(id_producto, cantidad)
            else:
                messagebox.showwarning("Advertencia", f"No se encontró el ID del producto para el código {codigo_producto}")

        # Actualizar el label con el total de la venta
        self.label_total.config(text=f"Total de la venta: {round(total, 2)}")    
        # Guardar la cédula del cliente si no existe
        buscar_y_guardar_cedula(self.svCedula.get())   
        # Obtener el ID del cliente por su cédula
        cliente_id = obtener_id_por_cedula(self.svCedula.get())
        
        # Usar el usuario logueado
        self.guardar_Venta(total, self.idUsuario, cliente_id, detalles_venta)
        
        # Recargar la tabla de productos y ventas para reflejar los cambios en el stock y las ventas
        self.cargarTablaProductos()
        self.cargarTablaVentas()
        # Limpiar el carrito después de generar la venta
        self.tree_carrito.delete(*self.tree_carrito.get_children())


    def guardar_Venta(self, total, usuario_id, cliente_id, detalles_venta):
        try:
            # Asignar la fecha actual al entry de fecha
            fecha_actual = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            # Crear el objeto Venta
            venta = Venta(total, fecha_actual, usuario_id, cliente_id)
            # Guardar la venta principal
            guardarVenta(venta)
            # Obtener el ID de la venta recién guardada
            id_venta = obtener_id_venta_reciente()
            # Guardar cada detalle de venta asociado a la venta principal
            for detalle in detalles_venta:
                detalle['idVenta'] = id_venta  # Asignar el ID de la venta principal al detalle
                guardarDetalle_venta(detalle)
            #messagebox.showinfo("Éxito", "Venta registrada correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la venta: {e}")


    def actualizar_stock_salida_carrito(self, idProducto, cantidad):
        try:
            # Actualizar el stock en la base de datos restando la cantidad vendida
            actualizar_stock_db(idProducto, -cantidad)
            # Recorrer todos los ítems del carrito
            for item in self.tree_carrito.get_children():
                # Obtener los valores del producto en el carrito
                valores = self.tree_carrito.item(item, "values")
                # Comprobar si el código del producto en el carrito coincide con el código del producto actualizado
                if valores[0] == idProducto:
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
