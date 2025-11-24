import tkinter as tk
from tkinter import ttk
from Model.ResumenDAO import *
from tkinter import messagebox
from tkinter.simpledialog import askstring
from datetime import datetime
from tkcalendar import DateEntry

class Frame_Resumen(tk.Frame):
    def __init__(self, root, width=1745, height=750):
        super().__init__(root, width=width, height=height)
        self.root = root
        self.config(bg='#f0f2f5')  # Establecer el color de fondo del frame principal
        self.pack(fill='both', expand=True)
        self.tablaResumenInventario()
        self.listarProductosConPrecioPromedio()
        self.sort_column = None
        self.sort_descending = False

    def tablaResumenInventario(self):
        if hasattr(self, 'productos_treeview'):
            self.productos_treeview.delete(*self.productos_treeview.get_children())
        
        if not hasattr(self, 'frame_productos'):
            self.frame_productos = tk.Frame(self, height=800)
            self.frame_productos.pack(fill='x', expand=False)

            self.titulo_tablaCaja = tk.Label(self.frame_productos, text="INVENTARIO ACTUAL", font=("Segoe UI", 16))
            self.titulo_tablaCaja.pack(anchor='center', pady=10)

            self.productos_treeview = ttk.Treeview(self.frame_productos, columns=('codigo', 'nombre', 'precioPromedio', 'cantidadStock', 'valorInventario'), height=20)
            self.scrollbar = ttk.Scrollbar(self.frame_productos, orient='vertical', command=self.productos_treeview.yview)
            self.productos_treeview.configure(yscroll=self.scrollbar.set)
            self.productos_treeview.pack(side='left', fill='both', expand=True)
            self.scrollbar.pack(side='right', fill='y')
            
            self.productos_treeview.heading('#0', text='Código')
            self.productos_treeview.heading('#1', text='Nombre', command=lambda: self.sort_treeview('#1', False))
            self.productos_treeview.heading('#2', text='Precio Promedio de Compra', command=lambda: self.sort_treeview('#2', False))
            self.productos_treeview.heading('#3', text='Cantidad en Stock Kg', command=lambda: self.sort_treeview('#3', False))
            self.productos_treeview.heading('#4', text='Valor Inventario Neto', command=lambda: self.sort_treeview('#4', False))
            
            self.productos_treeview.column("#0", anchor='w', width=100)
            self.productos_treeview.column("#1", anchor='w', width=200)
            self.productos_treeview.column("#2", anchor='w', width=150)
            self.productos_treeview.column("#3", anchor='w', width=150)
            self.productos_treeview.column("#4", anchor='w', width=200)
        
        self.total_label = tk.Label(self, text='Total Valor Inventario: 0.0', bg='#f0f2f5',  font=("Segoe UI", 14))
        self.total_label.pack(pady=10)

    def listarProductosConPrecioPromedio(self):
        productos, total_valor_inventario = listarProductosConPrecioPromedio()
        for producto in productos:
            precio_promedio_formateado = "{:,.2f}".format(producto[2])
            cantidad_stock_formateado = "{:,.2f}".format(producto[3])
            valor_inventario_formateado = "{:,.2f}".format(producto[4])
            self.productos_treeview.insert('', 'end', text=producto[0], values=(producto[1], precio_promedio_formateado, cantidad_stock_formateado, valor_inventario_formateado))
        
        self.total_label.config(text=f'Total Valor Inventario: {total_valor_inventario:,.2f}')

    def sort_treeview(self, col, descending):
        data = [(self.productos_treeview.set(child, col), child) for child in self.productos_treeview.get_children('')]
        data.sort(reverse=descending)
        
        for ix, item in enumerate(data):
            self.productos_treeview.move(item[1], '', ix)
        
        self.productos_treeview.heading(col, command=lambda: self.sort_treeview(col, not descending))

class Frame_ResumenVentas(tk.Frame):
    def __init__(self, root, width=1745, height=750):
        super().__init__(root, width=width, height=height)
        self.root = root
        self.config(bg='#f0f2f5')  # Establecer el color de fondo del frame principal
        self.pack(fill='both', expand=True)
        self.create_widgets()
        self.listar_productos()

    def create_widgets(self):
        self.frame_fechas = tk.Frame(self)
        self.frame_fechas.pack(fill='x', padx=10, pady=10)

        tk.Label(self.frame_fechas, text="Fecha Inicio:").pack(side='left')
        self.fecha_inicio = DateEntry(self.frame_fechas, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='y-mm-dd')
        self.fecha_inicio.pack(side='left', padx=5)

        tk.Label(self.frame_fechas, text="Fecha Fin:").pack(side='left')
        self.fecha_fin = DateEntry(self.frame_fechas, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='y-mm-dd')
        self.fecha_fin.pack(side='left', padx=5)

        self.boton_listar = tk.Button(self.frame_fechas, text="Listar", command=self.listar_productos)
        self.boton_listar.config(font=('Segoe UI', 10, 'bold'), fg='#ffffff', bg='#3498db', relief='flat', cursor='hand2')
        self.boton_listar.pack(side='left', padx=5)

        self.frame_tablaProductos = tk.Frame(self)
        self.frame_tablaProductos.pack(fill='both', expand=True)

        self.tablaProductos = ttk.Treeview(self.frame_tablaProductos, columns=('Codigo', 'Nombre', 'Cantidad Total', 'Total Vendido'))
        self.scrollbar = ttk.Scrollbar(self.frame_tablaProductos, orient='vertical', command=self.tablaProductos.yview)
        self.tablaProductos.configure(yscroll=self.scrollbar.set)
        self.tablaProductos.pack(side='left', fill='both', expand=True)
        self.scrollbar.pack(side='right', fill='y')

        self.tablaProductos.heading('#0', text='Codigo')
        self.tablaProductos.heading('#1', text='Nombre Producto')
        self.tablaProductos.heading('#2', text='Cantidad Total Vendido Kg')
        self.tablaProductos.heading('#3', text='Total Vendido')

        self.tablaProductos.column("#0", anchor='w', width=100)
        self.tablaProductos.column("#1", anchor='w', width=200)
        self.tablaProductos.column("#2", anchor='w', width=150)
        self.tablaProductos.column("#3", anchor='w', width=150)

        # Label para mostrar el total de Total Vendido
        self.label_total_vendido = tk.Label(self, text="Total Vendido: $0.00", font=("Segoe UI", 14))
        self.label_total_vendido.pack(pady=10)

    def listar_productos(self):
        fecha_inicio = self.fecha_inicio.get_date()
        fecha_fin = self.fecha_fin.get_date()
        
        self.listProductos = consulta_productos(fecha_inicio, fecha_fin)
        
        if hasattr(self, 'tablaProductos'):
            self.tablaProductos.delete(*self.tablaProductos.get_children())

        total_vendido = 0

        for p in self.listProductos:
            total_vendido += p[3]
            self.tablaProductos.insert('', 'end', text=p[0], values=(p[1], p[2], "{:,.2f}".format(p[3])), tags=('evenrow',))

        self.label_total_vendido.config(text=f"Total Vendido: ${total_vendido:,.2f}")


class ListadoProductosCompra(tk.Frame):
    def __init__(self, root, width=1745, height=750):
        super().__init__(root, width=width, height=height)
        self.root = root
        self.config(bg='#f0f2f5')  # Establecer el color de fondo del frame principal
        self.pack(fill='both', expand=True)
        self.create_widgets()
        self.listar_productos()

    def create_widgets(self):
        # Frame para el filtro de fechas
        frame_filtros = tk.Frame(self)
        frame_filtros.pack(fill='x', padx=10, pady=10)
        
        tk.Label(frame_filtros, text="Fecha Inicio:").pack(side='left')
        self.fecha_inicio = DateEntry(frame_filtros, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='y-mm-dd')
        self.fecha_inicio.pack(side='left', padx=5)
        
        tk.Label(frame_filtros, text="Fecha Fin:").pack(side='left')
        self.fecha_fin = DateEntry(frame_filtros, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='y-mm-dd')
        self.fecha_fin.pack(side='left', padx=5)
        
        btn_consultar = tk.Button(frame_filtros, text="Consultar", command=self.listar_productos)
        btn_consultar.config(font=('Segoe UI', 10, 'bold'), fg='#ffffff', bg='#3498db', relief='flat', cursor='hand2')
        btn_consultar.pack(side='left', padx=5)
        
        # Frame para la tabla
        self.frame_tabla = tk.Frame(self)
        self.frame_tabla.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.tabla = ttk.Treeview(self.frame_tabla, columns=('codigo', 'nombre', 'tipo', 'cantidad_comprada', 'precio_promedio', 'precio_total'))
        self.tabla.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(self.frame_tabla, orient='vertical', command=self.tabla.yview)
        scrollbar.pack(side='right', fill='y')
        
        self.tabla.configure(yscroll=scrollbar.set)
        
        self.tabla.heading('#0', text='Código')
        self.tabla.heading('#1', text='Nombre')
        self.tabla.heading('#2', text='Tipo')
        self.tabla.heading('#3', text='Cantidad Comprada')
        self.tabla.heading('#4', text='Precio Promedio')
        self.tabla.heading('#5', text='Precio Total')
        
        self.tabla.column('#0', anchor='w', width=100)
        self.tabla.column('#1', anchor='w', width=150)
        self.tabla.column('#2', anchor='w', width=150)
        self.tabla.column('#3', anchor='center', width=120)
        self.tabla.column('#4', anchor='center', width=120)
        self.tabla.column('#5', anchor='center', width=120)
        
        # Label para el total general
        self.total_general_label = tk.Label(self, text="Total General: 0", font=("Segoe UI", 14))
        self.total_general_label.pack(pady=10)
    
    def listar_productos(self):
        fecha_inicio = self.fecha_inicio.get_date()
        fecha_fin = self.fecha_fin.get_date()

        productos = consulta_productos_compra(fecha_inicio, fecha_fin)
        
        # Limpiar la tabla antes de actualizarla
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        
        total_general = 0.0
        for producto in productos:
            cantidad_comprada = "{:,.2f}".format(producto[3])
            precio_promedio = "{:,.2f}".format(producto[4])
            precio_total = "{:,.2f}".format(producto[5])
            self.tabla.insert('', 'end', text=producto[0], values=(producto[1], producto[2], cantidad_comprada, precio_promedio, precio_total))
            total_general += producto[5]
        
        self.total_general_label.config(text=f"Total General: {total_general:,.2f}")
