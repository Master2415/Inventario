import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import *
from datetime import datetime
from Model.ClienteDao import *

class Frame_Cliente(tk.Frame):

    def __init__(self, root, width=1280, height=720):
        super().__init__(root, width=width, height=height)
        self.root = root
        self.config(bg='#BBBBBB')  # Establecer el color de fondo del frame principal
        self.pack(fill='both', expand=True)
        self.idCliente = None # Usado para acceder a los metodos
        self.lebels_Entrys()
        self.tablaClientes()
        self.desHabilitar()
        

    def lebels_Entrys(self):
        #LABELS
        self.lblcedula = tk.Label(self, text='cedula')
        self.lblcedula.config(font=('ARIAl',15,'bold'), bg='#BBBBBB')
        self.lblcedula.grid(column=0, row=0, padx=10, pady=5)

        self.lblNombre = tk.Label(self, text='Nombre')
        self.lblNombre.config(font=('ARIAl',15,'bold'), bg='#BBBBBB')
        self.lblNombre.grid(column=0, row=1, padx=10, pady=5)

        self.lblApellido = tk.Label(self, text='Apellido')
        self.lblApellido.config(font=('ARIAl',15,'bold'), bg='#BBBBBB')
        self.lblApellido.grid(column=0, row=2, padx=10, pady=5)

        self.lblDireccion = tk.Label(self, text='Direccion')
        self.lblDireccion.config(font=('ARIAl',15,'bold'), bg='#BBBBBB')
        self.lblDireccion.grid(column=0, row=3, padx=10, pady=5)

        self.lblCorreo = tk.Label(self, text='Correo')
        self.lblCorreo.config(font=('ARIAl',15,'bold'), bg='#BBBBBB')
        self.lblCorreo.grid(column=0, row=4, padx=10, pady=5)

        self.lblTelefono = tk.Label(self, text='Telefono')
        self.lblTelefono.config(font=('ARIAl',15,'bold'), bg='#BBBBBB')
        self.lblTelefono.grid(column=0, row=5, padx=10, pady=5)

        self.lblCiudad = tk.Label(self, text='Ciudad')
        self.lblCiudad.config(font=('ARIAl',15,'bold'), bg='#BBBBBB')
        self.lblCiudad.grid(column=0, row=6, padx=10, pady=5)

        self.lblTipo = tk.Label(self, text='Tipo de Cliente')
        self.lblTipo.config(font=('ARIAl',15,'bold'), bg='#BBBBBB')
        self.lblTipo.grid(column=0, row=7, padx=10, pady=5)

        # Entrys
        self.svCedula = tk.StringVar()
        self.entruCedula = tk.Entry(self, textvariable=self.svCedula)
        self.entruCedula.config(width=40, font=('ARIAL',15))
        self.entruCedula.grid(column=1, row=0, padx=10, pady=5, columnspan=2)

        self.svNombre = tk.StringVar()
        self.entryNombre = tk.Entry(self, textvariable=self.svNombre)
        self.entryNombre.config(width=40, font=('ARIAL',15))
        self.entryNombre.grid(column=1, row=1, padx=10, pady=5, columnspan=2)

        self.svApellido = tk.StringVar()
        self.entryApellido = tk.Entry(self, textvariable=self.svApellido)
        self.entryApellido.config(width=40, font=('ARIAL',15))
        self.entryApellido.grid(column=1, row=2, padx=10, pady=5, columnspan=2)

        self.svDireccioon = tk.StringVar()
        self.entryDireccion = tk.Entry(self, textvariable=self.svDireccioon)
        self.entryDireccion.config(width=40, font=('ARIAL',15))
        self.entryDireccion.grid(column=1, row=3, padx=10, pady=5, columnspan=2)

        self.svcorreo = tk.StringVar()
        self.entryCorreo = tk.Entry(self, textvariable=self.svcorreo)
        self.entryCorreo.config(width=40, font=('ARIAL',15))
        self.entryCorreo.grid(column=1, row=4, padx=10, pady=5, columnspan=2)

        self.svTelefono = tk.StringVar()
        self.entryTelefono = tk.Entry(self, textvariable=self.svTelefono)
        self.entryTelefono.config(width=40, font=('ARIAL',15))
        self.entryTelefono.grid(column=1, row=5, padx=10, pady=5, columnspan=2)

        self.svCiudad = tk.StringVar()
        self.entryCiudad = tk.Entry(self, textvariable=self.svCiudad)
        self.entryCiudad.config(width=40, font=('ARIAL',15))
        self.entryCiudad.grid(column=1, row=6, padx=10, pady=5, columnspan=2)

        self.svTipo = tk.StringVar()
        self.entryTipo = tk.Entry(self, textvariable=self.svTipo)
        self.entryTipo.config(width=40, font=('ARIAL',15))
        self.entryTipo.grid(column=1, row=7, padx=10, pady=5, columnspan=2)

        self.svBuscar = tk.StringVar()
        self.entryBuscar = tk.Entry(self, textvariable=self.svBuscar)
        self.entryBuscar.config(width=40, font=('ARIAL',15))
        self.entryBuscar.grid(column=1, row=8, padx=10, pady=5, columnspan=2)

        #Botones
        self.btnNuevo = tk.Button(self, text='Agregar Cliente', command=self.habilitar)
        self.btnNuevo.config(width=20, font=('ARIAL',12,'bold'), fg='#DAD5D6', bg='#158645')
        self.btnNuevo.grid(column=3, row=0, padx=10, pady=5)

        self.btnGuardar = tk.Button(self, text='Guardar Nuevo', command=self.ingresarCliente)
        self.btnGuardar.config(width=20, font=('ARIAL',12,'bold'), fg='#DAD5D6', bg='#158645')
        self.btnGuardar.grid(column=3, row=1, padx=10, pady=5)

        self.btnEditar = tk.Button(self, text='Editar Cliente', command=self.editarCliente)
        self.btnEditar.config(width=20, font=('ARIAL',12,'bold'), fg='#DAD5D6', bg='#158645')
        self.btnEditar.grid(column=3, row=2, padx=10, pady=5)

        self.btnCancelar = tk.Button(self, text='Cancelar Nuevo', command=self.desHabilitar)
        self.btnCancelar.config(width=20, font=('ARIAL',12,'bold'), fg='#DAD5D6', bg='#CF0000')
        self.btnCancelar.grid(column=3, row=5, padx=10, pady=5)

        self.btnEliminar = tk.Button(self, text='Eliminar Cliente', command=self.eliminarPersona)
        self.btnEliminar.config(width=20, font=('ARIAL',12,'bold'), fg='#DAD5D6', bg='#CF0000')
        self.btnEliminar.grid(column=3, row=12, padx=10, pady=5)

        self.btnBuscar = tk.Button(self, text='Buscar', command=self.buscarCliente)
        self.btnBuscar.config(width=20, font=('ARIAL',12,'bold'), fg='#DAD5D6', bg='#001CCF')
        self.btnBuscar.grid(column=3, row=8, padx=10, pady=5)

    def eliminarPersona(self):
        try:
            self.idCliente = self.tabla.item(self.tabla.selection())['text']
            eliminarPersona(self.idCliente)
            
            self.tablaClientes()
            self.idCliente = None
        except:
            title = 'Eliminar Cliente'
            mensaje = 'No se pudo eliminar Cliente'
            messagebox.showinfo(title, mensaje)

    def editarCliente(self):
        try:
            # Obtengo los datos
            self.idCliente                 = self.tabla.item(self.tabla.selection())['text'] #Trae el ID
            self.cedula                    = self.tabla.item(self.tabla.selection())['values'][0]
            self.nombre                    = self.tabla.item(self.tabla.selection())['values'][1]
            self.apellido                  = self.tabla.item(self.tabla.selection())['values'][2]
            self.direccion                 = self.tabla.item(self.tabla.selection())['values'][3]
            self.correo                    = self.tabla.item(self.tabla.selection())['values'][4]
            self.telefono                  = self.tabla.item(self.tabla.selection())['values'][5]
            self.ciudad                    = self.tabla.item(self.tabla.selection())['values'][6]
            self.tipo                      = self.tabla.item(self.tabla.selection())['values'][7]
            
            self.habilitar()

            # Se agregan los datos obtenidos en el entry
            self.entruCedula.insert(0, self.cedula)
            self.entryNombre.insert(0, self.nombre)
            self.entryApellido.insert(0, self.apellido)
            self.entryDireccion.insert(0, self.direccion)
            self.entryCorreo.insert(0, self.correo)
            self.entryTelefono.insert(0, self.telefono)
            self.entryCiudad.insert(0, self.ciudad)
            self.entryTipo.insert(0, self.tipo)
        except:
            title = 'Editar Producto'
            mensaje = 'Error al editar Producto'
            messagebox.showerror(title, mensaje)
      

    def ingresarCliente(self):
        cliente = Cliente(self.svCedula.get(), self.svNombre.get(), self.svApellido.get(), self.svDireccioon.get(), 
                          self.svcorreo.get(), self.svTelefono.get(), self.svCiudad.get(), self.svTipo.get())

        if self.idCliente == None:
            guardarCliente(cliente)
        else:
            editarCliente(cliente, self.idCliente)

        self.desHabilitar() # Luego de guardar se desactivan los entrys, obligando al usuario a dar click en nuevo
        self.tablaClientes() # Se refresca la tabla de los clientes

    def habilitar(self):
        self.svCedula.set('')
        self.svNombre.set('')
        self.svApellido.set('')
        self.svDireccioon.set('')
        self.svcorreo.set('')
        self.svTelefono.set('')
        self.svCiudad.set('')
        self.svTipo.set('')

        self.entruCedula.config(state='normal')
        self.entryNombre.config(state='normal')
        self.entryApellido.config(state='normal')
        self.entryDireccion.config(state='normal')
        self.entryCorreo.config(state='normal')
        self.entryTelefono.config(state='normal')
        self.entryCiudad.config(state='normal')
        self.entryTipo.config(state='normal')

        self.btnGuardar.config(state='normal')
        self.btnCancelar.config(state='normal')

    def desHabilitar(self):
        self.idCliente = None
        self.svCedula.set('')
        self.svNombre.set('')
        self.svApellido.set('')
        self.svDireccioon.set('')
        self.svcorreo.set('')
        self.svTelefono.set('')
        self.svCiudad.set('')
        self.svTipo.set('')

        self.entruCedula.config(state='disabled')
        self.entryNombre.config(state='disabled')
        self.entryApellido.config(state='disabled')
        self.entryDireccion.config(state='disabled')
        self.entryCorreo.config(state='disabled')
        self.entryTelefono.config(state='disabled')
        self.entryCiudad.config(state='disabled')
        self.entryTipo.config(state='disabled')

        self.btnGuardar.config(state='disabled')
        self.btnCancelar.config(state='disabled')  

    def buscarCliente(self):
        # Obtener el texto del Entry
        texto_busqueda = self.svBuscar.get()

        # Verificar si se proporcionó algún texto de búsqueda
        if texto_busqueda:
            # Crear la condición WHERE
            where = "WHERE cedula LIKE '%" + texto_busqueda + "%' OR nombre LIKE '%" + texto_busqueda + "%' OR Ciudad LIKE '%" + texto_busqueda + "%' OR tipo_cliente LIKE '%" + texto_busqueda + "%'"

        else:
            where = ""  # Si no se proporcionó ninguna entrada, no se aplica ninguna condición WHERE

        # Llamar a la función para obtener los productos con las condiciones dadas
        self.tablaClientes(where)

    def tablaClientes(self,  where=""):

        if len(where) > 0:
            self.listaClientes = listarCondicion(where)
        else:
            self.listaClientes = listarClientes()

        # Frame para la tabla y la barra de desplazamiento
        frame_tabla = tk.Frame(self)
        frame_tabla.grid(column=0, row=10, columnspan=15, sticky='nsew')

        # Crear la tabla con barra de desplazamiento
        self.tabla = ttk.Treeview(frame_tabla, columns=('ID', 'Cedula', 'Nombre', 'Apellido', 'Direccion', 'Correo', 'Telefono', 'Ciudad'))
        scrollbar = ttk.Scrollbar(frame_tabla, orient='vertical', command=self.tabla.yview)
        self.tabla.configure(yscroll=scrollbar.set)
        self.tabla.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.tabla.heading('#0', text='ID')
        self.tabla.heading('#1', text='Cedula')
        self.tabla.heading('#2', text='Nombre')
        self.tabla.heading('#3', text='Apellido')
        self.tabla.heading('#4', text='Direccion')
        self.tabla.heading('#5', text='Correo')
        self.tabla.heading('#6', text='Telefono')
        self.tabla.heading('#7', text='ciudad')
        self.tabla.heading('#8', text='Tipo')

        self.tabla.column("#0", anchor='w', width=70)
        self.tabla.column("#1", anchor='w', width=100)
        self.tabla.column("#2", anchor='w', width=130)
        self.tabla.column("#3", anchor='w', width=150)
        self.tabla.column("#4", anchor='w', width=150)
        self.tabla.column("#5", anchor='w', width=200)
        self.tabla.column("#6", anchor='w', width=130)
        self.tabla.column("#7", anchor='w', width=100)
        self.tabla.column("#8", anchor='w', width=140)

        for p in self.listaClientes:
            self.tabla.insert('', 'end', text=p[0], values=(p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8]), tags=('evenrow',))
