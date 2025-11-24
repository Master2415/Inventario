import tkinter as tk
from tkinter import ttk, messagebox
from Model.ConfiguracionDAO import *

class ConfiguracionView(tk.Frame):
    def __init__(self, root, width=1745, height=750):
        super().__init__(root, width=width, height=height)
        self.root = root
        self.config(bg='#f0f2f5')
        self.pack(fill='both', expand=True)
        
        crear_tabla_configuracion()
        self.create_widgets()
        self.cargar_datos()
        
    def create_widgets(self):
        tk.Label(self, text="Configuración de Empresa", font=('Segoe UI', 24, 'bold'), bg='#f0f2f5', fg='#2c3e50').pack(pady=30)
        
        main_frame = tk.Frame(self, bg='white', padx=40, pady=40)
        main_frame.pack(padx=20, pady=10)
        main_frame.configure(highlightbackground="#d1d1d1", highlightthickness=1)
        
        # Campos
        self.entries = {}
        campos = [
            ("Nombre Empresa:", "nombre_empresa"),
            ("NIT / RUT:", "nit_rut"),
            ("Dirección:", "direccion"),
            ("Teléfono:", "telefono"),
            ("Slogan:", "slogan"),
            ("Mensaje Final Recibo:", "mensaje_final")
        ]
        
        for i, (label_text, key) in enumerate(campos):
            tk.Label(main_frame, text=label_text, font=('Segoe UI', 12), bg='white').grid(row=i, column=0, sticky='w', pady=10)
            entry = tk.Entry(main_frame, font=('Segoe UI', 12), width=40)
            entry.grid(row=i, column=1, padx=20, pady=10)
            self.entries[key] = entry
            
        btn_guardar = tk.Button(main_frame, text="Guardar Configuración", command=self.guardar,
                              font=('Segoe UI', 12, 'bold'), fg='white', bg='#27ae60', relief='flat', cursor='hand2', width=25)
        btn_guardar.grid(row=len(campos), column=0, columnspan=2, pady=30)
        
    def cargar_datos(self):
        config = obtener_configuracion()
        if config:
            self.entries['nombre_empresa'].insert(0, config['nombre_empresa'])
            self.entries['nit_rut'].insert(0, config['nit_rut'])
            self.entries['direccion'].insert(0, config['direccion'])
            self.entries['telefono'].insert(0, config['telefono'])
            self.entries['slogan'].insert(0, config['slogan'])
            self.entries['mensaje_final'].insert(0, config['mensaje_final'])
            
    def guardar(self):
        nombre = self.entries['nombre_empresa'].get()
        nit = self.entries['nit_rut'].get()
        direccion = self.entries['direccion'].get()
        telefono = self.entries['telefono'].get()
        slogan = self.entries['slogan'].get()
        mensaje = self.entries['mensaje_final'].get()
        
        if guardar_configuracion(nombre, nit, direccion, telefono, slogan, mensaje):
            messagebox.showinfo("Éxito", "Configuración guardada correctamente")
        else:
            messagebox.showerror("Error", "No se pudo guardar la configuración")
