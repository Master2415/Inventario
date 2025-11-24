import tkinter as tk
from tkinter import Toplevel, Text, Scrollbar
from datetime import datetime
from Model.ConfiguracionDAO import obtener_configuracion

class ReciboGenerator:
    def __init__(self, root, venta_data, detalles_venta, cliente_nombre):
        self.root = root
        self.venta_data = venta_data # {id, total, fecha, cajero}
        self.detalles_venta = detalles_venta # list of {producto, cantidad, precio, subtotal}
        self.cliente_nombre = cliente_nombre
        self.config = obtener_configuracion()
        
    def generar_recibo_window(self):
        window = Toplevel(self.root)
        window.title("Recibo de Venta")
        window.geometry("400x600")
        window.config(bg='white')
        
        # Área de texto para el recibo
        text_area = Text(window, font=('Consolas', 10), bg='white', relief='flat')
        text_area.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Contenido del recibo
        contenido = self._construir_contenido()
        text_area.insert('1.0', contenido)
        text_area.config(state='disabled') # Solo lectura
        
        # Botón Imprimir (Simulado)
        btn_print = tk.Button(window, text="Imprimir / Guardar", command=lambda: self._guardar_txt(contenido),
                            bg='#2c3e50', fg='white', font=('Segoe UI', 10, 'bold'))
        btn_print.pack(pady=10)
        
    def _construir_contenido(self):
        c = self.config
        fecha = self.venta_data['fecha']
        id_venta = self.venta_data['id']
        cajero = self.venta_data['cajero']
        
        lineas = []
        lineas.append(f"{c['nombre_empresa'].center(40)}")
        lineas.append(f"{c['slogan'].center(40)}")
        lineas.append(f"NIT/RUT: {c['nit_rut']}".center(40))
        lineas.append(f"{c['direccion']}".center(40))
        lineas.append(f"Tel: {c['telefono']}".center(40))
        lineas.append("-" * 40)
        lineas.append(f"Factura de Venta Nro: {id_venta}")
        lineas.append(f"Fecha: {fecha}")
        lineas.append(f"Cajero: {cajero}")
        lineas.append(f"Cliente: {self.cliente_nombre}")
        lineas.append("-" * 40)
        lineas.append(f"{'Cant.':<5} {'Producto':<20} {'Total':>10}")
        lineas.append("-" * 40)
        
        for d in self.detalles_venta:
            nombre = d['producto'][:20] # Truncar nombre
            cant = str(d['cantidad'])
            subtotal = f"{d['subtotal']:,.2f}"
            lineas.append(f"{cant:<5} {nombre:<20} {subtotal:>10}")
            
        lineas.append("-" * 40)
        lineas.append(f"TOTAL A PAGAR: ${self.venta_data['total']:,.2f}".rjust(40))
        lineas.append("-" * 40)
        lineas.append(f"{c['mensaje_final']}".center(40))
        lineas.append("\n\n")
        
        return "\n".join(lineas)

    def _guardar_txt(self, contenido):
        try:
            filename = f"Recibo_{self.venta_data['id']}.txt"
            with open(filename, "w", encoding='utf-8') as f:
                f.write(contenido)
            tk.messagebox.showinfo("Guardado", f"Recibo guardado como {filename}")
        except Exception as e:
            tk.messagebox.showerror("Error", f"No se pudo guardar: {e}")
