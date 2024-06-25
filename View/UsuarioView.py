import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import *
from Model.UsuarioDAO import *

class UsuarioView(tk.Frame):
    def __init__(self, root, width=1280, height=720):
        super().__init__(root, width=width, height=height)
        self.root = root
        self.config(bg='#f0f0f0')  # Establecer el color de fondo del frame principal
        self.pack(fill='both', expand=True)
        self.idUsuario = None
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

            self.tablaUser = ttk.Treeview(self.tabla_frame, height=10, columns=('ID', 'Usuario', 'Contrasena', 'nombre', 'apellido', 'cedula', 'Rol'))
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

            self.tablaUser.column("#0", anchor='w', width=100)
            self.tablaUser.column("#1", anchor='w', width=260)
            self.tablaUser.column("#2", anchor='w', width=260)
            self.tablaUser.column("#3", anchor='w', width=200)
            self.tablaUser.column("#4", anchor='w', width=200)
            self.tablaUser.column("#5", anchor='w', width=200)
            self.tablaUser.column("#6", anchor='w', width=200)
            
        
        for p in self.listausers:
            self.tablaUser.insert('', 'end', text=p[0], values=(p[1], p[2], p[3], p[4], p[5], p[6]), tags=('evenrow',))

        if not hasattr(self, 'botones_frame'):
            self.botones_frame = tk.Frame(self, bg='#f0f0f0')
            self.botones_frame.pack(pady=10)

            self.btnNuevo = tk.Button(self.botones_frame, text='Agregar', command=self.habilitar)
            self.btnNuevo.config(width=20, font=('Arial', 12, 'bold'), fg='#ffffff', bg='#5CB85C')
            self.btnNuevo.grid(column=0, row=0, padx=10, pady=5)

            self.btnEditar = tk.Button(self.botones_frame, text='Editar', command=self.editarUser)
            self.btnEditar.config(width=20, font=('Arial', 12, 'bold'), fg='#ffffff', bg='#007ACC')
            self.btnEditar.grid(column=1, row=0, padx=10, pady=5)

            self.btnEliminar = tk.Button(self.botones_frame, text='Eliminar', command=self.eliminarUser)
            self.btnEliminar.config(width=20, font=('Arial', 12, 'bold'), fg='#ffffff', bg='#D9534F')
            self.btnEliminar.grid(column=2, row=0, padx=10, pady=5)

        if not hasattr(self, 'formulario_frame'):
            self.formulario_frame = tk.Frame(self, bg='#BBBBBB')
            self.formulario_frame.pack(pady=10)

            self.lblUsuario = tk.Label(self.formulario_frame, text='Nombre de Usuario')
            self.lblUsuario.config(font=('ARIAl',15,'bold'), bg='#BBBBBB')
            self.lblUsuario.grid(column=0, row=0, padx=10, pady=5)

            self.lblContrasena = tk.Label(self.formulario_frame, text='Contraseña')
            self.lblContrasena.config(font=('ARIAl',15,'bold'), bg='#BBBBBB')
            self.lblContrasena.grid(column=0, row=1, padx=10, pady=5)

            self.lblCedula = tk.Label(self.formulario_frame, text='Cedula del Empleado')
            self.lblCedula.config(font=('ARIAl',15,'bold'), bg='#BBBBBB')
            self.lblCedula.grid(column=0, row=2, padx=10, pady=5)

            # Entrys
            self.svUsuario = tk.StringVar()
            self.entryUsuario = tk.Entry(self.formulario_frame, textvariable=self.svUsuario)
            self.entryUsuario.config(width=40, font=('ARIAL',15))
            self.entryUsuario.grid(column=1, row=0, padx=10, pady=5, columnspan=2)

            self.svContrasena = tk.StringVar()
            self.entryContrasena = tk.Entry(self.formulario_frame, textvariable=self.svContrasena)
            self.entryContrasena.config(width=40, font=('ARIAL',15))
            self.entryContrasena.grid(column=1, row=1, padx=10, pady=5, columnspan=2)

            self.svCedula = tk.StringVar()
            self.entryCedula = tk.Entry(self.formulario_frame, textvariable=self.svCedula)
            self.entryCedula.config(width=40, font=('ARIAL',15))
            self.entryCedula.grid(column=1, row=2, padx=10, pady=5, columnspan=2)

            self.btnGuardar = tk.Button(self.formulario_frame, text='Guardar', command=self.agregarUser)
            self.btnGuardar.config(width=20, font=('Arial', 12, 'bold'), fg='#ffffff', bg='#5CB85C', cursor='hand2')
            self.btnGuardar.grid(column=1, row=3, padx=10, pady=10)

            self.btnCancelar = tk.Button(self.formulario_frame, text='Cancelar')
            self.btnCancelar.config(width=20, font=('Arial', 12, 'bold'), fg='#ffffff', bg='#D9534F', cursor='hand2')
            self.btnCancelar.grid(column=2, row=3, padx=10, pady=10)
    
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
            # Obtengo los datos
            self.idUsuario = self.tablaUser.item(self.tablaUser.selection())['text']  # Trae el ID
            self.nombreUser = self.tablaUser.item(self.tablaUser.selection())['values'][0]
            self.contrasena = self.tablaUser.item(self.tablaUser.selection())['values'][1]
            self.cedulaUser = self.tablaUser.item(self.tablaUser.selection())['values'][4] 

            self.habilitar()

            # Se agregan los datos obtenidos en el entry
            self.entryUsuario.insert(0, self.nombreUser)
            self.entryContrasena.insert(0, self.contrasena)
            self.entryCedula.insert(0, self.cedulaUser)  # Asegúrate de tener un entry para la cédula

        except Exception as e:
            title = 'Editar Usuario'
            mensaje = f'Error al editar Usuario: {e}'
            messagebox.showerror(title, mensaje)



    def agregarUser(self):
        usuario = Usuario(self.entryUsuario.get(), self.entryContrasena.get())  # Asegúrate de pasar la cédula también

        if self.idUsuario is None:
            guardarUsuario(usuario, self.entryCedula.get())
        else:
            editarUsuario(self.idUsuario, usuario, self.entryCedula.get())

        self.deshabilitar()
        self.frame_tablaUsers()

        
    def habilitar(self):
        self.svUsuario.set('')
        self.svContrasena.set('')
        self.svCedula.set('')
        
        self.entryUsuario.config(state='normal')
        self.entryContrasena.config(state='normal')
        self.entryCedula.config(state='normal')
    
        self.btnGuardar.config(state='normal')
        self.btnCancelar.config(state='normal')
        
    def deshabilitar(self):
        self.svUsuario.set('')
        self.svContrasena.set('')
        self.svCedula.set('')
        
        self.entryUsuario.config(state='disabled')
        self.entryContrasena.config(state='disabled')
        self.entryCedula.config(state='disabled')
    
        self.btnGuardar.config(state='disabled')
        self.btnCancelar.config(state='disabled')

