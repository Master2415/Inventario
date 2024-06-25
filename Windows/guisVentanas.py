import tkinter as tk
from tkinter import messagebox
from Conexion.Conexion import conexionBD
from View.ProductoView import Frame_Producto
from View.ClienteView import Frame_Cliente
from View.VentaView import Frame_Venta
from View.ProveedorView2 import Frame_Proveedor
from View.StockView import Frame_Stock
from View.AdminView import Frame_Admin
from Model.VentaDAO import Venta

class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Inventario")
        self.geometry("1745x820")
        self.config(bg='#CDD8FF')

        # Variable para almacenar el usuario actual
        self.usuario_actual = None

        # Crear el marco de la barra lateral
        self.frame_sidebar = tk.Frame(self, width=200, bg='#53005B')
        self.frame_sidebar.pack(side='left', fill='y')

        # Crear el marco de contenido principal
        self.frame_main = tk.Frame(self, bg='#FFFFFF', width=1080, height=720)
        self.frame_main.pack(side='left', expand=True, fill='both')

       # Formulario de inicio de sesión
        self.frame_login = tk.Frame(self.frame_main, bg='#BBBBBB')
        self.frame_login.place(relx=0.5, rely=0.5, anchor='center')

        # Configurar la grilla para el formulario de inicio de sesión
        self.frame_login.columnconfigure(0, weight=1)
        self.frame_login.columnconfigure(1, weight=1)

        tk.Label(self.frame_login, text="Usuario:", font=('Arial', 15, 'bold'), bg='#BBBBBB').grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.entry_usuario = tk.Entry(self.frame_login, width=25, font=('Arial', 15))
        self.entry_usuario.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.frame_login, text="Contraseña:", font=('Arial', 15, 'bold'), bg='#BBBBBB').grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.entry_contraseña = tk.Entry(self.frame_login, show="*", width=25, font=('Arial', 15))
        self.entry_contraseña.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(self.frame_login, text="Iniciar sesión", command=self.iniciar_sesion, width=20, font=('Arial', 12, 'bold'), fg='#DAD5D6', bg='#001CCF').grid(row=2, columnspan=2, pady=10)

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

        self.btnStock = tk.Button(self.frame_sidebar, text="Stock", command=self.mostrarStock)
        self.btnStock.config(width=20, font=('ARIAL',12,'bold'), fg='#DAD5D6', bg='#CF0000')
        self.btnStock.pack(fill='x', pady=7, padx=5)

        self.btnAdmin = tk.Button(self.frame_sidebar, text="Administrador", command=self.mostrarAdmin)
        self.btnAdmin.config(width=20, font=('ARIAL',12,'bold'), fg='#DAD5D6', bg='#CF0000')
        self.btnAdmin.pack(fill='x', pady=7, padx=5)

        # Botón de salir en la parte inferior de la barra lateral
        self.btnSalir = tk.Button(self.frame_sidebar, text="Salir", command=self.salir)
        self.btnSalir.config(width=20, font=('ARIAL',12,'bold'), fg='#DAD5D6', bg='#CF0000')
        self.btnSalir.pack(side='bottom', fill='x', pady=5, padx=5)

        # Deshabilitar botones al inicio
        self.habilitar_botones(False)

    def habilitar_botones(self, estado):
        self.btnProductos.config(state='normal' if estado else 'disabled')
        self.btnClientes.config(state='normal' if estado else 'disabled')
        self.btnProveedores.config(state='normal' if estado else 'disabled')
        self.btnVenta.config(state='normal' if estado else 'disabled')
        self.btnStock.config(state='normal' if estado else 'disabled')
        self.btnAdmin.config(state='normal' if estado else 'disabled')

    def iniciar_sesion(self):
        usuario = self.entry_usuario.get()
        contraseña = self.entry_contraseña.get()

        # Conexión a la base de datos
        conexion = conexionBD()
        cursor = conexion.cursor()

        # Validar credenciales
        cursor.execute("SELECT idEmpleado FROM usuario WHERE correo=%s AND contrasena=%s AND estado=1", (usuario, contraseña))
        resultado = cursor.fetchone()
       

        if resultado:
            id_empleado = resultado[0]
            cursor.execute("SELECT Rol_idRol FROM empleado WHERE idEmpleado=%s", (id_empleado,))
            rol_resultado = cursor.fetchone()
            
            if rol_resultado:
                rol_id = rol_resultado[0]
                self.usuario_actual = usuario
                self.habilitar_botones(True)
                if rol_id != 1:
                    self.btnAdmin.pack_forget()  # Ocultar botón de administrador
                self.frame_login.pack_forget()  # Ocultar el formulario de inicio de sesión
            else:
                messagebox.showerror("Error de inicio de sesión", "No se encontró el rol del usuario.")
        else:
            messagebox.showerror("Error de inicio de sesión", "Usuario o contraseña incorrectos")
        
        cursor.close()
        conexion.close()

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

    def mostrarStock(self):
        # Limpiar el contenido anterior del marco principal
        for widget in self.frame_main.winfo_children():
            widget.destroy()
        
         # Mostrar la vista de productos en el marco principal
        frame_Stock = Frame_Stock(self.frame_main, width=1080, height=720)
        frame_Stock.pack(fill='both', expand=True)

    def mostrarAdmin(self):
        # Limpiar el contenido anterior del marco principal
        for widget in self.frame_main.winfo_children():
            widget.destroy()
        
         # Mostrar la vista de productos en el marco principal
        frame_Admin = Frame_Admin(self.frame_main, width=1080, height=720)
        frame_Admin.pack(fill='both', expand=True)

        
    def salir(self):
        self.destroy()



