import tkinter as tk
from View.ProductoView import Frame_Producto
from View.ClienteView import Frame_Cliente
from View.VentaView import Frame_Venta
from View.ProveedorView2 import Frame_Proveedor

class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Inventario")
        self.geometry("1745x750")
        self.config(bg='#CDD8FF')

        # Crear el marco de la barra lateral
        self.frame_sidebar = tk.Frame(self, width=200, bg='#53005B')
        self.frame_sidebar.pack(side='left', fill='y')

        # Crear el marco de contenido principal
        self.frame_main = tk.Frame(self, bg='#FFFFFF', width=1080, height=720)
        self.frame_main.pack(side='left', expand=True, fill='both')

        # Botones de la barra lateral con estilo
        self.btnProductos = tk.Button(self.frame_sidebar, text="Productos", command=self.mostrarProductos)
        self.btnProductos.config(width=20, font=('ARIAL',12,'bold'), fg='#DAD5D6', bg='#CF0000')
        self.btnProductos.pack(fill='x', pady=5, padx=5)
    
        self.btnClientes = tk.Button(self.frame_sidebar, text="Clientes", command=self.mostrarClientes)
        self.btnClientes.config(width=20, font=('ARIAL',12,'bold'), fg='#DAD5D6', bg='#CF0000')
        self.btnClientes.pack(fill='x', pady=5, padx=5)

        self.btnProveedores = tk.Button(self.frame_sidebar, text="Proveedores", command=self.mostrarProveedor)
        self.btnProveedores.config(width=20, font=('ARIAL',12,'bold'), fg='#DAD5D6', bg='#CF0000')
        self.btnProveedores.pack(fill='x', pady=5, padx=5)

        self.btnVenta = tk.Button(self.frame_sidebar, text="Venta", command=self.mostrarVenta)
        self.btnVenta.config(width=20, font=('ARIAL',12,'bold'), fg='#DAD5D6', bg='#CF0000')
        self.btnVenta.pack(fill='x', pady=5, padx=5)

        # Botón de salir en la parte inferior de la barra lateral
        self.btnSalir = tk.Button(self.frame_sidebar, text="Salir", command=self.salir)
        self.btnSalir.config(width=20, font=('ARIAL',12,'bold'), fg='#DAD5D6', bg='#CF0000')
        self.btnSalir.pack(side='bottom', fill='x', pady=5, padx=5)


    def mostrarProductos(self):
        # Limpiar el contenido anterior del marco principal
        for widget in self.frame_main.winfo_children():
            widget.destroy()

        # Mostrar la vista de productos en el marco principal
        frame_producto = Frame_Producto(self.frame_main, width=1080, height=720)
        frame_producto.pack(fill='both', expand=True)
    
    def mostrarClientes(self):
        # Limpiar el contenido anterior del marco principal
        for widget in self.frame_main.winfo_children():
            widget.destroy()
        
         # Mostrar la vista de productos en el marco principal
        frame_producto = Frame_Cliente(self.frame_main, width=1080, height=720)
        frame_producto.pack(fill='both', expand=True)
    
    def mostrarVenta(self):
        # Limpiar el contenido anterior del marco principal
        for widget in self.frame_main.winfo_children():
            widget.destroy()
        
         # Mostrar la vista de productos en el marco principal
        frame_Venta = Frame_Venta(self.frame_main, width=1080, height=720)
        frame_Venta.pack(fill='both', expand=True)

    def mostrarProveedor(self):
        # Limpiar el contenido anterior del marco principal
        for widget in self.frame_main.winfo_children():
            widget.destroy()
        
         # Mostrar la vista de productos en el marco principal
        frame_Proveedor = Frame_Proveedor(self.frame_main, width=1080, height=720)
        frame_Proveedor.pack(fill='both', expand=True)

        
    def salir(self):
        self.destroy()



