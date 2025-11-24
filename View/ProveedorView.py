import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import *
from Model.ProductoDAO import *
from Model.ProveedorDAO import *

class ProveedorView(tk.Toplevel):
    def __init__(self, parent, idProducto):
        super().__init__(parent)
        self.parent = parent
        self.idProducto = idProducto
        self.title('Proveedor del producto')
        self.resizable(0, 0)
        self.config(bg='#f0f0f0')
        self.create_widgets()
        self.populate_providers()
        self.formulario_frame = None  # Inicializa la variable aquí
        self.idProveedor = None

    def create_widgets(self):
        self.tablaProveedores = ttk.Treeview(self, columns=('ID', 'Empresa', 'Tipo', 'Telefono', 'Dirección', 'Correo'))
        self.tablaProveedores.grid(row=0, column=0, columnspan=7, sticky='nsew')

        self.scrollProveedor = ttk.Scrollbar(self, orient='vertical', command=self.tablaProveedores.yview)
        self.scrollProveedor.grid(row=0, column=8, sticky='ns')

        self.tablaProveedores.configure(yscrollcommand=self.scrollProveedor.set)
        self.tablaProveedores.tag_configure('evenrow', background='#D7D7D7')

        self.tablaProveedores.heading('#0', text='ID')
        self.tablaProveedores.heading('#1', text='Empresa')
        self.tablaProveedores.heading('#2', text='Tipo')
        self.tablaProveedores.heading('#3', text='Telefono')
        self.tablaProveedores.heading('#4', text='Dirección')
        self.tablaProveedores.heading('#5', text='Correo')

        self.tablaProveedores.column('#0', anchor=tk.W, width=50)
        self.tablaProveedores.column('#1', anchor=tk.W, width=250)
        self.tablaProveedores.column('#2', anchor=tk.W, width=150)
        self.tablaProveedores.column('#3', anchor=tk.W, width=170)
        self.tablaProveedores.column('#4', anchor=tk.W, width=250)
        self.tablaProveedores.column('#5', anchor=tk.W, width=200)

        self.btnGuardarProveedor = tk.Button(self, text='Agregar Proveedor', command=self.mostrar_formulario_agregar)
        self.btnGuardarProveedor.config(width=20, font=('ARIAL', 12, 'bold'), fg='#DAD5D6', bg='#002771', cursor='hand2', activebackground='#7198E0')
        self.btnGuardarProveedor.grid(row=2, column=0, padx=10, pady=5)

        self.btnEliminarProveedor = tk.Button(self, text='Eliminar', command=self.eliminar)
        self.btnEliminarProveedor.config(width=20, font=('ARIAL', 12, 'bold'), fg='#DAD5D6', bg='#890011', cursor='hand2', activebackground='#DB939C')
        self.btnEliminarProveedor.grid(row=2, column=1, padx=10, pady=5)

        self.btnSalirWindowP = tk.Button(self, text='Salir', command=self.salir_top)
        self.btnSalirWindowP.config(width=20, font=('ARIAL', 12, 'bold'), fg='#DAD5D6', bg='#000000', cursor='hand2', activebackground='#6F6F6F')
        self.btnSalirWindowP.grid(row=2, column=3, padx=10, pady=5)

    def populate_providers(self):
        try:
            self.listaProveedores = listarProveedoresID(self.idProducto)
            for i, p in enumerate(self.listaProveedores):
                self.tablaProveedores.insert('', 'end', text=p[0], values=(p[1], p[2], p[3], p[4], p[5]), tags=('evenrow',) if i % 2 == 0 else ())
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo mostrar el proveedor: {e}")

    def salir_top(self):
        self.destroy()

    def mostrar_formulario_agregar(self):
        if self.formulario_frame:
            self.formulario_frame.destroy()

        self.formulario_frame = tk.Frame(self, bg='#BBBBBB')
        self.formulario_frame.grid(row=3, column=0, columnspan=9, sticky='nsew')

        self.lblnombreEmpresa = tk.Label(self.formulario_frame, text='Empresa')
        self.lblnombreEmpresa.config(font=('ARIAl', 15, 'bold'), bg='#BBBBBB')
        self.lblnombreEmpresa.grid(column=0, row=0, padx=10, pady=5)

        self.lblTipo = tk.Label(self.formulario_frame, text='Tipo')
        self.lblTipo.config(font=('ARIAl', 15, 'bold'), bg='#BBBBBB')
        self.lblTipo.grid(column=0, row=1, padx=10, pady=5)

        self.lblTelefono = tk.Label(self.formulario_frame, text='Telefono')
        self.lblTelefono.config(font=('ARIAl', 15, 'bold'), bg='#BBBBBB')
        self.lblTelefono.grid(column=0, row=2, padx=10, pady=5)

        self.lblDireccion = tk.Label(self.formulario_frame, text='Direccion')
        self.lblDireccion.config(font=('ARIAl', 15, 'bold'), bg='#BBBBBB')
        self.lblDireccion.grid(column=0, row=3, padx=10, pady=5)

        self.lblCorreo = tk.Label(self.formulario_frame, text='Correo')
        self.lblCorreo.config(font=('ARIAl', 15, 'bold'), bg='#BBBBBB')
        self.lblCorreo.grid(column=0, row=4, padx=10, pady=5)

        # Entrys
        self.svNombre = tk.StringVar()
        self.entryNombre = tk.Entry(self.formulario_frame, textvariable=self.svNombre)
        self.entryNombre.config(width=40, font=('ARIAL', 15))
        self.entryNombre.grid(column=1, row=0, padx=10, pady=5, columnspan=2)

        self.svTipo = tk.StringVar()
        self.entryTipo = tk.Entry(self.formulario_frame, textvariable=self.svTipo)
        self.entryTipo.config(width=40, font=('ARIAL', 15))
        self.entryTipo.grid(column=1, row=1, padx=10, pady=5, columnspan=2)

        self.svTelefono = tk.StringVar()
        self.entryTelefono = tk.Entry(self.formulario_frame, textvariable=self.svTelefono)
        self.entryTelefono.config(width=40, font=('ARIAL', 15))
        self.entryTelefono.grid(column=1, row=2, padx=10, pady=5, columnspan=2)

        self.svDireccion = tk.StringVar()
        self.entryDireccion = tk.Entry(self.formulario_frame, textvariable=self.svDireccion)
        self.entryDireccion.config(width=40, font=('ARIAL', 15))
        self.entryDireccion.grid(column=1, row=3, padx=10, pady=5, columnspan=2)

        self.svCorreo = tk.StringVar()
        self.entryCorreo = tk.Entry(self.formulario_frame, textvariable=self.svCorreo)
        self.entryCorreo.config(width=40, font=('ARIAL', 15))
        self.entryCorreo.grid(column=1, row=4, padx=10, pady=5, columnspan=2)

        self.btnGuardar = tk.Button(self.formulario_frame, text='Guardar Nuevo', command=self.ingresar_proveedor)
        self.btnGuardar.config(width=20, font=('ARIAL', 12, 'bold'), fg='#DAD5D6', bg='#158645')
        self.btnGuardar.grid(column=3, row=1, padx=10, pady=5)

        self.btnCancelar = tk.Button(self.formulario_frame, text='Cancelar', command=self.ocultar_formulario)
        self.btnCancelar.config(width=20, font=('ARIAL', 12, 'bold'), fg='#DAD5D6', bg='#CF0000')
        self.btnCancelar.grid(column=3, row=2, padx=10, pady=5)

    def eliminar(self):
        try:
            self.idProveedor = self.tablaProveedores.item(self.tablaProveedores.selection())['text']
            eliminarProveedor(self.idProveedor)
            self.destroy()

        except:
            title = 'Eliminar Producto'
            mensaje = 'No se pudo eliminar Producto'
            messagebox.showinfo(title, mensaje)

    def ocultar_formulario(self):
        if self.formulario_frame:
            self.formulario_frame.destroy()

    def ingresar_proveedor(self): 
        proveedor = Proveedor(self.svNombre.get(), self.svTipo.get(), self.svTelefono.get(), self.svDireccion.get(), self.svCorreo.get())

        try:
            if self.idProveedor == None:
                agregarProveedor(proveedor, self.idProducto)
            else:
                editarProveedor(proveedor, self.idProveedor)
        except:
            title = 'Agregar Proveedor'
            mensaje = 'Error al agregar Proveedor'
            messagebox.showerror(title, mensaje)

        self.create_widgets()
    
    