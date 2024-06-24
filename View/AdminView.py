import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import *
from View.RolView import *
from View.EmpleadoView import *


class Frame_Admin(tk.Frame):

    def __init__(self, root, width=1745, height=750):
        super().__init__(root, width=width, height=height)
        self.root = root
        self.config(bg='#f0f0f0')  # Establecer el color de fondo del frame principal
        self.pack(fill='both', expand=True)
     
        #self.frameBuscar()
        self.framebtn()
        #self.btnBuscar.config(command=self.buscarCliente) 

    def frameBuscar(self):
        self.buscar_frame = tk.Frame(self, bg='#f0f0f0')
        self.buscar_frame.pack(pady=10)

    def framebtn(self):
        self.btn_frame = tk.Frame(self, bg='#BBBBBB')
        self.btn_frame.pack(pady=10)

        self.btnRol = tk.Button(self.btn_frame, text='ROL')
        self.btnRol.config(width=20, font=('Arial', 12, 'bold'), fg='#ffffff', bg='#007ACC')
        self.btnRol.grid(column=1, row=0, padx=10, pady=5)

        self.btnEmpleado = tk.Button(self.btn_frame, text='Empleados', command=self.mostrarEmpleados)
        self.btnEmpleado.config(width=20, font=('Arial', 12, 'bold'), fg='#ffffff', bg='#007ACC')
        self.btnEmpleado.grid(column=2, row=0, padx=10, pady=5)

    def mostrarRol():
        RolView()

    def mostrarEmpleados(self):
        EmpleadoView(self)