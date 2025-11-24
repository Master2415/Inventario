import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from Model.UtilidadDAO import *
from Model.NominaDAO import calcular_nomina_rango

class UtilidadView(tk.Frame):
    def __init__(self, root, width=1745, height=750):
        super().__init__(root, width=width, height=height)
        self.root = root
        self.config(bg='#f0f2f5')
        self.pack(fill='both', expand=True)
        
        self.ventas_totales = 0.0
        self.compras_totales = 0.0
        self.utilidad_bruta = 0.0
        self.costo_nomina = 0.0
        
        self.create_widgets()
        
    def create_widgets(self):
        # Título
        lbl_titulo = tk.Label(self, text="Cálculo de Utilidad", font=('Segoe UI', 20, 'bold'), bg='#f0f2f5')
        lbl_titulo.pack(pady=20)
        
        # Frame de Fechas
        frame_fechas = tk.Frame(self, bg='#f0f2f5')
        frame_fechas.pack(pady=10)
        
        tk.Label(frame_fechas, text="Fecha Inicio:", font=('Segoe UI', 12), bg='#f0f2f5').pack(side='left', padx=5)
        self.cal_inicio = DateEntry(frame_fechas, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='y-mm-dd')
        self.cal_inicio.pack(side='left', padx=5)
        
        tk.Label(frame_fechas, text="Fecha Fin:", font=('Segoe UI', 12), bg='#f0f2f5').pack(side='left', padx=5)
        self.cal_fin = DateEntry(frame_fechas, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='y-mm-dd')
        self.cal_fin.pack(side='left', padx=5)
        
        btn_calcular = tk.Button(frame_fechas, text="Calcular Utilidad", command=self.calcular_utilidad,
                               font=('Segoe UI', 11, 'bold'), fg='#ffffff', bg='#3498db', relief='flat', cursor='hand2')
        btn_calcular.pack(side='left', padx=20)
        
        # Frame de Resultados de Utilidad
        frame_resultados = tk.Frame(self, bg='#ffffff', bd=1, relief='solid')
        frame_resultados.pack(pady=20, padx=50, fill='x')
        
        self.lbl_ventas = tk.Label(frame_resultados, text="Ventas Totales: $0.00", font=('Segoe UI', 14), bg='#ffffff', fg='#27ae60')
        self.lbl_ventas.grid(row=0, column=0, padx=20, pady=10, sticky='w')
        
        self.lbl_compras = tk.Label(frame_resultados, text="Compras Totales: $0.00", font=('Segoe UI', 14), bg='#ffffff', fg='#c0392b')
        self.lbl_compras.grid(row=1, column=0, padx=20, pady=10, sticky='w')
        
        ttk.Separator(frame_resultados, orient='horizontal').grid(row=2, column=0, sticky='ew', padx=10, pady=5)
        
        self.lbl_utilidad_bruta = tk.Label(frame_resultados, text="Utilidad Bruta: $0.00", font=('Segoe UI', 16, 'bold'), bg='#ffffff')
        self.lbl_utilidad_bruta.grid(row=3, column=0, padx=20, pady=10, sticky='w')
        
        # Sección de Costos Operativos (Nómina)
        ttk.Separator(frame_resultados, orient='horizontal').grid(row=4, column=0, sticky='ew', padx=10, pady=5)
        
        self.lbl_costo_nomina = tk.Label(frame_resultados, text="Costo Nómina (Pagos Realizados): $0.00", font=('Segoe UI', 14), bg='#ffffff', fg='#c0392b')
        self.lbl_costo_nomina.grid(row=5, column=0, padx=20, pady=10, sticky='w')
        
        ttk.Separator(frame_resultados, orient='horizontal').grid(row=6, column=0, sticky='ew', padx=10, pady=5)
        
        self.lbl_utilidad_neta = tk.Label(frame_resultados, text="Utilidad Neta: $0.00", font=('Segoe UI', 18, 'bold'), bg='#ffffff', fg='#2980b9')
        self.lbl_utilidad_neta.grid(row=7, column=0, padx=20, pady=20, sticky='w')

    def calcular_utilidad(self):
        fecha_inicio = self.cal_inicio.get_date()
        fecha_fin = self.cal_fin.get_date()
        
        # Calcular Ventas y Compras
        self.ventas_totales = calcular_ventas_totales(fecha_inicio, fecha_fin)
        self.compras_totales = calcular_compras_totales(fecha_inicio, fecha_fin)
        self.utilidad_bruta = self.ventas_totales - self.compras_totales
        
        # Calcular Nómina (Pagos registrados en el rango)
        self.costo_nomina = float(calcular_nomina_rango(fecha_inicio, fecha_fin))
        
        # Calcular Utilidad Neta
        self.utilidad_neta = self.utilidad_bruta - self.costo_nomina
        
        # Actualizar Labels
        self.lbl_ventas.config(text=f"Ventas Totales: ${self.ventas_totales:,.2f}")
        self.lbl_compras.config(text=f"Compras Totales: ${self.compras_totales:,.2f}")
        self.lbl_utilidad_bruta.config(text=f"Utilidad Bruta: ${self.utilidad_bruta:,.2f}")
        self.lbl_costo_nomina.config(text=f"Costo Nómina (Pagos Realizados): ${self.costo_nomina:,.2f}")
        self.lbl_utilidad_neta.config(text=f"Utilidad Neta: ${self.utilidad_neta:,.2f}")
