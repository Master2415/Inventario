import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from Model.DashboardDAO import *
from datetime import datetime, timedelta

class DashboardView(tk.Frame):
    def __init__(self, root, width=1745, height=750):
        super().__init__(root, width=width, height=height)
        self.root = root
        self.config(bg='#f0f2f5')
        self.pack(fill='both', expand=True)
        
        self.create_widgets()
        self.cargar_datos_iniciales()

    def create_widgets(self):
        # Título
        lbl_titulo = tk.Label(self, text="Dashboard General", font=('Segoe UI', 24, 'bold'), bg='#f0f2f5', fg='#2c3e50')
        lbl_titulo.pack(pady=20)

        # Frame de Filtros (Fechas)
        frame_filtros = tk.Frame(self, bg='#f0f2f5')
        frame_filtros.pack(pady=10)

        tk.Label(frame_filtros, text="Desde:", font=('Segoe UI', 12), bg='#f0f2f5').pack(side='left', padx=5)
        self.cal_inicio = DateEntry(frame_filtros, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='y-mm-dd')
        self.cal_inicio.pack(side='left', padx=5)

        tk.Label(frame_filtros, text="Hasta:", font=('Segoe UI', 12), bg='#f0f2f5').pack(side='left', padx=5)
        self.cal_fin = DateEntry(frame_filtros, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='y-mm-dd')
        self.cal_fin.pack(side='left', padx=5)

        btn_actualizar = tk.Button(frame_filtros, text="Actualizar Dashboard", command=self.actualizar_dashboard,
                                 font=('Segoe UI', 11, 'bold'), fg='#ffffff', bg='#3498db', relief='flat', cursor='hand2')
        btn_actualizar.pack(side='left', padx=20)

        # KPI Card (Total Ventas)
        self.frame_kpi = tk.Frame(self, bg='#ffffff', bd=1, relief='solid')
        self.frame_kpi.pack(pady=20, padx=50, fill='x')

        lbl_kpi_titulo = tk.Label(self.frame_kpi, text="Ventas Totales (Periodo Seleccionado)", font=('Segoe UI', 14), bg='#ffffff', fg='#7f8c8d')
        lbl_kpi_titulo.pack(pady=10)

        self.lbl_total_ventas = tk.Label(self.frame_kpi, text="$0.00", font=('Segoe UI', 36, 'bold'), bg='#ffffff', fg='#27ae60')
        self.lbl_total_ventas.pack(pady=10)

        # Frame Contenedor de Tablas
        frame_tablas = tk.Frame(self, bg='#f0f2f5')
        frame_tablas.pack(fill='both', expand=True, padx=20, pady=10)

        # Tabla Top Productos
        frame_top = tk.LabelFrame(frame_tablas, text="Top 5 Productos Más Vendidos", font=('Segoe UI', 12, 'bold'), bg='#f0f2f5')
        frame_top.pack(side='left', fill='both', expand=True, padx=10)

        self.tree_top = ttk.Treeview(frame_top, columns=('Producto', 'Cantidad'), show='headings', height=10)
        self.tree_top.heading('Producto', text='Producto')
        self.tree_top.heading('Cantidad', text='Cantidad Vendida')
        self.tree_top.column('Producto', width=200)
        self.tree_top.column('Cantidad', width=100, anchor='center')
        self.tree_top.pack(fill='both', expand=True, padx=5, pady=5)

        # Tabla Bajo Stock
        frame_stock = tk.LabelFrame(frame_tablas, text="Alerta: Productos Próximos a Agotarse (<10)", font=('Segoe UI', 12, 'bold'), bg='#f0f2f5', fg='#c0392b')
        frame_stock.pack(side='right', fill='both', expand=True, padx=10)

        self.tree_stock = ttk.Treeview(frame_stock, columns=('Producto', 'Stock'), show='headings', height=10)
        self.tree_stock.heading('Producto', text='Producto')
        self.tree_stock.heading('Stock', text='Stock Actual')
        self.tree_stock.column('Producto', width=200)
        self.tree_stock.column('Stock', width=100, anchor='center')
        self.tree_stock.pack(fill='both', expand=True, padx=5, pady=5)

    def cargar_datos_iniciales(self):
        # Por defecto, cargar mes actual
        hoy = datetime.now()
        inicio_mes = hoy.replace(day=1)
        self.cal_inicio.set_date(inicio_mes)
        self.cal_fin.set_date(hoy)
        self.actualizar_dashboard()

    def actualizar_dashboard(self):
        fecha_inicio = self.cal_inicio.get_date()
        fecha_fin = self.cal_fin.get_date()

        # 1. Actualizar KPI Ventas
        total_ventas = obtener_ventas_por_rango(fecha_inicio, fecha_fin)
        self.lbl_total_ventas.config(text=f"${total_ventas:,.2f}")

        # 2. Actualizar Top Productos
        self.tree_top.delete(*self.tree_top.get_children())
        top_productos = obtener_top_productos()
        for prod in top_productos:
            self.tree_top.insert('', 'end', values=(prod[0], int(prod[1])))

        # 3. Actualizar Bajo Stock
        self.tree_stock.delete(*self.tree_stock.get_children())
        bajo_stock = obtener_bajo_stock()
        for prod in bajo_stock:
            self.tree_stock.insert('', 'end', values=(prod[0], int(prod[1])))
