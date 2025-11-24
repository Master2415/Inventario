import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from Model.ClienteDao import *
from Model.VentaDAO import listarVentasCliente
from View.DetalleVentaView import DetalleVentaView

class Frame_Cliente(tk.Frame):
    def __init__(self, root, width=1280, height=720):
        super().__init__(root, width=width, height=height)
        self.root = root
        self.config(bg='#f0f2f5')
        self.pack(fill='both', expand=True)
        self.idCliente = None
        
        self.frameBuscar()
        self.frame_tablaCliente()
        self.deshabilitar()

    def frameBuscar(self):
        self.buscar_frame = tk.Frame(self, bg='#f0f2f5')
        self.buscar_frame.pack(pady=10, fill='x', padx=20)

        self.svBuscar = tk.StringVar()
        self.entryBuscar = tk.Entry(self.buscar_frame, textvariable=self.svBuscar)
        self.entryBuscar.config(width=40, font=('Segoe UI', 15))
        self.entryBuscar.grid(column=0, row=0, padx=10, pady=5)

        self.btnBuscar = tk.Button(self.buscar_frame, text='Buscar', command=self.buscarCliente)
        self.btnBuscar.config(width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#3498db', relief='flat', cursor='hand2')
        self.btnBuscar.grid(column=1, row=0, padx=10, pady=5)

    def frame_tablaCliente(self, where=""):
        if hasattr(self, 'tablaClientes'):
            self.tablaClientes.delete(*self.tablaClientes.get_children())

        if len(where) > 0:
            self.listaClientes = listarCondicion(where)
        else:
            self.listaClientes = listarClientes()

        if not hasattr(self, 'tabla_frame'):
            self.tabla_frame = tk.Frame(self)
            self.tabla_frame.pack(fill='x', expand=False, padx=20)

            self.tablaClientes = ttk.Treeview(self.tabla_frame, height=10, columns=('ID', 'Cedula', 'Nombre', 'Apellido', 'Direccion', 'Correo', 'Telefono', 'Ciudad', 'Tipo Cliente'))
            self.scrollCliente = ttk.Scrollbar(self.tabla_frame, orient='vertical', command=self.tablaClientes.yview)
            self.tablaClientes.configure(yscroll=self.scrollCliente.set)
            self.tablaClientes.pack(side='left', fill='both', expand=True)
            self.scrollCliente.pack(side='right', fill='y')

            self.tablaClientes.heading('#0', text='ID')
            self.tablaClientes.heading('#1', text='Cedula')
            self.tablaClientes.heading('#2', text='Nombre')
            self.tablaClientes.heading('#3', text='Apellido')
            self.tablaClientes.heading('#4', text='Direccion')
            self.tablaClientes.heading('#5', text='Correo')
            self.tablaClientes.heading('#6', text='Telefono')
            self.tablaClientes.heading('#7', text='Ciudad')
            self.tablaClientes.heading('#8', text='Tipo Cliente')

            self.tablaClientes.column("#0", anchor='w', width=50)
            self.tablaClientes.column("#1", anchor='w', width=100)
            self.tablaClientes.column("#2", anchor='w', width=150)
            self.tablaClientes.column("#3", anchor='w', width=150)
            self.tablaClientes.column("#4", anchor='w', width=150)
            self.tablaClientes.column("#5", anchor='w', width=180)
            self.tablaClientes.column("#6", anchor='w', width=100)
            self.tablaClientes.column("#7", anchor='w', width=100)
            self.tablaClientes.column("#8", anchor='w', width=100)

        for p in self.listaClientes:
            self.tablaClientes.insert('', 'end', text=p[0], values=(p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8]), tags=('evenrow',))

        if not hasattr(self, 'botones_frame'):
            self.botones_frame = tk.Frame(self, bg='#f0f2f5')
            self.botones_frame.pack(pady=10)

            self.btnNuevo = tk.Button(self.botones_frame, text='Agregar', command=self.habilitar)
            self.btnNuevo.config(width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#27ae60', relief='flat', cursor='hand2')
            self.btnNuevo.grid(column=0, row=0, padx=10, pady=5)

            self.btnEditar = tk.Button(self.botones_frame, text='Editar', command=self.editarCliente)
            self.btnEditar.config(width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#3498db', relief='flat', cursor='hand2')
            self.btnEditar.grid(column=1, row=0, padx=10, pady=5)

            self.btnCompras = tk.Button(self.botones_frame, text='Compras Realizadas', command=self.verCompras)
            self.btnCompras.config(width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#f39c12', relief='flat', cursor='hand2')
            self.btnCompras.grid(column=2, row=0, padx=10, pady=5)

            self.btnEliminar = tk.Button(self.botones_frame, text='Eliminar', command=self.eliminarCliente)
            self.btnEliminar.config(width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#c0392b', relief='flat', cursor='hand2')
            self.btnEliminar.grid(column=3, row=0, padx=10, pady=5)

        if not hasattr(self, 'formulario_frame'):
            self.formulario_frame = tk.Frame(self, bg='#f0f2f5')
            self.formulario_frame.pack(fill='x', padx=20, pady=10)

            # Labels
            labels = ['Cedula', 'Nombre', 'Apellido', 'Direccion', 'Correo', 'Telefono', 'Ciudad', 'Tipo Cliente']
            for i, text in enumerate(labels):
                lbl = tk.Label(self.formulario_frame, text=text, font=('Segoe UI', 15, 'bold'), bg='#f0f2f5')
                lbl.grid(column=0, row=i, padx=10, pady=5, sticky='e')

            # Entries
            self.svCedula = tk.StringVar()
            self.entryCedula = tk.Entry(self.formulario_frame, textvariable=self.svCedula, width=40, font=('Segoe UI', 15))
            self.entryCedula.grid(column=1, row=0, padx=10, pady=5, sticky='w')

            self.svNombre = tk.StringVar()
            self.entryNombre = tk.Entry(self.formulario_frame, textvariable=self.svNombre, width=40, font=('Segoe UI', 15))
            self.entryNombre.grid(column=1, row=1, padx=10, pady=5, sticky='w')

            self.svApellido = tk.StringVar()
            self.entryApellido = tk.Entry(self.formulario_frame, textvariable=self.svApellido, width=40, font=('Segoe UI', 15))
            self.entryApellido.grid(column=1, row=2, padx=10, pady=5, sticky='w')

            self.svDireccion = tk.StringVar()
            self.entryDireccion = tk.Entry(self.formulario_frame, textvariable=self.svDireccion, width=40, font=('Segoe UI', 15))
            self.entryDireccion.grid(column=1, row=3, padx=10, pady=5, sticky='w')

            self.svCorreo = tk.StringVar()
            self.entryCorreo = tk.Entry(self.formulario_frame, textvariable=self.svCorreo, width=40, font=('Segoe UI', 15))
            self.entryCorreo.grid(column=1, row=4, padx=10, pady=5, sticky='w')

            self.svTelefono = tk.StringVar()
            self.entryTelefono = tk.Entry(self.formulario_frame, textvariable=self.svTelefono, width=40, font=('Segoe UI', 15))
            self.entryTelefono.grid(column=1, row=5, padx=10, pady=5, sticky='w')

            self.svCiudad = tk.StringVar()
            self.entryCiudad = tk.Entry(self.formulario_frame, textvariable=self.svCiudad, width=40, font=('Segoe UI', 15))
            self.entryCiudad.grid(column=1, row=6, padx=10, pady=5, sticky='w')

            self.svTipoCliente = tk.StringVar()
            self.entryTipoCliente = tk.Entry(self.formulario_frame, textvariable=self.svTipoCliente, width=40, font=('Segoe UI', 15))
            self.entryTipoCliente.grid(column=1, row=7, padx=10, pady=5, sticky='w')

            # Buttons for Form
            self.btnGuardar = tk.Button(self.formulario_frame, text='Guardar', command=self.ingresarCliente)
            self.btnGuardar.config(width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#27ae60', relief='flat', cursor='hand2')
            self.btnGuardar.grid(column=1, row=8, padx=10, pady=10)

            self.btnCancelar = tk.Button(self.formulario_frame, text='Cancelar', command=self.deshabilitar)
            self.btnCancelar.config(width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#c0392b', relief='flat', cursor='hand2')
            self.btnCancelar.grid(column=2, row=8, padx=10, pady=10)

    def habilitar(self):
        self.svCedula.set('')
        self.svNombre.set('')
        self.svApellido.set('')
        self.svDireccion.set('')
        self.svCorreo.set('')
        self.svTelefono.set('')
        self.svCiudad.set('')
        self.svTipoCliente.set('')

        self.entryCedula.config(state='normal')
        self.entryNombre.config(state='normal')
        self.entryApellido.config(state='normal')
        self.entryDireccion.config(state='normal')
        self.entryCorreo.config(state='normal')
        self.entryTelefono.config(state='normal')
        self.entryCiudad.config(state='normal')
        self.entryTipoCliente.config(state='normal')

        self.btnGuardar.config(state='normal')
        self.btnCancelar.config(state='normal')

    def deshabilitar(self):
        self.svCedula.set('')
        self.svNombre.set('')
        self.svApellido.set('')
        self.svDireccion.set('')
        self.svCorreo.set('')
        self.svTelefono.set('')
        self.svCiudad.set('')
        self.svTipoCliente.set('')

        self.entryCedula.config(state='disabled')
        self.entryNombre.config(state='disabled')
        self.entryApellido.config(state='disabled')
        self.entryDireccion.config(state='disabled')
        self.entryCorreo.config(state='disabled')
        self.entryTelefono.config(state='disabled')
        self.entryCiudad.config(state='disabled')
        self.entryTipoCliente.config(state='disabled')

        self.btnGuardar.config(state='disabled')
        self.btnCancelar.config(state='disabled')

    def buscarCliente(self):
        texto_busqueda = self.svBuscar.get()
        if texto_busqueda:
            where = "WHERE p.cedula LIKE '%" + texto_busqueda + "%' OR p.nombre LIKE '%" + texto_busqueda + "%'"
        else:
            where = ""
        self.frame_tablaCliente(where)

    def ingresarCliente(self):
        cliente = Cliente(self.svCedula.get(), self.svNombre.get(), self.svApellido.get(), self.svDireccion.get(),
                          self.svCorreo.get(), self.svTelefono.get(), self.svCiudad.get(), self.svTipoCliente.get())

        if self.idCliente is None:
            guardarCliente(cliente)
        else:
            editarCliente(cliente, self.idCliente)

        self.deshabilitar()
        self.frame_tablaCliente()
        self.idCliente = None

    def editarCliente(self):
        try:
            self.idCliente = self.tablaClientes.item(self.tablaClientes.selection())['text']
            self.cedula = self.tablaClientes.item(self.tablaClientes.selection())['values'][0]
            self.nombre = self.tablaClientes.item(self.tablaClientes.selection())['values'][1]
            self.apellido = self.tablaClientes.item(self.tablaClientes.selection())['values'][2]
            self.direccion = self.tablaClientes.item(self.tablaClientes.selection())['values'][3]
            self.correo = self.tablaClientes.item(self.tablaClientes.selection())['values'][4]
            self.telefono = self.tablaClientes.item(self.tablaClientes.selection())['values'][5]
            self.ciudad = self.tablaClientes.item(self.tablaClientes.selection())['values'][6]
            self.tipo_cliente = self.tablaClientes.item(self.tablaClientes.selection())['values'][7]

            self.habilitar()

            self.entryCedula.insert(0, self.cedula)
            self.entryNombre.insert(0, self.nombre)
            self.entryApellido.insert(0, self.apellido)
            self.entryDireccion.insert(0, self.direccion)
            self.entryCorreo.insert(0, self.correo)
            self.entryTelefono.insert(0, self.telefono)
            self.entryCiudad.insert(0, self.ciudad)
            self.entryTipoCliente.insert(0, self.tipo_cliente)

        except Exception as e:
            messagebox.showerror("Error", f"Error al editar cliente: {e}")

    def eliminarCliente(self):
        try:
            self.idCliente = self.tablaClientes.item(self.tablaClientes.selection())['text']
            eliminarPersona(self.idCliente)
            self.frame_tablaCliente()
            self.idCliente = None
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar cliente: {e}")

    def verCompras(self):
        try:
            self.idCliente = self.tablaClientes.item(self.tablaClientes.selection())['text']
            comprasRealizadas(self, self.idCliente)
        except Exception as e:
            messagebox.showerror("Error", "Seleccione un cliente para ver sus compras.")

class comprasRealizadas(tk.Toplevel):
    def __init__(self, parent, idCliente):
        super().__init__(parent)
        self.idCliente = idCliente
        self.title('Compras Realizadas')
        self.geometry('800x400')
        self.listaVentas = listarVentasCliente(self.idCliente)
        self.tablaVentas = ttk.Treeview(self, columns=('idVenta', 'total', 'fecha', 'Cajero', 'Cedula Cliente'), show='headings')
        self.tablaVentas.pack(fill='both', expand=True)

        self.tablaVentas.heading('idVenta', text='ID', anchor='w')
        self.tablaVentas.heading('total', text='Total', anchor='w')
        self.tablaVentas.heading('fecha', text='Fecha', anchor='w')
        self.tablaVentas.heading('Cajero', text='Cajero', anchor='w')
        self.tablaVentas.heading('Cedula Cliente', text='Cedula Cliente', anchor='w')

        self.tablaVentas.column('idVenta', anchor='w', width=50)
        self.tablaVentas.column('total', anchor='w', width=100)
        self.tablaVentas.column('fecha', anchor='w', width=170)
        self.tablaVentas.column('Cajero', anchor='w', width=120)
        self.tablaVentas.column('Cedula Cliente', anchor='w', width=120)

        for venta in self.listaVentas:
            id_venta = venta[0]
            total = f"{venta[1]:,.2f}"
            fecha = venta[2]
            Cajero = venta[3]
            Cedula = venta[4]

            self.tablaVentas.insert('', 'end', values=(id_venta, total, fecha, Cajero, Cedula))

        btn_detalle = tk.Button(self, text="Ver Detalle", command=self.verDetalleVenta,
                              font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#3498db', relief='flat', cursor='hand2')
        btn_detalle.pack(pady=10)

    def verDetalleVenta(self):
        selected_item = self.tablaVentas.selection()
        if selected_item:
            idVenta = self.tablaVentas.item(selected_item)['values'][0]
            DetalleVentaView(self, idVenta)
        else:
            messagebox.showerror("Error", "Seleccione una Venta")