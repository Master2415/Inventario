import tkinter as tk
from tkinter import ttk
from Model.ResumenDAO import *
from tkinter import messagebox
from tkinter.simpledialog import askstring
from datetime import datetime

class Frame_Resumen(tk.Frame):
    def __init__(self, root, width=1745, height=750):
        super().__init__(root, width=width, height=height)
        self.root = root
        self.config(bg='#f0f0f0')  # Establecer el color de fondo del frame principal
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

            self.titulo_tablaCaja = tk.Label(self.frame_productos, text="INVENTARIO ACTUAL", font=("Arial", 16))
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
        
        self.total_label = tk.Label(self, text='Total Valor Inventario: 0.0', bg='#f0f0f0',  font=("Arial", 14))
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
        self.config(bg='#f0f0f0')  # Establecer el color de fondo del frame principal
        self.pack(fill='both', expand=True)
        self.create_widgets()
        self.listar_productos()

    def create_widgets(self):
        self.frame_fechas = tk.Frame(self)
        self.frame_fechas.pack(fill='x', padx=10, pady=10)

        tk.Label(self.frame_fechas, text="Fecha Inicio (YYYY-MM-DD):").pack(side='left')
        self.fecha_inicio = tk.Entry(self.frame_fechas)
        self.fecha_inicio.pack(side='left', padx=5)

        tk.Label(self.frame_fechas, text="Fecha Fin (YYYY-MM-DD):").pack(side='left')
        self.fecha_fin = tk.Entry(self.frame_fechas)
        self.fecha_fin.pack(side='left', padx=5)

        self.boton_listar = tk.Button(self.frame_fechas, text="Listar", command=self.listar_productos)
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
        self.label_total_vendido = tk.Label(self, text="Total Vendido: $0.00", font=("Arial", 14))
        self.label_total_vendido.pack(pady=10)

    def listar_productos(self):
        fecha_inicio = self.fecha_inicio.get()
        fecha_fin = self.fecha_fin.get()
        if not fecha_inicio or not fecha_fin:
            messagebox.showinfo("Error", "Ambos campos de fecha son obligatorios para generar la lista.")
            return
        try:
            datetime.strptime(fecha_inicio, '%Y-%m-%d')
            datetime.strptime(fecha_fin, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha incorrecto. Use YYYY-MM-DD.")
            return

        self.listProductos = consulta_productos(fecha_inicio, fecha_fin)
        
        if hasattr(self, 'tablaProductos'):
            self.tablaProductos.delete(*self.tablaProductos.get_children())

        total_vendido = 0

        for p in self.listProductos:
            total_vendido += p[3]
            self.tablaProductos.insert('', 'end', text=p[0], values=(p[1], p[2], "{:,.2f}".format(p[3])), tags=('evenrow',))

        self.label_total_vendido.config(text=f"Total Vendido: ${total_vendido:,.2f}")


    