import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import *
from Model.DetalleVentaDAO import *

class DetalleVentaView(tk.Toplevel):
    def __init__(self, parent, idVenta):
        super().__init__(parent)
        self.parent = parent
        self.idVenta = idVenta
        self.title('Detalle de Venta')
        self.resizable(0, 0)
        self.config(bg='#f0f2f5')
        self.tablaDetalle()
        self.idDetalleVenta = None

    def tablaDetalle(self):
        try:
            self.listaDetalleVenta = listaDetalleVenta(self.idVenta)
            self.tree_detalle = ttk.Treeview(self, columns=("Cantidad", "Precio Unitario", "Subtotal", "Nombre Producto", "Código Producto"), show="headings", selectmode="browse")
            self.tree_detalle.heading("Cantidad", text="Cantidad en Kg")
            self.tree_detalle.heading("Precio Unitario", text="Precio por Kg")
            self.tree_detalle.heading("Subtotal", text="Subtotal")
            self.tree_detalle.heading("Nombre Producto", text="Nombre Producto")
            self.tree_detalle.heading("Código Producto", text="Código Producto")

            for i, detalle in enumerate(self.listaDetalleVenta):
                cantidad = detalle[1]
                precio = f"{detalle[2]:,.2f}"  # Formatear precio a dos decimales
                subtotal = f"{detalle[3]:,.2f}"
                id_venta = detalle[4]
                codigo_producto = detalle[5]  # Suponiendo que ahora el detalle contiene el código del producto

                # Agregar ceros a la izquierda al código del producto si es necesario
                codigo_producto = f"{codigo_producto}" 

                self.tree_detalle.insert('', 'end', values=(cantidad, precio, subtotal, id_venta, codigo_producto), tags=('evenrow',) if i % 2 == 0 else ())

            self.tree_detalle.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo mostrar el detalle de venta: {e}")

    
    