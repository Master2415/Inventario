import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import *
from Model.EmpleadoDAO import *

class EmpleadoView(tk.Frame):
    def __init__(self, root, width=1280, height=720):
        super().__init__(root, width=width, height=height)
        self.root = root
        self.config(bg='#f0f2f5')  # Establecer el color de fondo del frame principal
        self.pack(fill='both', expand=True)
        self.idEmpleado = None
        self.frameBuscar()
        self.frame_tablaEmpleado() 
        self.listaCargos() # Debe ir despues de la definicion de la tabla, ya que ahi esta el combobox
        self.deshabilitar()
        self.btnBuscar.config(command=self.buscarEmpleado) 


    def frameBuscar(self):
        self.buscar_frame = tk.Frame(self, bg='#f0f2f5')
        self.buscar_frame.pack(pady=10, fill='x', padx=20,)

        self.svBuscar = tk.StringVar()
        self.entryBuscar = tk.Entry(self.buscar_frame, textvariable=self.svBuscar)
        self.entryBuscar.config(width=40, font=('Segoe UI', 15), bg='#ffffff')
        self.entryBuscar.grid(column=0, row=0, padx=10, pady=5)

        self.btnBuscar = tk.Button(self.buscar_frame, text='Buscar')
        self.btnBuscar.config(width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#3498db', relief='flat', cursor='hand2')
        self.btnBuscar.grid(column=1, row=0, padx=10, pady=5)

    def frame_tablaEmpleado(self, where=""):
        if hasattr(self, 'tablaEmpleados'):
            self.tablaEmpleados.delete(*self.tablaEmpleados.get_children())

        if len(where) > 0:
            self.listaMEmpleado = listarEmpleadoWhere(where)
        else:
            self.listaMEmpleado = listarEmpleado()

        if not hasattr(self, 'tabla_frame'):
            self.tabla_frame = tk.Frame(self)
            self.tabla_frame.pack(fill='x', expand=False)

            self.tablaEmpleados = ttk.Treeview(self.tabla_frame, height=10, columns=('ID', 'Cedula', 'Nombre', 'Apellido', 'Direccion', 'Correo', 'Telefono', 'Ciudad', 'Horas trabajadas', 'Fecha Contratación', 'Cargo'))
            self.scrollEmpleado = ttk.Scrollbar(self.tabla_frame, orient='vertical', command=self.tablaEmpleados.yview)
            self.tablaEmpleados.configure(yscroll=self.scrollEmpleado.set)
            self.tablaEmpleados.pack(side='left', fill='both', expand=True)
            self.scrollEmpleado.pack(side='right', fill='y')

            self.tablaEmpleados.heading('#0', text='ID')
            self.tablaEmpleados.heading('#1', text='Cedula')
            self.tablaEmpleados.heading('#2', text='Nombre')
            self.tablaEmpleados.heading('#3', text='Apellido')
            self.tablaEmpleados.heading('#4', text='Direccion')
            self.tablaEmpleados.heading('#5', text='Correo')
            self.tablaEmpleados.heading('#6', text='Telefono')
            self.tablaEmpleados.heading('#7', text='ciudad')
            self.tablaEmpleados.heading('#8', text='Horas trabajadas')
            self.tablaEmpleados.heading('#9', text='Fecha Contratación')
            self.tablaEmpleados.heading('#10', text='Cargo')

            self.tablaEmpleados.column("#0", anchor='w', width=70)
            self.tablaEmpleados.column("#1", anchor='w', width=100)
            self.tablaEmpleados.column("#2", anchor='w', width=130)
            self.tablaEmpleados.column("#3", anchor='w', width=150)
            self.tablaEmpleados.column("#4", anchor='w', width=140)
            self.tablaEmpleados.column("#5", anchor='w', width=180)
            self.tablaEmpleados.column("#6", anchor='w', width=130)
            self.tablaEmpleados.column("#7", anchor='w', width=100)
            self.tablaEmpleados.column("#8", anchor='w', width=80)
            self.tablaEmpleados.column('#9', anchor='w', width=150)
            self.tablaEmpleados.column('#10', anchor='w', width=100)
  
        for p in self.listaMEmpleado:
            self.tablaEmpleados.insert('', 'end', text=p[0], values=(p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10]), tags=('evenrow',))

        if not hasattr(self, 'botones_frame'):
            self.botones_frame = tk.Frame(self, bg='#f0f2f5')
            self.botones_frame.pack(pady=10)

            self.btnNuevo = tk.Button(self.botones_frame, text='Agregar', command=self.habilitar)
            self.btnNuevo.config(width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#27ae60', relief='flat', cursor='hand2')
            self.btnNuevo.grid(column=0, row=0, padx=10, pady=5)

            self.btnEditar = tk.Button(self.botones_frame, text='Editar', command=self.editarEmpleado)
            self.btnEditar.config(width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#3498db', relief='flat', cursor='hand2')
            self.btnEditar.grid(column=1, row=0, padx=10, pady=5)

            self.btnEliminar = tk.Button(self.botones_frame, text='Eliminar', command=self.eliminarEmpleado)
            self.btnEliminar.config(width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#c0392b', relief='flat', cursor='hand2')
            self.btnEliminar.grid(column=2, row=0, padx=10, pady=5)

        if not hasattr(self, 'formulario_frame'):
            self.formulario_frame = tk.Frame(self, bg='#f0f2f5')
            self.formulario_frame.pack(fill='x', padx=20, pady=10)

            # Labels
            labels = ['Cedula', 'Nombre', 'Apellido', 'Direccion', 'Correo', 'Telefono', 'Ciudad', 'Horas Trabajadas', 'Fecha de contratación', 'Codigo del cargo']
            for i, text in enumerate(labels):
                lbl = tk.Label(self.formulario_frame, text=text, font=('Segoe UI', 15, 'bold'), bg='#f0f2f5')
                lbl.grid(column=0, row=i, padx=10, pady=5, sticky='e')

            # Entries
            self.svCedula = tk.StringVar()
            self.entruCedula = tk.Entry(self.formulario_frame, textvariable=self.svCedula, width=40, font=('Segoe UI', 15))
            self.entruCedula.grid(column=1, row=0, padx=10, pady=5, sticky='w')

            self.svNombre = tk.StringVar()
            self.entryNombre = tk.Entry(self.formulario_frame, textvariable=self.svNombre, width=40, font=('Segoe UI', 15))
            self.entryNombre.grid(column=1, row=1, padx=10, pady=5, sticky='w')

            self.svApellido = tk.StringVar()
            self.entryApellido = tk.Entry(self.formulario_frame, textvariable=self.svApellido, width=40, font=('Segoe UI', 15))
            self.entryApellido.grid(column=1, row=2, padx=10, pady=5, sticky='w')

            self.svDireccioon = tk.StringVar()
            self.entryDireccion = tk.Entry(self.formulario_frame, textvariable=self.svDireccioon, width=40, font=('Segoe UI', 15))
            self.entryDireccion.grid(column=1, row=3, padx=10, pady=5, sticky='w')

            self.svcorreo = tk.StringVar()
            self.entryCorreo = tk.Entry(self.formulario_frame, textvariable=self.svcorreo, width=40, font=('Segoe UI', 15))
            self.entryCorreo.grid(column=1, row=4, padx=10, pady=5, sticky='w')

            self.svTelefono = tk.StringVar()
            self.entryTelefono = tk.Entry(self.formulario_frame, textvariable=self.svTelefono, width=40, font=('Segoe UI', 15))
            self.entryTelefono.grid(column=1, row=5, padx=10, pady=5, sticky='w')

            self.svCiudad = tk.StringVar()
            self.entryCiudad = tk.Entry(self.formulario_frame, textvariable=self.svCiudad, width=40, font=('Segoe UI', 15))
            self.entryCiudad.grid(column=1, row=6, padx=10, pady=5, sticky='w')

            self.svHoras = tk.StringVar()
            self.entryHoras = tk.Entry(self.formulario_frame, textvariable=self.svHoras, width=40, font=('Segoe UI', 15))
            self.entryHoras.grid(column=1, row=7, padx=10, pady=5, sticky='w')

            self.svFecha = tk.StringVar()
            self.entryFecha = tk.Entry(self.formulario_frame, textvariable=self.svFecha, width=40, font=('Segoe UI', 15))
            self.entryFecha.grid(column=1, row=8, padx=10, pady=5, sticky='w')

            self.boxCargo = ttk.Combobox(self.formulario_frame, state='readonly', width=40, font=('Segoe UI', 12))
            self.boxCargo.grid(column=1, row=9, padx=10, pady=5, sticky='w')

            self.btnGuardar = tk.Button(self.formulario_frame, text='Guardar', command=self.ingresarEmpleado)
            self.btnGuardar.config(width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#27ae60', relief='flat', cursor='hand2')
            self.btnGuardar.grid(column=1, row=10, padx=10, pady=10)

            self.btnCancelar = tk.Button(self.formulario_frame, text='Cancelar', command=self.deshabilitar)
            self.btnCancelar.config(width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#c0392b', relief='flat', cursor='hand2')
            self.btnCancelar.grid(column=2, row=10, padx=10, pady=10)

    def listaCargos(self):
        try:
            lista_cargos = obtener_Cargos_combobox()
            self.boxCargo['values'] = lista_cargos
            if lista_cargos:
                self.boxCargo.current(0)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar los Cargos: {e}")

    def eliminarEmpleado(self):
        try:
            self.idEmpleado = self.tablaEmpleados.item(self.tablaEmpleados.selection())['text']
            eliminarEmpleado(self.idEmpleado)
            
            self.frame_tablaEmpleado()
            self.idEmpleado = None
        except:
            title = 'Eliminar Empleado'
            mensaje = 'No se pudo eliminar Empleado'
            messagebox.showinfo(title, mensaje)

    def editarEmpleado(self):
        try:
            # Obtengo los datos
            self.idEmpleado                 = self.tablaEmpleados.item(self.tablaEmpleados.selection())['text'] #Trae el ID
            self.cedula                    = self.tablaEmpleados.item(self.tablaEmpleados.selection())['values'][0]
            self.nombre                    = self.tablaEmpleados.item(self.tablaEmpleados.selection())['values'][1]
            self.apellido                  = self.tablaEmpleados.item(self.tablaEmpleados.selection())['values'][2]
            self.direccion                 = self.tablaEmpleados.item(self.tablaEmpleados.selection())['values'][3]
            self.correo                    = self.tablaEmpleados.item(self.tablaEmpleados.selection())['values'][4]
            self.telefono                  = self.tablaEmpleados.item(self.tablaEmpleados.selection())['values'][5]
            self.ciudad                    = self.tablaEmpleados.item(self.tablaEmpleados.selection())['values'][6]
            self.horasTarabajadas          = self.tablaEmpleados.item(self.tablaEmpleados.selection())['values'][7]
            self.fechaContrato             = self.tablaEmpleados.item(self.tablaEmpleados.selection())['values'][8]
            self.cargo                     = self.tablaEmpleados.item(self.tablaEmpleados.selection())['values'][9]
            
            self.habilitar()

            # Se agregan los datos obtenidos en el entry
            self.entruCedula.insert(0, self.cedula)
            self.entryNombre.insert(0, self.nombre)
            self.entryApellido.insert(0, self.apellido)
            self.entryDireccion.insert(0, self.direccion)
            self.entryCorreo.insert(0, self.correo)
            self.entryTelefono.insert(0, self.telefono)
            self.entryCiudad.insert(0, self.ciudad)
            self.entryHoras.insert(0, self.horasTarabajadas)
            self.entryFecha.insert(0, self.fechaContrato)
            self.boxCargo.insert(0, self.cargo)

        except:
            title = 'Editar Empleado'
            mensaje = 'Error al editar Empleado'
            messagebox.showerror(title, mensaje)

    def ingresarEmpleado(self):
        rol_seleccionas = self.boxCargo.get()

        empleado = Empleado(self.svCedula.get(), self.svNombre.get(), self.svApellido.get(), self.svDireccioon.get(), 
                          self.svcorreo.get(), self.svTelefono.get(), self.svCiudad.get(), self.svHoras.get(), 
                          self.svFecha.get())

        if self.idEmpleado == None:
            guardarEmpleado(empleado, rol_seleccionas)
        else:
            editarEmpleado(empleado, self.idEmpleado, rol_seleccionas)

        self.deshabilitar() # Luego de guardar se desactivan los entrys, obligando al usuario a dar click en nuevo
        self.frame_tablaEmpleado() # Se refresca la tabla de los clientes

    def buscarEmpleado(self):
        texto_busqueda = self.svBuscar.get()
        if texto_busqueda:
            where = "cedula LIKE '%" + texto_busqueda + "%' OR nombre LIKE '%" + texto_busqueda + "%' OR ciudad LIKE '%" + texto_busqueda + "%'"
        else:
            where = ""  # Si no se proporcionó ninguna entrada, no se aplica ninguna condición WHERE
        self.frame_tablaEmpleado(where)

    def habilitar(self):
        self.svCedula.set('')
        self.svNombre.set('')
        self.svApellido.set('')
        self.svDireccioon.set('')
        self.svcorreo.set('')
        self.svTelefono.set('')
        self.svCiudad.set('')
        self.svHoras.set('')
        self.svFecha.set('')
        self.boxCargo.set('')

        self.entruCedula.config(state='normal')
        self.entryNombre.config(state='normal')
        self.entryApellido.config(state='normal')
        self.entryDireccion.config(state='normal')
        self.entryCorreo.config(state='normal')
        self.entryTelefono.config(state='normal')
        self.entryCiudad.config(state='normal')
        self.entryHoras.config(state='normal')
        self.entryFecha.config(state='normal')
        self.boxCargo.config(state='normal')

        self.btnGuardar.config(state='normal')
        self.btnCancelar.config(state='normal')
        
    def deshabilitar(self):
        self.svCedula.set('')
        self.svNombre.set('')
        self.svApellido.set('')
        self.svDireccioon.set('')
        self.svcorreo.set('')
        self.svTelefono.set('')
        self.svCiudad.set('')
        self.svHoras.set('')
        self.svFecha.set('')
        self.boxCargo.set('')

        self.entruCedula.config(state='disabled')
        self.entryNombre.config(state='disabled')
        self.entryApellido.config(state='disabled')
        self.entryDireccion.config(state='disabled')
        self.entryCorreo.config(state='disabled')
        self.entryTelefono.config(state='disabled')
        self.entryCiudad.config(state='disabled')
        self.entryHoras.config(state='disabled')
        self.entryFecha.config(state='disabled')
        self.boxCargo.config(state='disabled')

        self.btnGuardar.config(state='disabled')
        self.btnCancelar.config(state='disabled')