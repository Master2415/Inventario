import tkinter as tk
from tkinter import messagebox
from Conexion.Conexion import conexionBD
from View.ProductoView import Frame_Producto
from View.ClienteView import Frame_Cliente
from View.VentaView import Frame_Venta
from View.ProveedorView2 import Frame_Proveedor
from View.StockView import Frame_Stock
from View.AdminView import Frame_Admin
from View.CajaView import Frame_Caja
from View.DashboardView import DashboardView

class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Inventario")
        self.geometry("1280x720")
        self.config(bg='#f0f2f5')
        self.state('zoomed') # Maximizar ventana

        # Colores
        self.primary_color = '#2c3e50' # Azul oscuro para sidebar
        self.accent_color = '#3498db' # Azul claro para acentos
        self.hover_color = '#34495e' # Color hover sidebar
        self.text_color = '#ecf0f1' # Texto claro
        self.bg_color = '#f0f2f5' # Fondo principal

        # Variable para almacenar el usuario actual
        self.usuario_actual = None

        # Crear el marco de la barra lateral
        self.frame_sidebar = tk.Frame(self, width=250, bg=self.primary_color)
        self.frame_sidebar.pack(side='left', fill='y')
        self.frame_sidebar.pack_propagate(False) # Mantener ancho fijo

        # Título en sidebar
        self.lbl_title = tk.Label(self.frame_sidebar, text="INVENTARIO", font=('Segoe UI', 20, 'bold'), bg=self.primary_color, fg=self.text_color)
        self.lbl_title.pack(pady=30)

        # Crear el marco de contenido principal
        self.frame_main = tk.Frame(self, bg=self.bg_color)
        self.frame_main.pack(side='left', expand=True, fill='both')

       # Formulario de inicio de sesión
        self.frame_login = tk.Frame(self.frame_main, bg='white', padx=40, pady=40)
        self.frame_login.place(relx=0.5, rely=0.5, anchor='center')
        
        # Sombra/Borde para login
        self.frame_login.configure(highlightbackground="#d1d1d1", highlightthickness=1)

        tk.Label(self.frame_login, text="Bienvenido", font=('Segoe UI', 24, 'bold'), bg='white', fg='#333').pack(pady=(0, 20))

        tk.Label(self.frame_login, text="Usuario", font=('Segoe UI', 12), bg='white', fg='#666').pack(anchor='w')
        self.entry_usuario = tk.Entry(self.frame_login, width=30, font=('Segoe UI', 12), relief='flat', bg='#f9f9f9')
        self.entry_usuario.pack(pady=(5, 15), ipady=5)
        self.entry_usuario.configure(highlightbackground="#ddd", highlightthickness=1)

        tk.Label(self.frame_login, text="Contraseña", font=('Segoe UI', 12), bg='white', fg='#666').pack(anchor='w')
        self.entry_contraseña = tk.Entry(self.frame_login, show="*", width=30, font=('Segoe UI', 12), relief='flat', bg='#f9f9f9')
        self.entry_contraseña.pack(pady=(5, 20), ipady=5)
        self.entry_contraseña.configure(highlightbackground="#ddd", highlightthickness=1)

        self.btn_login = tk.Button(self.frame_login, text="Iniciar sesión", command=self.iniciar_sesion, 
                                 width=30, font=('Segoe UI', 12, 'bold'), fg='white', bg=self.accent_color, 
                                 relief='flat', cursor='hand2')
        self.btn_login.pack(ipady=5)

        # Botones del menú (se crearán pero no se mostrarán hasta login)
        self.menu_buttons = []
        
        self.create_menu_button("Dashboard", self.mostrarDashboard)
        self.create_menu_button("Caja", self.mostrarCaja)
        self.create_menu_button("Entrada Productos", self.mostrarProductos)
        self.create_menu_button("Clientes", self.mostrarClientes)
        self.create_menu_button("Proveedores", self.mostrarProveedor)
        self.create_menu_button("Venta", self.mostrarVenta)
        self.create_menu_button("Stock", self.mostrarStock)
        self.create_menu_button("Administrador", self.mostrarAdmin)
        
        # Botón Salir
        self.btnSalir = tk.Button(self.frame_sidebar, text="Cerrar Sesión", command=self.salir,
                                font=('Segoe UI', 11), fg=self.text_color, bg='#c0392b',
                                relief='flat', cursor='hand2', anchor='w', padx=20)
        self.btnSalir.pack(side='bottom', fill='x', pady=20, padx=10)

        # Ocultar botones inicialmente
        self.hide_menu()

    def create_menu_button(self, text, command):
        btn = tk.Button(self.frame_sidebar, text=text, command=command,
                       font=('Segoe UI', 11), fg=self.text_color, bg=self.primary_color,
                       relief='flat', cursor='hand2', anchor='w', padx=20)
        
        # Hover effects
        btn.bind('<Enter>', lambda e: btn.config(bg=self.hover_color))
        btn.bind('<Leave>', lambda e: btn.config(bg=self.primary_color))
        
        self.menu_buttons.append(btn)
        return btn

    def show_menu(self):
        for btn in self.menu_buttons:
            btn.pack(fill='x', pady=2)
            
    def hide_menu(self):
        for btn in self.menu_buttons:
            btn.pack_forget()

    def iniciar_sesion(self):
        usuario = self.entry_usuario.get()
        contraseña = self.entry_contraseña.get()

        conexion = conexionBD()
        if not conexion:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            return

        cursor = conexion.cursor()
        cursor.execute("SELECT idEmpleado FROM usuario WHERE correo=%s AND contrasena=%s AND estado=1", (usuario, contraseña))
        resultado = cursor.fetchone()

        if resultado:
            id_empleado = resultado[0]
            cursor.execute("SELECT Rol_idRol FROM empleado WHERE idEmpleado=%s", (id_empleado,))
            rol_resultado = cursor.fetchone()
            
            if rol_resultado:
                rol_id = rol_resultado[0]
                self.usuario_actual = usuario
                self.show_menu()
                
                # Gestionar visibilidad de admin
                if rol_id != 1:
                    # Encontrar y ocultar botón admin (el último en la lista)
                    self.menu_buttons[-1].pack_forget()
                
                self.frame_login.place_forget()
                # Mostrar pantalla por defecto (ej. Venta o Caja)
                self.mostrarCaja()
            else:
                messagebox.showerror("Error", "No se encontró el rol del usuario.")
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
        
        cursor.close()
        conexion.close()

    def switch_frame(self, frame_class):
        # Limpiar frame principal
        for widget in self.frame_main.winfo_children():
            widget.destroy()
            
        # Crear nuevo frame
        frame = frame_class(self.frame_main, width=1080, height=720)
        frame.pack(fill='both', expand=True)

    def mostrarDashboard(self): self.switch_frame(DashboardView)
    def mostrarCaja(self): self.switch_frame(Frame_Caja)
    def mostrarProductos(self): self.switch_frame(Frame_Producto)
    def mostrarClientes(self): self.switch_frame(Frame_Cliente)
    def mostrarVenta(self): self.switch_frame(Frame_Venta)
    def mostrarProveedor(self): self.switch_frame(Frame_Proveedor)
    def mostrarStock(self): self.switch_frame(Frame_Stock)
    def mostrarAdmin(self): self.switch_frame(Frame_Admin)
        
    def salir(self):
        self.destroy()



