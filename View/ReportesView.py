import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
import csv
from datetime import datetime
from Model.ReportesDAO import obtener_ventas_rango, listarProductos, listarClientes, listarEmpleado

class ReportesView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Generar Reportes CSV")
        self.geometry("800x600")
        self.config(bg='#f0f2f5')
        self.resizable(True, True)
        
        # Título
        lbl_titulo = tk.Label(self, text="Panel de Reportes", font=('Segoe UI', 20, 'bold'), bg='#f0f2f5', fg='#2c3e50')
        lbl_titulo.pack(pady=20)

        # Frame principal
        main_frame = tk.Frame(self, bg='#f0f2f5')
        main_frame.pack(fill='both', expand=True, padx=40)

        # --- Sección Ventas (con rango de fechas) ---
        frame_ventas = tk.LabelFrame(main_frame, text="Reporte de Ventas", font=('Segoe UI', 12, 'bold'), bg='#f0f2f5', fg='#34495e')
        frame_ventas.pack(fill='x', pady=10, ipady=10)

        tk.Label(frame_ventas, text="Desde:", bg='#f0f2f5', font=('Segoe UI', 10)).grid(row=0, column=0, padx=10, pady=5)
        self.cal_inicio = DateEntry(frame_ventas, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.cal_inicio.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(frame_ventas, text="Hasta:", bg='#f0f2f5', font=('Segoe UI', 10)).grid(row=0, column=2, padx=10, pady=5)
        self.cal_fin = DateEntry(frame_ventas, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.cal_fin.grid(row=0, column=3, padx=10, pady=5)

        btn_ventas = tk.Button(frame_ventas, text="Exportar Ventas", command=self.exportar_ventas,
                               font=('Segoe UI', 10, 'bold'), bg='#27ae60', fg='white', relief='flat', cursor='hand2')
        btn_ventas.grid(row=0, column=4, padx=20, pady=5)

        # --- Sección Otros Reportes ---
        frame_otros = tk.LabelFrame(main_frame, text="Otros Reportes", font=('Segoe UI', 12, 'bold'), bg='#f0f2f5', fg='#34495e')
        frame_otros.pack(fill='x', pady=10, ipady=10)

        # Inventario
        btn_inventario = tk.Button(frame_otros, text="Exportar Inventario Completo", command=self.exportar_inventario,
                                   font=('Segoe UI', 11), bg='#3498db', fg='white', relief='flat', cursor='hand2', width=30)
        btn_inventario.pack(pady=10)

        # Clientes
        btn_clientes = tk.Button(frame_otros, text="Exportar Lista de Clientes", command=self.exportar_clientes,
                                 font=('Segoe UI', 11), bg='#9b59b6', fg='white', relief='flat', cursor='hand2', width=30)
        btn_clientes.pack(pady=10)

        # Empleados
        btn_empleados = tk.Button(frame_otros, text="Exportar Lista de Empleados", command=self.exportar_empleados,
                                  font=('Segoe UI', 11), bg='#e67e22', fg='white', relief='flat', cursor='hand2', width=30)
        btn_empleados.pack(pady=10)

    def exportar_csv(self, data, headers, default_name):
        if not data:
            messagebox.showwarning("Advertencia", "No hay datos para exportar.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                                                 initialfile=default_name)
        if not file_path:
            return

        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(headers)
                writer.writerows(data)
            messagebox.showinfo("Éxito", f"Reporte guardado correctamente en:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")

    def exportar_ventas(self):
        fecha_inicio = self.cal_inicio.get_date()
        fecha_fin = self.cal_fin.get_date()
        
        if fecha_inicio > fecha_fin:
            messagebox.showerror("Error", "La fecha de inicio no puede ser mayor a la fecha fin.")
            return

        data = obtener_ventas_rango(fecha_inicio, fecha_fin)
        # Estructura de data (según ReportesDAO): idVenta, total, fecha, correo_usuario, cedula_cliente, nombre_cliente, apellido_cliente
        headers = ["ID Venta", "Total", "Fecha", "Usuario (Correo)", "Cédula Cliente", "Nombre Cliente", "Apellido Cliente"]
        
        filename = f"Reporte_Ventas_{fecha_inicio}_{fecha_fin}.csv"
        self.exportar_csv(data, headers, filename)

    def exportar_inventario(self):
        raw_data = listarProductos()
        # Estructura de raw_data (según ProductoDAO.listarProductos):
        # idProducto, codigo, nombre_productostock, tipo_productostock, cantidadStock, precio, fechaIngreso, nombre_proveedor
        
        # Mapeamos o filtramos si es necesario, pero listarProductos ya trae lo que queremos.
        # Solo necesitamos asegurarnos de que los datos coincidan con los encabezados.
        headers = ["ID", "Código", "Producto", "Tipo", "Stock", "Precio", "Fecha Ingreso", "Proveedor"]
        
        filename = f"Reporte_Inventario_{datetime.now().strftime('%Y-%m-%d')}.csv"
        self.exportar_csv(raw_data, headers, filename)

    def exportar_clientes(self):
        raw_data = listarClientes()
        # Estructura de raw_data (según ClienteDao.listarClientes):
        # id, cedula, nombre, apellido, direccion, correo, telefono, ciudad, tipo_cliente
        
        # Quitamos el ID interno si no es relevante, o lo dejamos. Dejémoslo.
        # Pero listarClientes devuelve una lista de tuplas, así que pasamos directo.
        headers = ["ID", "Cédula", "Nombre", "Apellido", "Dirección", "Correo", "Teléfono", "Ciudad", "Tipo"]
        
        filename = f"Reporte_Clientes_{datetime.now().strftime('%Y-%m-%d')}.csv"
        self.exportar_csv(raw_data, headers, filename)

    def exportar_empleados(self):
        raw_data = listarEmpleado()
        # Estructura de raw_data (según EmpleadoDAO.listarEmpleado):
        # id, cedula, nombre, apellido, direccion, correo, telefono, ciudad, horas_trabajadas, fecha_contrato, cargo
        
        headers = ["ID", "Cédula", "Nombre", "Apellido", "Dirección", "Correo", "Teléfono", "Ciudad", "Horas Trab.", "Fecha Contrato", "Cargo"]
        
        filename = f"Reporte_Empleados_{datetime.now().strftime('%Y-%m-%d')}.csv"
        self.exportar_csv(raw_data, headers, filename)
