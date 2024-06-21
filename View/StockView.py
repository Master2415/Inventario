import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from Model.StockDAO import listarStock
from Model.ProveedorDAO import *
from View.ProveedorView import ProveedorView


class Frame_Stock(tk.Frame):
    def __init__(self, root, width=1745, height=750):
        super().__init__(root, width=width, height=height)
        self.root = root
        self.config(bg='#f0f0f0')  # Color de fondo del frame principal
        self.pack(fill='both', expand=True)
        self.idStock = None
        self.formulario_frame = None 
        self.mostrar_formulario_agregar()
        self.populate_providers()

    def mostrar_formulario_agregar(self):
        if self.formulario_frame:
            self.formulario_frame.destroy()

        self.formulario_frame = tk.Frame(self, bg='#f0f0f0')
        self.formulario_frame.pack(pady=20, padx=20, anchor='n')

        entry_bg = '#ffffff'

        self.svBuscar = tk.StringVar()
        self.entryBuscar = tk.Entry(self.formulario_frame, textvariable=self.svBuscar)
        self.entryBuscar.config(width=40, font=('Arial', 15), bg=entry_bg)
        self.entryBuscar.grid(column=0, row=0, padx=10, pady=5, sticky='w')

        self.btnBuscar = tk.Button(self.formulario_frame, text='Buscar')
        self.btnBuscar.config(width=20, font=('Arial', 12, 'bold'), fg='#ffffff', bg='#007ACC')
        self.btnBuscar.grid(column=1, row=0, padx=10, pady=5)

        self.tabla_frame = tk.Frame(self)
        self.tabla_frame.pack(pady=(20, 0), padx=20, anchor='n')

        self.tablaProductosStock = ttk.Treeview(self.tabla_frame, columns=('ID', 'Codigo', 'Nombre', 'Tipo', 'Utilidad', 'IVA', 'Precio Total', 'Kg Disponibles'))
        self.tablaProductosStock.pack(side='left')

        self.scrollProveedor = ttk.Scrollbar(self.tabla_frame, orient='vertical', command=self.tablaProductosStock.yview)
        self.scrollProveedor.pack(side='right', fill='y')

        self.tablaProductosStock.configure(yscrollcommand=self.scrollProveedor.set)
        self.tablaProductosStock.tag_configure('evenrow', background='#E8E8E8')

        self.tablaProductosStock.heading('#0', text='ID')
        self.tablaProductosStock.heading('#1', text='Codigo')
        self.tablaProductosStock.heading('#2', text='Nombre')
        self.tablaProductosStock.heading('#3', text='Tipo')
        self.tablaProductosStock.heading('#4', text='Utilidad')
        self.tablaProductosStock.heading('#5', text='IVA')
        self.tablaProductosStock.heading('#6', text='Precio a la venta')
        self.tablaProductosStock.heading('#7', text='Kg Disponibles')

        self.tablaProductosStock.column('#0', anchor=tk.W, width=50)
        self.tablaProductosStock.column('#1', anchor=tk.W, width=150)
        self.tablaProductosStock.column('#2', anchor=tk.W, width=150)
        self.tablaProductosStock.column('#3', anchor=tk.W, width=150)
        self.tablaProductosStock.column('#4', anchor=tk.W, width=150)
        self.tablaProductosStock.column('#5', anchor=tk.W, width=150)
        self.tablaProductosStock.column('#6', anchor=tk.W, width=150)
        self.tablaProductosStock.column('#7', anchor=tk.W, width=150)

        # Botones debajo de la tabla
        self.btn_frame = tk.Frame(self, bg='#f0f0f0')
        self.btn_frame.pack(pady=(10, 20), anchor='n')

        self.btnRegistroEntrda = tk.Button(self.btn_frame, text='Ver registros de entrada')
        self.btnRegistroEntrda.config(width=20, font=('Arial', 12, 'bold'), fg='#ffffff', bg='#5CB85C')
        self.btnRegistroEntrda.pack(side='left', padx=10, pady=5)

        self.btnRegistroEntrda = tk.Button(self.btn_frame, text='Ver Proveedores', command=self.ver_proveedor)
        self.btnRegistroEntrda.config(width=20, font=('Arial', 12, 'bold'), fg='#ffffff', bg='#5CB85C')
        self.btnRegistroEntrda.pack(side='left', padx=10, pady=5)

        self.btnEditar = tk.Button(self.btn_frame, text='Modificar')
        self.btnEditar.config(width=20, font=('Arial', 12, 'bold'), fg='#ffffff', bg='#007ACC')
        self.btnEditar.pack(side='left', padx=10, pady=5)

        self.btnEliminar = tk.Button(self.btn_frame, text='Eliminar Proveedor')
        self.btnEliminar.config(width=20, font=('Arial', 12, 'bold'), fg='#ffffff', bg='#D9534F')
        self.btnEliminar.pack(side='left', padx=10, pady=5)

    

    def populate_providers(self):
        try:
            self.listaProductos = listarStock()
            for i, p in enumerate(self.listaProductos):
                # Formatear el precio a la venta con separadores de miles y dos decimales
                precio_venta = "{:,.2f}".format(p[6])
                # Insertar en la tabla, formateando como cadena
                tags = ('evenrow',) if i % 2 == 0 else ()
                self.tablaProductosStock.insert('', 'end', text=p[0], values=(p[1], p[2], p[3], p[4], p[5], precio_venta, p[7]), tags=tags)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo mostrar el proveedor: {e}")

    
    def ver_proveedor(self):
        self.idStock = self.get_selected_product_id()
        if self.idStock:
            ProveedorView(self, self.idStock)
        else:
            messagebox.showerror("Error", "Seleccione un producto")

    def get_selected_product_id(self):
        selected_item = self.tablaProductosStock.selection()
        if selected_item:
            return self.tablaProductosStock.item(selected_item)['text']
        else:
            return None


