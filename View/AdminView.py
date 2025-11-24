import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkcalendar import *
from View.RolView import *
from View.EmpleadoView import *
from View.UsuarioView import *
from View.ResumenView import *
from View.UtilidadView import *
from View.ReportesView import ReportesView
from View.NominaView import NominaView
from View.ConfiguracionView import ConfiguracionView

class Frame_Admin(tk.Frame):

    def __init__(self, root, width=1745, height=750):
        super().__init__(root, width=width, height=height)
        self.root = root
        self.config(bg='#f0f2f5')  # Establecer el color de fondo del frame principal
        self.pack(fill='both', expand=True)
        self.current_frame = None  # Variable para guardar el frame actual
        self.framebtn()


    def framebtn(self):
        self.btn_frame = tk.Frame(self, bg='#f0f2f5')
        self.btn_frame.pack(pady=10)

        self.btnRol = tk.Button(self.btn_frame, text='ROL')
        self.btnRol.config(width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#3498db', relief='flat', cursor='hand2', command=self.mostrarRol)
        self.btnRol.grid(column=0, row=0, padx=10, pady=5)

        self.btnEmpleado = tk.Button(self.btn_frame, text='Empleados', command=self.mostrarEmpleados)
        self.btnEmpleado.config(width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#3498db', relief='flat', cursor='hand2')
        self.btnEmpleado.grid(column=1, row=0, padx=10, pady=5)

        self.btnUsers = tk.Button(self.btn_frame, text='Usuarios', command=self.mostrarUsuarios)
        self.btnUsers.config(width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#3498db', relief='flat', cursor='hand2')
        self.btnUsers.grid(column=2, row=0, padx=10, pady=5)

        self.btnResumen = tk.Button(self.btn_frame, text='Resumen Inventario', command=self.mostrarResumen)
        self.btnResumen.config(width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#f39c12', relief='flat', cursor='hand2')
        self.btnResumen.grid(column=0, row=1, padx=10, pady=5)

        self.btnResumenventa = tk.Button(self.btn_frame, text='Resumen Ventas', command=self.mostrarResumenVentas)
        self.btnResumenventa.config(width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#f39c12', relief='flat', cursor='hand2')
        self.btnResumenventa.grid(column=1, row=1, padx=10, pady=5)

        self.btnResumCompra = tk.Button(self.btn_frame, text='Resumen Compras', command=self.mostrarResumenCompra)
        self.btnResumCompra.config(width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#f39c12', relief='flat', cursor='hand2')
        self.btnResumCompra.grid(column=2, row=1, padx=10, pady=5)
        
        # Nómina (Ahora arriba de Utilidad o en una posición lógica)
        self.btnNomina = tk.Button(self.btn_frame, text='Nómina', command=self.mostrarNomina)
        self.btnNomina.config(width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#27ae60', relief='flat', cursor='hand2')
        self.btnNomina.grid(column=3, row=1, padx=10, pady=5)

        self.btnUtilidad = tk.Button(self.btn_frame, text='Utilidad', command=self.mostrarUtilidad)
        self.btnUtilidad.config(width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#8e44ad', relief='flat', cursor='hand2')
        self.btnUtilidad.grid(column=4, row=1, padx=10, pady=5)

        self.btnReportes = tk.Button(self.btn_frame, text='Reportes CSV', command=self.mostrarReportes)
        self.btnReportes.config(width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#2c3e50', relief='flat', cursor='hand2')
        self.btnReportes.grid(column=0, row=2, padx=10, pady=5)
        
        self.btnConfig = tk.Button(self.btn_frame, text='Configuración', command=self.mostrarConfiguracion)
        self.btnConfig.config(width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#7f8c8d', relief='flat', cursor='hand2')
        self.btnConfig.grid(column=1, row=2, padx=10, pady=5)

    def mostrarUtilidad(self):
        self._mostrar_frame(UtilidadView)

    def mostrarResumenCompra(self):
        self._mostrar_frame(ListadoProductosCompra)

    def mostrarRol(self):
        self._mostrar_frame(RolView)

    def mostrarEmpleados(self):
        self._mostrar_frame(EmpleadoView)

    def mostrarUsuarios(self):
        self._mostrar_frame(UsuarioView)
    
    def mostrarResumen(self):
        self._mostrar_frame(Frame_Resumen)

    def mostrarResumenVentas(self):
        self._mostrar_frame(Frame_ResumenVentas)

    def mostrarReportes(self):
        ReportesView(self)
        
    def mostrarNomina(self):
        self._mostrar_frame(NominaView)
        
    def mostrarConfiguracion(self):
        self._mostrar_frame(ConfiguracionView)

    def _mostrar_frame(self, FrameClass):
        # Destruir el frame actual si existe
        if self.current_frame is not None:
            self.current_frame.destroy()

        # Crear el nuevo frame
        self.current_frame = FrameClass(self)
        self.current_frame.pack(pady=10)