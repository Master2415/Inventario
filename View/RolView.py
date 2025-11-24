import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import *
from Model.RolDAO import *

class RolView(tk.Frame):
    def __init__(self, root, width=1280, height=720):
        super().__init__(root, width=width, height=height)
        self.root = root
        self.config(bg='#f0f2f5')  # Establecer el color de fondo del frame principal
        self.pack(fill='both', expand=True)
        self.idRol = None
        self.frame_tablaRoles()
        self.deshabilitar()
     
    def frame_tablaRoles(self, where=""):
        if hasattr(self, 'tablaRol'):
            self.tablaRol.delete(*self.tablaRol.get_children())

        if len(where) > 0:
            self.listaRol = listarRolWhere(where)
        else:
            self.listaRol = listarRol()

        if not hasattr(self, 'tabla_frame'):
            self.tabla_frame = tk.Frame(self)
            self.tabla_frame.pack(fill='x', expand=False)

            self.tablaRol = ttk.Treeview(self.tabla_frame, height=10, columns=('ID', 'Rol', 'Salario'))
            self.scrollEmpleado = ttk.Scrollbar(self.tabla_frame, orient='vertical', command=self.tablaRol.yview)
            self.tablaRol.configure(yscroll=self.scrollEmpleado.set)
            self.tablaRol.pack(side='left', fill='both', expand=True)
            self.tablaRol.pack(side='right', fill='y')

            self.tablaRol.heading('#0', text='ID')
            self.tablaRol.heading('#1', text='Rol')
            self.tablaRol.heading('#2', text='Salario Mensual')

            self.tablaRol.column("#0", anchor='w', width=100)
            self.tablaRol.column("#1", anchor='w', width=180)
            self.tablaRol.column("#2", anchor='w', width=180)
          
  
        for p in self.listaRol:
            self.tablaRol.insert('', 'end', text=p[0], values=(p[1], p[2]), tags=('evenrow',))

        if not hasattr(self, 'botones_frame'):
            self.botones_frame = tk.Frame(self, bg='#f0f2f5')
            self.botones_frame.pack(pady=10)

            self.btnNuevo = tk.Button(self.botones_frame, text='Agregar', command=self.habilitar)
            self.btnNuevo.config(width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#27ae60', relief='flat', cursor='hand2')
            self.btnNuevo.grid(column=0, row=0, padx=10, pady=5)

            self.btnEditar = tk.Button(self.botones_frame, text='Editar', command=self.editarRol)
            self.btnEditar.config(width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#3498db', relief='flat', cursor='hand2')
            self.btnEditar.grid(column=1, row=0, padx=10, pady=5)

            self.btnEliminar = tk.Button(self.botones_frame, text='Eliminar', command=self.eliminarRol)
            self.btnEliminar.config(width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#c0392b', relief='flat', cursor='hand2')
            self.btnEliminar.grid(column=2, row=0, padx=10, pady=5)

        if not hasattr(self, 'formulario_frame'):
            self.formulario_frame = tk.Frame(self, bg='#f0f2f5')
            self.formulario_frame.pack(pady=10)

            self.lblnombreRol = tk.Label(self.formulario_frame, text='Nombre del Rol')
            self.lblnombreRol.config(font=('Segoe UI', 15, 'bold'), bg='#f0f2f5')
            self.lblnombreRol.grid(column=0, row=0, padx=10, pady=5)

            self.lblSalario = tk.Label(self.formulario_frame, text='Salario')
            self.lblSalario.config(font=('Segoe UI', 15, 'bold'), bg='#f0f2f5')
            self.lblSalario.grid(column=0, row=1, padx=10, pady=5)

            # Entrys
            self.svNombreRol = tk.StringVar()
            self.entruNombreRol = tk.Entry(self.formulario_frame, textvariable=self.svNombreRol)
            self.entruNombreRol.config(width=40, font=('Segoe UI', 15))
            self.entruNombreRol.grid(column=1, row=0, padx=10, pady=5, columnspan=2)

            self.svSalario = tk.StringVar()
            self.entrySalario = tk.Entry(self.formulario_frame, textvariable=self.svSalario)
            self.entrySalario.config(width=40, font=('Segoe UI', 15))
            self.entrySalario.grid(column=1, row=1, padx=10, pady=5, columnspan=2)

            self.btnGuardar = tk.Button(self.formulario_frame, text='Guardar', command=self.agregarRol)
            self.btnGuardar.config(width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#27ae60', relief='flat', cursor='hand2')
            self.btnGuardar.grid(column=1, row=10, padx=10, pady=10)

            self.btnCancelar = tk.Button(self.formulario_frame, text='Cancelar')
            self.btnCancelar.config(width=20, font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#c0392b', relief='flat', cursor='hand2')
            self.btnCancelar.grid(column=2, row=10, padx=10, pady=10)
    
    def eliminarRol(self):
        try:
            self.idRol = self.tablaRol.item(self.tablaRol.selection())['text']
            eliminarRol(self.idRol)
            
            self.frame_tablaRoles()
            self.idRol = None
        except:
            title = 'Eliminar Rol'
            mensaje = 'No se pudo eliminar Rol'
            messagebox.showinfo(title, mensaje)
    
    def editarRol(self):
        try:
            # Obtengo los datos
            self.idRol                 = self.tablaRol.item(self.tablaRol.selection())['text'] #Trae el ID
            self.nombrerol                    = self.tablaRol.item(self.tablaRol.selection())['values'][0]
            self.salario                    = self.tablaRol.item(self.tablaRol.selection())['values'][1]
            
            self.habilitar()

            # Se agregan los datos obtenidos en el entry
            self.entruNombreRol.insert(0, self.nombrerol)
            self.entrySalario.insert(0, self.salario)
   
        except:
            title = 'Editar Rol'
            mensaje = 'Error al editar Rol'
            messagebox.showerror(title, mensaje)


    def agregarRol(self):
        rol = Rol(self.entruNombreRol.get(), self.entrySalario.get())

        if self.idRol == None:
            guardarRol(rol)
        else: 
            editarRol(rol, self.idRol)

        self.deshabilitar()
        self.frame_tablaRoles()
        
    def habilitar(self):
        self.svNombreRol.set('')
        self.svSalario.set('')
        
        self.entruNombreRol.config(state='normal')
        self.entrySalario.config(state='normal')
    
        self.btnGuardar.config(state='normal')
        self.btnCancelar.config(state='normal')
        
    def deshabilitar(self):
        self.svNombreRol.set('')
        self.svSalario.set('')
        
        self.entruNombreRol.config(state='disabled')
        self.entrySalario.config(state='disabled')
    
        self.btnGuardar.config(state='disabled')
        self.btnCancelar.config(state='disabled')
