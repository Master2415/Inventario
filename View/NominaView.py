import tkinter as tk
from tkinter import ttk, messagebox
from Model.NominaDAO import *

class NominaView(tk.Frame):
    def __init__(self, root, width=1745, height=750):
        super().__init__(root, width=width, height=height)
        self.root = root
        self.config(bg='#f0f2f5')
        self.pack(fill='both', expand=True)
        
        # Asegurar que la tabla existe
        crear_tabla_nomina()
        
        self.empleados = [] # Lista de tuplas (id, nombre, horas)
        self.empleado_seleccionado = None
        self.tipo_pago = tk.StringVar(value="HORA")
        
        self.create_widgets()
        self.cargar_empleados()
        
    def create_widgets(self):
        # Título
        tk.Label(self, text="Gestión de Nómina", font=('Segoe UI', 24, 'bold'), bg='#f0f2f5', fg='#2c3e50').pack(pady=30)
        
        # Contenedor principal
        main_frame = tk.Frame(self, bg='white', padx=40, pady=40)
        main_frame.pack(padx=20, pady=10)
        main_frame.configure(highlightbackground="#d1d1d1", highlightthickness=1)
        
        # Selección de Empleado
        tk.Label(main_frame, text="Seleccionar Empleado:", font=('Segoe UI', 12), bg='white').grid(row=0, column=0, sticky='w', pady=10)
        
        self.combo_empleados = ttk.Combobox(main_frame, font=('Segoe UI', 12), width=30, state="readonly")
        self.combo_empleados.grid(row=0, column=1, padx=20, pady=10)
        self.combo_empleados.bind("<<ComboboxSelected>>", self.on_empleado_selected)
        
        # Información del Empleado
        self.lbl_info_horas = tk.Label(main_frame, text="Horas Trabajadas: 0", font=('Segoe UI', 12, 'bold'), bg='white', fg='#7f8c8d')
        self.lbl_info_horas.grid(row=1, column=0, columnspan=2, sticky='w', pady=10)
        
        ttk.Separator(main_frame, orient='horizontal').grid(row=2, column=0, columnspan=2, sticky='ew', pady=20)
        
        # Tipo de Pago
        tk.Label(main_frame, text="Tipo de Pago:", font=('Segoe UI', 12), bg='white').grid(row=3, column=0, sticky='w', pady=10)
        
        frame_radios = tk.Frame(main_frame, bg='white')
        frame_radios.grid(row=3, column=1, sticky='w', padx=20)
        
        tk.Radiobutton(frame_radios, text="Pago por Hora", variable=self.tipo_pago, value="HORA", 
                      command=self.update_input_label, bg='white', font=('Segoe UI', 11)).pack(side='left', padx=10)
        tk.Radiobutton(frame_radios, text="Monto Fijo (Bono/Adelanto)", variable=self.tipo_pago, value="FIJO", 
                      command=self.update_input_label, bg='white', font=('Segoe UI', 11)).pack(side='left', padx=10)
        
        # Entrada de Valor
        self.lbl_input = tk.Label(main_frame, text="Valor por Hora ($):", font=('Segoe UI', 12), bg='white')
        self.lbl_input.grid(row=4, column=0, sticky='w', pady=10)
        
        self.entry_valor = tk.Entry(main_frame, font=('Segoe UI', 12), width=15)
        self.entry_valor.grid(row=4, column=1, sticky='w', padx=20, pady=10)
        self.entry_valor.bind('<KeyRelease>', self.calcular_total_preview)
        
        # Total a Pagar (Preview)
        self.lbl_total = tk.Label(main_frame, text="Total a Pagar: $0.00", font=('Segoe UI', 16, 'bold'), bg='white', fg='#27ae60')
        self.lbl_total.grid(row=5, column=0, columnspan=2, pady=20)
        
        # Botón Pagar
        btn_pagar = tk.Button(main_frame, text="Realizar Pago", command=self.realizar_pago,
                            font=('Segoe UI', 12, 'bold'), fg='white', bg='#27ae60', relief='flat', cursor='hand2', width=20)
        btn_pagar.grid(row=6, column=0, columnspan=2, pady=20)
        
    def cargar_empleados(self):
        self.empleados = obtener_empleados_para_nomina()
        values = [f"{emp[1]} (ID: {emp[0]})" for emp in self.empleados]
        self.combo_empleados['values'] = values
        
    def on_empleado_selected(self, event):
        idx = self.combo_empleados.current()
        if idx >= 0:
            self.empleado_seleccionado = self.empleados[idx]
            # Actualizar label de horas
            horas = self.empleado_seleccionado[2]
            self.lbl_info_horas.config(text=f"Horas Trabajadas: {horas}")
            self.calcular_total_preview()
            
    def update_input_label(self):
        tipo = self.tipo_pago.get()
        if tipo == "HORA":
            self.lbl_input.config(text="Valor por Hora ($):")
        else:
            self.lbl_input.config(text="Monto a Pagar ($):")
        self.calcular_total_preview()
            
    def calcular_total_preview(self, event=None):
        if not self.empleado_seleccionado:
            self.lbl_total.config(text="Total a Pagar: $0.00")
            return
            
        try:
            valor_str = self.entry_valor.get()
            if not valor_str:
                valor = 0.0
            else:
                valor = float(valor_str)
                
            tipo = self.tipo_pago.get()
            total = 0.0
            
            if tipo == "HORA":
                horas = float(self.empleado_seleccionado[2])
                total = horas * valor
            else:
                total = valor
                
            self.lbl_total.config(text=f"Total a Pagar: ${total:,.2f}")
            
        except ValueError:
            self.lbl_total.config(text="Total a Pagar: $0.00")
            
    def realizar_pago(self):
        if not self.empleado_seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un empleado")
            return
            
        try:
            valor = float(self.entry_valor.get())
            if valor <= 0:
                messagebox.showwarning("Advertencia", "El valor debe ser mayor a 0")
                return
                
            tipo = self.tipo_pago.get()
            id_empleado = self.empleado_seleccionado[0]
            horas = float(self.empleado_seleccionado[2])
            
            monto_total = 0.0
            horas_pagadas = 0
            
            if tipo == "HORA":
                if horas <= 0:
                    messagebox.showwarning("Advertencia", "El empleado no tiene horas trabajadas para pagar.")
                    return
                monto_total = horas * valor
                horas_pagadas = horas
            else:
                monto_total = valor
                horas_pagadas = 0
                
            confirm = messagebox.askyesno("Confirmar Pago", f"¿Está seguro de registrar un pago de ${monto_total:,.2f} a {self.empleado_seleccionado[1]}?")
            
            if confirm:
                exito = registrar_pago(id_empleado, monto_total, tipo, horas_pagadas)
                if exito:
                    messagebox.showinfo("Éxito", "Pago registrado correctamente")
                    self.entry_valor.delete(0, 'end')
                    self.lbl_total.config(text="Total a Pagar: $0.00")
                    # Recargar empleados para actualizar horas
                    self.cargar_empleados()
                    self.combo_empleados.set('')
                    self.empleado_seleccionado = None
                    self.lbl_info_horas.config(text="Horas Trabajadas: 0")
                else:
                    messagebox.showerror("Error", "No se pudo registrar el pago")
                    
        except ValueError:
            messagebox.showerror("Error", "Ingrese un valor numérico válido")
