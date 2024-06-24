import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import *
from Model.ProductoDAO import *
from Model.ProveedorDAO import *

class RolView(tk.Toplevel):
    def __init__(self, root, width=1280, height=720):
        super().__init__(root, width=width, height=height)
        self.root = root
        self.config(bg='#f0f0f0')  # Establecer el color de fondo del frame principal
        self.pack(fill='both', expand=True)
     
        