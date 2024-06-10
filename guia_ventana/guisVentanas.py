import tkinter as tk
from Producto.ProductoView import Frame_Producto
from Cliente.ClienteView import Frame_Cliente

class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Inventario")
        self.geometry("1450x720")
        self.config(bg='#CDD8FF')

        # Crear el marco de la barra lateral
        self.frame_sidebar = tk.Frame(self, width=200, bg='#53005B')
        self.frame_sidebar.pack(side='left', fill='y')

        # Crear el marco de contenido principal
        self.frame_main = tk.Frame(self, bg='#FFFFFF', width=1080, height=720)
        self.frame_main.pack(side='left', expand=True, fill='both')

        # Botones de la barra lateral con estilo
        self.btnAgregarHistoria = tk.Button(self.frame_sidebar, text="Productos", command=self.mostrarProductos)
        self.btnAgregarHistoria.config(width=20, font=('ARIAL',12,'bold'), fg='#DAD5D6', bg='#CF0000')
        self.btnAgregarHistoria.pack(fill='x', pady=5, padx=5)
    
        self.btnOtraOpcion = tk.Button(self.frame_sidebar, text="Clientes", command=self.mostrarClientes)
        self.btnOtraOpcion.config(width=20, font=('ARIAL',12,'bold'), fg='#DAD5D6', bg='#CF0000')
        self.btnOtraOpcion.pack(fill='x', pady=5, padx=5)

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
    
    def salir(self):
        self.destroy()



