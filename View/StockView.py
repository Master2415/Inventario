import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from Model.ProveedorDAO import *
from View.ProveedorView import ProveedorView
from Model.StockDAO import *
from Model.ProductoDAO import listarRegistroProductos


class Frame_Stock(tk.Frame):
    def __init__(self, root, width=1745, height=750):
        super().__init__(root, width=width, height=height)
        self.root = root
        self.config(bg='#f0f0f0')
        self.pack(fill='both', expand=True)
        self.idStock = None
        self.frameBuscar()
        self.create_table()
        self.deshabilitar()
        self.btnBuscar.config(command=self.buscarProducto)

    def frameBuscar(self):
        self.buscar_frame = tk.Frame(self, bg='#f0f0f0')
        self.buscar_frame.pack(pady=10)

        self.svBuscar = tk.StringVar()
        self.entryBuscar = tk.Entry(self.buscar_frame, textvariable=self.svBuscar)
        self.entryBuscar.config(width=40, font=('Arial', 15), bg='#ffffff')
        self.entryBuscar.grid(column=0, row=0, padx=10, pady=5)

        self.btnBuscar = tk.Button(self.buscar_frame, text='Buscar')
        self.btnBuscar.config(width=20, font=('Arial', 12, 'bold'), fg='#ffffff', bg='#007ACC')
        self.btnBuscar.grid(column=1, row=0, padx=10, pady=5)

    def create_table(self, where=""):
        if hasattr(self, 'tablaProductosStock'):
            self.tablaProductosStock.delete(*self.tablaProductosStock.get_children())

        if len(where) > 0:
            self.listaProductosStock = listarStockWhere(where)
        else:
            self.listaProductosStock = listarStock()

        if not hasattr(self, 'tabla_frame'):
            self.tabla_frame = tk.Frame(self)
            self.tabla_frame.pack(fill='x', expand=False)

            self.tablaProductosStock = ttk.Treeview(self.tabla_frame, height=10, columns=('ID', 'Codigo', 'Nombre', 'Tipo', 'Utilidad', 'IVA', 'Precio Total', 'Kg Disponibles', 'Precio Neto'))
            self.scrollProducto = ttk.Scrollbar(self.tabla_frame, orient='vertical', command=self.tablaProductosStock.yview)
            self.tablaProductosStock.configure(yscroll=self.scrollProducto.set)
            self.tablaProductosStock.pack(side='left', fill='both', expand=True)
            self.scrollProducto.pack(side='right', fill='y')

            self.tablaProductosStock.heading('#0', text='ID')
            self.tablaProductosStock.heading('#1', text='Codigo')
            self.tablaProductosStock.heading('#2', text='Nombre')
            self.tablaProductosStock.heading('#3', text='Tipo')
            self.tablaProductosStock.heading('#4', text='Utilidad')
            self.tablaProductosStock.heading('#5', text='IVA')
            self.tablaProductosStock.heading('#6', text='Precio Total')
            self.tablaProductosStock.heading('#7', text='Kg Disponibles')
            self.tablaProductosStock.heading('#8', text='Precio Neto')

            self.tablaProductosStock.column('#0', anchor=tk.W, width=50)
            self.tablaProductosStock.column('#1', anchor=tk.W, width=150)
            self.tablaProductosStock.column('#2', anchor=tk.W, width=150)
            self.tablaProductosStock.column('#3', anchor=tk.W, width=150)
            self.tablaProductosStock.column('#4', anchor=tk.W, width=150)
            self.tablaProductosStock.column('#5', anchor=tk.W, width=150)
            self.tablaProductosStock.column('#6', anchor=tk.W, width=150)
            self.tablaProductosStock.column('#7', anchor=tk.W, width=150)
            self.tablaProductosStock.column('#8', anchor=tk.W, width=150)

            for p in self.listaProductosStock:
                self.tablaProductosStock.insert('', 'end', text=p[0], values=(p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8]), tags=('evenrow',))

        # Botones debajo de la tabla
        self.btn_frame = tk.Frame(self, bg='#f0f0f0')
        self.btn_frame.pack(pady=(10, 20), anchor='n')

        self.btnRegistroEntrda = tk.Button(self.btn_frame, text='Registrsos del producto', command=self.ver_RegistrosEntrada)
        self.btnRegistroEntrda.config(width=20, font=('Arial', 12, 'bold'), fg='#ffffff', bg='#E8B200')
        self.btnRegistroEntrda.grid(column=0, row=0, padx=10, pady=5)

        self.btnProveedores = tk.Button(self.btn_frame, text='Ver Proveedores', command=self.ver_proveedor)
        self.btnProveedores.config(width=20, font=('Arial', 12, 'bold'), fg='#ffffff', bg='#E8B200')
        self.btnProveedores.grid(column=1, row=0, padx=10, pady=5)


        if not hasattr(self, 'botones_frame'):
            self.botones_frame = tk.Frame(self, bg='#f0f0f0')
            self.botones_frame.pack(pady=10)

            self.btnNuevo = tk.Button(self.botones_frame, text='Agregar Producto', command=self.habilitar)
            self.btnNuevo.config(width=20, font=('Arial', 12, 'bold'), fg='#ffffff', bg='#5CB85C')
            self.btnNuevo.grid(column=0, row=0, padx=10, pady=5)

            self.btnEditar = tk.Button(self.botones_frame, text='Editar Producto', command=self.editarProducto)
            self.btnEditar.config(width=20, font=('Arial', 12, 'bold'), fg='#ffffff', bg='#007ACC')
            self.btnEditar.grid(column=1, row=0, padx=10, pady=5)

            self.btnEliminar = tk.Button(self.botones_frame, text='Eliminar Producto', command=self.eliminarProducto)
            self.btnEliminar.config(width=20, font=('Arial', 12, 'bold'), fg='#ffffff', bg='#D9534F')
            self.btnEliminar.grid(column=2, row=0, padx=10, pady=5)

        if not hasattr(self, 'formulario_frame'):
            self.formulario_frame = tk.Frame(self, bg='#BBBBBB')
            self.formulario_frame.pack(fill='x', padx=20, pady=10)

            self.lblCodigo = tk.Label(self.formulario_frame, text='Codigo')
            self.lblCodigo.config(font=('Arial', 15, 'bold'), bg='#BBBBBB')
            self.lblCodigo.grid(column=0, row=1, padx=10, pady=5)

            self.lblNombre = tk.Label(self.formulario_frame, text='Nombre')
            self.lblNombre.config(font=('Arial', 15, 'bold'), bg='#BBBBBB')
            self.lblNombre.grid(column=0, row=2, padx=10, pady=5)

            self.lblTipo = tk.Label(self.formulario_frame, text='Tipo Producto')
            self.lblTipo.config(font=('Arial', 15, 'bold'), bg='#BBBBBB')
            self.lblTipo.grid(column=0, row=3, padx=10, pady=5)

            self.lblPrecioNeto = tk.Label(self.formulario_frame, text='Precio Neto')
            self.lblPrecioNeto.config(font=('Arial', 15, 'bold'), bg='#BBBBBB')
            self.lblPrecioNeto.grid(column=0, row=4, padx=10, pady=5)

            self.lblUtilidad = tk.Label(self.formulario_frame, text='Utilidad')
            self.lblUtilidad.config(font=('Arial', 15, 'bold'), bg='#BBBBBB')
            self.lblUtilidad.grid(column=0, row=5, padx=10, pady=5)

            self.lblIVA = tk.Label(self.formulario_frame, text='IVA')
            self.lblIVA.config(font=('Arial', 15, 'bold'), bg='#BBBBBB')
            self.lblIVA.grid(column=0, row=6, padx=10, pady=5)

            self.svcodigo = tk.StringVar()
            self.entrycodigo = tk.Entry(self.formulario_frame, textvariable=self.svcodigo)
            self.entrycodigo.config(width=40, font=('Arial', 15))
            self.entrycodigo.grid(column=1, row=1, padx=10, pady=5, columnspan=2)

            self.svNombre = tk.StringVar()
            self.entryNombre = tk.Entry(self.formulario_frame, textvariable=self.svNombre)
            self.entryNombre.config(width=40, font=('Arial', 15))
            self.entryNombre.grid(column=1, row=2, padx=10, pady=5, columnspan=2)

            self.svTipo = tk.StringVar()
            self.entryTipo = tk.Entry(self.formulario_frame, textvariable=self.svTipo)
            self.entryTipo.config(width=40, font=('Arial', 15))
            self.entryTipo.grid(column=1, row=3, padx=10, pady=5, columnspan=2)

            self.svPrecioNeto = tk.StringVar()
            self.entryPrecio = tk.Entry(self.formulario_frame, textvariable=self.svPrecioNeto)
            self.entryPrecio.config(width=40, font=('Arial', 15))
            self.entryPrecio.grid(column=1, row=4, padx=10, pady=5, columnspan=2)

            self.svUtilidad = tk.StringVar()
            self.entryUtilidad = tk.Entry(self.formulario_frame, textvariable=self.svUtilidad)
            self.entryUtilidad.config(width=40, font=('Arial', 15))
            self.entryUtilidad.grid(column=1, row=5, padx=10, pady=5, columnspan=2)

            self.svIVA = tk.StringVar()
            self.entryIVA = tk.Entry(self.formulario_frame, textvariable=self.svIVA)
            self.entryIVA.config(width=40, font=('Arial', 15))
            self.entryIVA.grid(column=1, row=6, padx=10, pady=5, columnspan=2)

            self.btnGuardar = tk.Button(self.formulario_frame, text='Guardar', command=self.agregarProducto)
            self.btnGuardar.config(width=20, font=('Arial', 12, 'bold'), fg='#ffffff', bg='#5CB85C', cursor='hand2')
            self.btnGuardar.grid(column=1, row=7, padx=10, pady=10)

            self.btnCancelar = tk.Button(self.formulario_frame, text='Cancelar', command=self.deshabilitar)
            self.btnCancelar.config(width=20, font=('Arial', 12, 'bold'), fg='#ffffff', bg='#D9534F', cursor='hand2')
            self.btnCancelar.grid(column=2, row=7, padx=10, pady=10)
    

    def agregarProducto(self):
        precio_neto = float(self.svPrecioNeto.get())
        utilidad = float(self.svUtilidad.get())
        iva = float(self.svIVA.get())

        self.precioTotal = precio_neto * (1 + utilidad + iva)

        productoStock = ProductoStock(self.svcodigo.get(), self.svNombre.get(), self.svTipo.get(), 
                                      self.svUtilidad.get(), self.svIVA.get(), self.precioTotal, self.svPrecioNeto.get())
          
        if self.idStock is None:
            guardarProStock(productoStock)
        else:
            editarProStock(self.idStock, productoStock)
     
        self.create_table()


    def habilitar(self):
        self.svcodigo.set('')
        self.svNombre.set('')
        self.svTipo.set('')
        self.svPrecioNeto.set('')
        self.svUtilidad.set('')
        self.svIVA.set('')

        self.entrycodigo.config(state='normal')
        self.entryNombre.config(state='normal')
        self.entryTipo.config(state='normal')
        self.entryPrecio.config(state='normal')
        self.entryUtilidad.config(state='normal')
        self.entryIVA.config(state='normal')

        self.btnGuardar.config(state='normal')
        self.btnCancelar.config(state='normal')
        
    def deshabilitar(self):
        self.svcodigo.set('')
        self.svNombre.set('')
        self.svTipo.set('')
        self.svPrecioNeto.set('')
        self.svUtilidad.set('')
        self.svIVA.set('')

        self.entrycodigo.config(state='disabled')
        self.entryNombre.config(state='disabled')
        self.entryTipo.config(state='disabled')
        self.entryPrecio.config(state='disabled')
        self.entryUtilidad.config(state='disabled')
        self.entryIVA.config(state='disabled')

        self.btnGuardar.config(state='disabled')
        self.btnCancelar.config(state='disabled')
    
    def buscarProducto(self):
        valor = self.svBuscar.get()
        if valor:
            where = f"codigo LIKE '%{valor}%' OR nombre LIKE '%{valor}%' OR tipo LIKE '%{valor}%'"
        else:
            where = ""  # Si no se proporcionó ninguna entrada, no se aplica ninguna condición WHERE    
        self.create_table(where)


    def editarProducto(self):
        try:
            try:       
                self.idStock =      self.tablaProductosStock.item(self.tablaProductosStock.selection())['text']
                self.codigo =       self.tablaProductosStock.item(self.tablaProductosStock.selection())['values'][0]
                self.nombre =       self.tablaProductosStock.item(self.tablaProductosStock.selection())['values'][1]
                self.tipo =         self.tablaProductosStock.item(self.tablaProductosStock.selection())['values'][2]
                self.utilidad =     (self.tablaProductosStock.item(self.tablaProductosStock.selection())['values'][3])  # Convertir a float
                self.iva =          (self.tablaProductosStock.item(self.tablaProductosStock.selection())['values'][4])  # Convertir a float
                self.precioNeto =   self.tablaProductosStock.item(self.tablaProductosStock.selection())['values'][7]
                
                self.habilitar()

                # Actualizar las variables de los widgets de entrada
                self.svcodigo.set(self.codigo)
                self.svNombre.set(self.nombre)
                self.svTipo.set(self.tipo)
                self.svUtilidad.set(self.utilidad)
                self.svIVA.set(self.iva)
                self.svPrecioNeto.set(self.precioNeto)           
            except IndexError as e:
                messagebox.showerror('Error', 'Los valores seleccionados no son correctos')
        except ValueError as e:
            messagebox.showerror('Error', f'Error de conversión: {str(e)}')
        except Exception as e:
            messagebox.showerror('Error', f'Error inesperado: {str(e)}')     


    def eliminarProducto(self):
        try:
            self.idStock = self.tablaProductosStock.item(self.tablaProductosStock.selection())['text']
            eliminarProStock(self.idStock)
            self.create_table()
        except IndexError as e:
            messagebox.showerror('Error', 'Seleccione un producto de la tabla')


    def ver_proveedor(self):
        self.idStock = self.get_selected_product_id()
        if self.idStock:
            ProveedorView(self, self.idStock)
        else:
            messagebox.showerror("Error", "Seleccione un producto")

    def ver_RegistrosEntrada(self):
        self.idStock = self.get_selected_product_id()
        if self.idStock:
            Registro(self, self.idStock)
        else:
            messagebox.showerror("Error", "Seleccione un producto")

    def get_selected_product_id(self):
        selected_item = self.tablaProductosStock.selection()
        if selected_item:
            return self.tablaProductosStock.item(selected_item)['text']
        else:
            return None
        
class Registro(tk.Toplevel):
    def __init__(self, parent, idProducto):
        super().__init__(parent)
        self.parent = parent
        self.idProducto = idProducto
        self.title('Ingresos del producto')
        self.resizable(0, 0)
        
        self.config(bg='#f0f0f0')
        self.tablaProductos()
        self.idProducto = None

    def tablaProductos(self):
        # Eliminar los elementos existentes de la tabla si ya existe
        if hasattr(self, 'tablaProducto'):
            self.tablaProducto.delete(*self.tablaProducto.get_children())
        else:
            # Si la tabla no existe, crearla junto con su frame y scrollbar
            self.frame_tablaProducto = tk.Frame(self)
            self.frame_tablaProducto.pack(fill='x', expand=False)

            # Crear la tablaProducto con barra de desplazamiento
            self.tablaProducto = ttk.Treeview(self.frame_tablaProducto, height=10, columns=('idProducto', 'Codigo', 'Producto', 'Tipo', 'Cant. ingresada', 'Precio', 'Fecha de Ingreso', 'Proveedor'))
            self.scrollbar = ttk.Scrollbar(self.frame_tablaProducto, orient='vertical', command=self.tablaProducto.yview)
            self.tablaProducto.configure(yscroll=self.scrollbar.set)
            self.tablaProducto.pack(side='left', fill='both', expand=True)
            self.scrollbar.pack(side='right', fill='y')

            self.tablaProducto.heading('#0', text='ID')
            self.tablaProducto.heading('#1', text='Codigo')
            self.tablaProducto.heading('#2', text='Producto')
            self.tablaProducto.heading('#3', text='Tipo')
            self.tablaProducto.heading('#4', text='Cant. ingresada')
            self.tablaProducto.heading('#5', text='Precio')
            self.tablaProducto.heading('#6', text='Fecha de Ingreso')
            self.tablaProducto.heading('#7', text='Proveedor')

            self.tablaProducto.column("#0", anchor='w', width=100)
            self.tablaProducto.column("#1", anchor='w', width=130)
            self.tablaProducto.column("#2", anchor='w', width=180)
            self.tablaProducto.column("#3", anchor='w', width=150)
            self.tablaProducto.column("#4", anchor='w', width=150)
            self.tablaProducto.column("#5", anchor='w', width=120)
            self.tablaProducto.column("#6", anchor='w', width=180)
            self.tablaProducto.column("#7", anchor='w', width=170)

        
        self.listaProductos = listarRegistroProductos(self.idProducto)

        for p in self.listaProductos:
            precio_formateado = "{:,.2f}".format(p[5])  # Asumiendo que p[5] es el precio
            self.tablaProducto.insert('', 'end', text=p[0], values=(p[1], p[2], p[3], p[4], precio_formateado, p[6], p[7]), tags=('evenrow',))


