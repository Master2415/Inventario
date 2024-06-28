import tkinter as tk
from tkinter import ttk
from Model.ResumenDAO import *

class Frame_Resumen(tk.Frame):
    
    def __init__(self, root, width=1745, height=750):
        super().__init__(root, width=width, height=height)
        self.root = root
        self.config(bg='#f0f0f0')  # Establecer el color de fondo del frame principal
        self.pack(fill='both', expand=True)
        self.create_widgets()
        self.listarProductosConPrecioPromedio()

    def create_widgets(self):
        if hasattr(self, 'productos_treeview'):
            self.productos_treeview.delete(*self.productos_treeview.get_children())
        
        if not hasattr(self, 'frame_productos'):
            self.frame_productos = tk.Frame(self, height=800)
            self.frame_productos.pack(fill='x', expand=False)
            
            self.productos_treeview = ttk.Treeview(self.frame_productos, columns=('codigo', 'nombre', 'precioPromedio',  'cantidadStock', 'valorInventario'), height=20)
            self.scrollbar = ttk.Scrollbar(self.frame_productos, orient='vertical', command=self.productos_treeview.yview)
            self.productos_treeview.configure(yscroll=self.scrollbar.set)
            self.productos_treeview.pack(side='left', fill='both', expand=True)
            self.scrollbar.pack(side='right', fill='y')
            
            self.productos_treeview.heading('#0', text='Código')
            self.productos_treeview.heading('#1', text='Nombre')
            self.productos_treeview.heading('#2', text='Precio Promedio')
            self.productos_treeview.heading('#3', text='Cantidad en Stock')
            self.productos_treeview.heading('#4', text='Valor Inventario')
            
            self.productos_treeview.column("#0", anchor='w', width=100)
            self.productos_treeview.column("#1", anchor='w', width=200)
            self.productos_treeview.column("#2", anchor='w', width=150)
            self.productos_treeview.column("#3", anchor='w', width=150)
            self.productos_treeview.column("#4", anchor='w', width=200)
        
        self.total_label = tk.Label(self, text='Total Valor Inventario: 0.0', bg='#f0f0f0')
        self.total_label.pack()

    def listarProductosConPrecioPromedio(self):
        productos, total_valor_inventario = listarProductosConPrecioPromedio()
        for producto in productos:
            precio_promedio_formateado = "{:,.2f}".format(producto[2])
            cantidad_stock_formateado = "{:,.2f}".format(producto[3])
            valor_inventario_formateado = "{:,.2f}".format(producto[4])
            self.productos_treeview.insert('', 'end', text=producto[0], values=(producto[1], precio_promedio_formateado, cantidad_stock_formateado, valor_inventario_formateado))
        
        self.total_label.config(text=f'Total Valor Inventario: {total_valor_inventario:,.2f}')