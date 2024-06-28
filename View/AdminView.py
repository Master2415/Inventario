import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkcalendar import *
from View.RolView import *
from View.EmpleadoView import *
from View.UsuarioView import *
from View.ResumenView import *

class Frame_Admin(tk.Frame):

    def __init__(self, root, width=1745, height=750):
        super().__init__(root, width=width, height=height)
        self.root = root
        self.config(bg='#f0f0f0')  # Establecer el color de fondo del frame principal
        self.pack(fill='both', expand=True)
        self.current_frame = None  # Variable para guardar el frame actual
        self.framebtn()


    def framebtn(self):
        self.btn_frame = tk.Frame(self, bg='#BBBBBB')
        self.btn_frame.pack(fill='x', padx=20, pady=10)

        self.btnRol = tk.Button(self.btn_frame, text='ROL')
        self.btnRol.config(width=20, font=('Arial', 12, 'bold'), fg='#ffffff', bg='#007ACC', command=self.mostrarRol)
        self.btnRol.grid(column=1, row=0, padx=10, pady=5)

        self.btnEmpleado = tk.Button(self.btn_frame, text='Empleados', command=self.mostrarEmpleados)
        self.btnEmpleado.config(width=20, font=('Arial', 12, 'bold'), fg='#ffffff', bg='#007ACC')
        self.btnEmpleado.grid(column=2, row=0, padx=10, pady=5)

        self.btnUsers = tk.Button(self.btn_frame, text='Usuarios', command=self.mostrarUsuarios)
        self.btnUsers.config(width=20, font=('Arial', 12, 'bold'), fg='#ffffff', bg='#007ACC')
        self.btnUsers.grid(column=3, row=0, padx=10, pady=5)

        self.btnResumen = tk.Button(self.btn_frame, text='Resumen Inventario', command=self.mostrarResumen)
        self.btnResumen.config(width=20, font=('Arial', 12, 'bold'), fg='#ffffff', bg='#E8B200')
        self.btnResumen.grid(column=0, row=1, padx=10, pady=5)

        self.btnResumenventa = tk.Button(self.btn_frame, text='Resumen Ventas', command=self.mostrarResumenVentas)
        self.btnResumenventa.config(width=20, font=('Arial', 12, 'bold'), fg='#ffffff', bg='#E8B200')
        self.btnResumenventa.grid(column=1, row=1, padx=10, pady=5)

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

    def _mostrar_frame(self, FrameClass):
        # Destruir el frame actual si existe
        if self.current_frame is not None:
            self.current_frame.destroy()

        # Crear el nuevo frame
        self.current_frame = FrameClass(self)
        self.current_frame.pack(pady=10)