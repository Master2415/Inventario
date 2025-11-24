import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import *
from Model.UsuarioDAO import *
from Model.VentaDAO import listarVentasUsuario

class UsuarioView(tk.Frame):
    def __init__(self, root, width=1280, height=720):
        super().__init__(root, width=width, height=height)
        self.root = root
        self.config(bg='#f0f2f5')  # Establecer el color de fondo del frame principal
        self.pack(fill='both', expand=True)
        self.idUsuario = None
        self.empleados_map = {} # Mapa para guardar idEmpleado -> string del combo
        self.empleados_map_reverse = {} # Mapa para guardar string del combo -> idEmpleado
        
        self.frame_tablaUsers()
        self.deshabilitar()
     
    def frame_tablaUsers(self, where=""):
        if hasattr(self, 'tablaUser'):
            self.tablaUser.delete(*self.tablaUser.get_children())

        if len(where) > 0:
            self.listausers = listarUserWhere(where)
        else:
            self.listausers = listarUser()
        
        if not hasattr(self, 'tabla_frame'):
            self.tabla_frame = tk.Frame(self)
            self.tabla_frame.pack(fill='x', expand=False)

            self.tablaUser = ttk.Treeview(self.tabla_frame, height=10, columns=('ID', 'Usuario', 'Contrasena', 'nombre', 'apellido', 'cedula', 'Rol', 'idEmpleado'))
            self.scrolluser = ttk.Scrollbar(self.tabla_frame, orient='vertical', command=self.tablaUser.yview)
            self.tablaUser.configure(yscroll=self.scrolluser.set)
            self.tablaUser.pack(side='left', fill='both', expand=True)
            self.tablaUser.pack(side='right', fill='y')

            self.tablaUser.heading('#0', text='ID')
            self.tablaUser.heading('#1', text='Usuario')
            self.tablaUser.heading('#2', text='Contrasena')
            self.tablaUser.heading('#3', text='Nombre')
            self.tablaUser.heading('#4', text='Apellido')
            self.tablaUser.heading('#5', text='Cedula')
            self.tablaUser.heading('#6', text='Rol')
            # idEmpleado oculto o visible si se quiere debuggear, pero no es necesario mostrarlo al usuario final
            
            self.tablaUser.column("#0", anchor='w', width=50)
            self.tablaUser.column("#1", anchor='w', width=200)
            self.tablaUser.column("#2", anchor='w', width=200)
            self.tablaUser.column("#3", anchor='w', width=150)
            self.tablaUser.column("#4", anchor='w', width=150)
            self.tablaUser.column("#5", anchor='w', width=150)
            self.tablaUser.column("#6", anchor='w', width=150)
            self.tablaUser.column("#7", width=0, stretch=NO) # Ocultar idEmpleado
            
        
        for p in self.listausers:
            # p = (idusuario, correo, contrasena, nombre, apellido, cedula, nombreRol, idEmpleado)
            self.tablaUser.insert('', 'end', text=p[0], values=(p[1], p[2], p[3], p[4], p[5], p[6], p[7]), tags=('evenrow',))

        if not hasattr(self, 'botones_frame'):
            self.botones_frame = tk.Frame(self, bg='#f0f2f5')
            self.botones_frame.pack(pady=10)

            self.btnNuevo = tk.Button(self.botones_frame, text='Agregar', command=self.habilitar)
            self.btnNuevo.config(width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#27ae60', relief='flat', cursor='hand2')
            self.btnNuevo.grid(column=0, row=0, padx=10, pady=5)

            self.btnEditar = tk.Button(self.botones_frame, text='Editar', command=self.editarUser)
            self.btnEditar.config(width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#3498db', relief='flat', cursor='hand2')
            self.btnEditar.grid(column=1, row=0, padx=10, pady=5)

            self.btnEliminar = tk.Button(self.botones_frame, text='Eliminar', command=self.eliminarUser)
            self.btnEliminar.config(width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#c0392b', relief='flat', cursor='hand2')
            self.btnEliminar.grid(column=2, row=0, padx=10, pady=5)

            self.btnVerVentas = tk.Button(self.botones_frame, text='Ver Ventas', command=self.verVentasUsuario)
            self.btnVerVentas.config(width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#f39c12', relief='flat', cursor='hand2')
            self.btnVerVentas.grid(column=3, row=0, padx=10, pady=5)

        if not hasattr(self, 'formulario_frame'):
            self.formulario_frame = tk.Frame(self, bg='#f0f2f5')
            self.formulario_frame.pack(pady=10)

            self.lblUsuario = tk.Label(self.formulario_frame, text='Nombre de Usuario')
            self.lblUsuario.config(font=('Segoe UI', 12, 'bold'), bg='#f0f2f5')
            self.lblUsuario.grid(column=0, row=0, padx=10, pady=5)

            self.lblContrasena = tk.Label(self.formulario_frame, text='Contraseña')
            self.lblContrasena.config(font=('Segoe UI', 12, 'bold'), bg='#f0f2f5')
            self.lblContrasena.grid(column=0, row=1, padx=10, pady=5)

            self.lblEmpleado = tk.Label(self.formulario_frame, text='Empleado')
            self.lblEmpleado.config(font=('Segoe UI', 12, 'bold'), bg='#f0f2f5')
            self.lblEmpleado.grid(column=0, row=2, padx=10, pady=5)

            # Entrys
            self.svUsuario = tk.StringVar()
            self.entryUsuario = tk.Entry(self.formulario_frame, textvariable=self.svUsuario)
            self.entryUsuario.config(width=40, font=('Segoe UI', 12))
            self.entryUsuario.grid(column=1, row=0, padx=10, pady=5, columnspan=2)

            self.svContrasena = tk.StringVar()
            self.entryContrasena = tk.Entry(self.formulario_frame, textvariable=self.svContrasena)
            self.entryContrasena.config(width=40, font=('Segoe UI', 12))
            self.entryContrasena.grid(column=1, row=1, padx=10, pady=5, columnspan=2)

            # Combobox Empleado
            self.svEmpleado = tk.StringVar()
            self.comboEmpleado = ttk.Combobox(self.formulario_frame, textvariable=self.svEmpleado, state="readonly")
            self.comboEmpleado.config(width=38, font=('Segoe UI', 12))
            self.comboEmpleado.grid(column=1, row=2, padx=10, pady=5, columnspan=2)

            self.btnGuardar = tk.Button(self.formulario_frame, text='Guardar', command=self.agregarUser)
            self.btnGuardar.config(width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#27ae60', cursor='hand2', relief='flat')
            self.btnGuardar.grid(column=1, row=3, padx=10, pady=10)

            self.btnCancelar = tk.Button(self.formulario_frame, text='Cancelar', command=self.deshabilitar)
            self.btnCancelar.config(width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#c0392b', cursor='hand2', relief='flat')
            self.btnCancelar.grid(column=2, row=3, padx=10, pady=10)
    
    def cargar_empleados(self):
        empleados = obtener_empleados_para_combo()
        self.empleados_map = {}
        self.empleados_map_reverse = {}
        valores_combo = []
        for emp in empleados:
            # emp = (idEmpleado, nombre, apellido, cedula)
            texto = f"{emp[1]} {emp[2]} - {emp[3]}"
            self.empleados_map[texto] = emp[0]
            self.empleados_map_reverse[emp[0]] = texto
            valores_combo.append(texto)
        self.comboEmpleado['values'] = valores_combo

    def eliminarUser(self):
        try:
            self.idUsuario = self.tablaUser.item(self.tablaUser.selection())['text']
            eliminarUsuario(self.idUsuario)
            
            self.frame_tablaUsers()
            self.idUsuario = None
        except:
            title = 'Eliminar Usuario'
            mensaje = 'No se pudo eliminar Usuario'
            messagebox.showinfo(title, mensaje)
    
    def editarUser(self):
        try:
            selection = self.tablaUser.selection()
            if not selection:
                messagebox.showwarning("Advertencia", "Seleccione un usuario")
                return

            # Obtengo los datos
            self.idUsuario = self.tablaUser.item(selection)['text']  # Trae el ID
            self.nombreUser = self.tablaUser.item(selection)['values'][0]
            self.contrasena = self.tablaUser.item(selection)['values'][1]
            # El idEmpleado está en la columna 7 (índice 6 en values porque values es 0-indexed)
            self.idEmpleadoActual = self.tablaUser.item(selection)['values'][6] 

            self.habilitar()

            # Se agregan los datos obtenidos en el entry
            self.entryUsuario.insert(0, self.nombreUser)
            self.entryContrasena.insert(0, self.contrasena)
            
            # Seleccionar el empleado en el combo
            if self.idEmpleadoActual in self.empleados_map_reverse:
                self.comboEmpleado.set(self.empleados_map_reverse[self.idEmpleadoActual])

        except Exception as e:
            title = 'Editar Usuario'
            mensaje = f'Error al editar Usuario: {e}'
            messagebox.showerror(title, mensaje)

    def agregarUser(self):
        nombre_empleado = self.svEmpleado.get()
        if not nombre_empleado:
            messagebox.showwarning("Advertencia", "Seleccione un empleado")
            return
            
        idEmpleado = self.empleados_map.get(nombre_empleado)
        if not idEmpleado:
             messagebox.showerror("Error", "Empleado inválido")
             return

        usuario = Usuario(self.entryUsuario.get(), self.entryContrasena.get())

        if self.idUsuario is None:
            guardarUsuario(usuario, idEmpleado)
        else:
            editarUsuario(self.idUsuario, usuario, idEmpleado)

        self.deshabilitar()
        self.frame_tablaUsers()

        
    def habilitar(self):
        self.svUsuario.set('')
        self.svContrasena.set('')
        self.svEmpleado.set('')
        
        self.cargar_empleados() # Cargar empleados al habilitar el formulario

        self.entryUsuario.config(state='normal')
        self.entryContrasena.config(state='normal')
        self.comboEmpleado.config(state='normal')
    
        self.btnGuardar.config(state='normal')
        self.btnCancelar.config(state='normal')
        
    def deshabilitar(self):
        self.svUsuario.set('')
        self.svContrasena.set('')
        self.svEmpleado.set('')
        self.idUsuario = None # Limpiar ID al cancelar/guardar
        
        self.entryUsuario.config(state='disabled')
        self.entryContrasena.config(state='disabled')
        self.comboEmpleado.config(state='disabled')
    
        self.btnGuardar.config(state='disabled')
        self.btnCancelar.config(state='disabled')

    def verVentasUsuario(self):
        try:
            selection = self.tablaUser.selection()
            if not selection:
                messagebox.showwarning("Advertencia", "Seleccione un usuario")
                return
            
            self.idUsuario = self.tablaUser.item(selection[0])['text']
            
            ventas = listarVentasUsuario(self.idUsuario)
            
            top = tk.Toplevel(self)
            top.title(f"Ventas del Usuario ID: {self.idUsuario}")
            top.geometry("800x400")
            
            tablaVentas = ttk.Treeview(top, columns=('idVenta', 'total', 'fecha', 'Cedula Cliente'), show='headings')
            tablaVentas.heading('idVenta', text='ID Venta')
            tablaVentas.heading('total', text='Total')
            tablaVentas.heading('fecha', text='Fecha')
            tablaVentas.heading('Cedula Cliente', text='Cedula Cliente')
            
            tablaVentas.column('idVenta', width=100)
            tablaVentas.column('total', width=100)
            tablaVentas.column('fecha', width=200)
            tablaVentas.column('Cedula Cliente', width=150)
            
            tablaVentas.pack(fill='both', expand=True)
            
            for v in ventas:
                # v = (idVenta, total, fecha, correo_usuario, cedula_cliente)
                tablaVentas.insert('', 'end', values=(v[0], f"{v[1]:,.2f}", v[2], v[4]))
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al ver ventas: {e}")
