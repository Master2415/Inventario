import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import *
from Model.CajaDAO import *
from Model.UsuarioDAO import obtener_Users_combobox

class Frame_Caja(tk.Frame):

    def __init__(self, root, width=1745, height=750):
        super().__init__(root, width=width, height=height)
        self.root = root
        self.config(bg='#f0f0f0')  # Establecer el color de fondo del frame principal
        self.pack(fill='both', expand=True)
        self.idCaja = None # Usado para acceder a los metodos
        self.tablaCajas()
        self.cargar_usuarios()
        self.deshabilitar()


    def tablaCajas(self):
        if hasattr(self, 'tablaCaja'):
            self.tablaCaja.delete(*self.tablaCaja.get_children())

        self.listCaja = listarCaja()

        if not hasattr(self, 'frame_tablaCaja'):
            self.frame_tablaCaja = tk.Frame(self)
            self.frame_tablaCaja.pack(fill='x', expand=False)

            # Crear la tablaCaja con barra de desplazamiento
            self.tablaCaja = ttk.Treeview(self.frame_tablaCaja, columns=('ID', 'horaInicio', 'horaFin', 'montoApertura', 'montoFin', 'Usuario'))
            self.scrollbar = ttk.Scrollbar(self.frame_tablaCaja, orient='vertical', command=self.tablaCaja.yview)
            self.tablaCaja.configure(yscroll=self.scrollbar.set)
            self.tablaCaja.pack(side='left', fill='both', expand=True)
            self.scrollbar.pack(side='right', fill='y')

            self.tablaCaja.heading('#0', text='ID')
            self.tablaCaja.heading('#1', text='Hora Apertura')
            self.tablaCaja.heading('#2', text='Fora Cierre')
            self.tablaCaja.heading('#3', text='Monto Apertura')
            self.tablaCaja.heading('#4', text='Monto Cierre')
            self.tablaCaja.heading('#5', text='Usuario')

            self.tablaCaja.column("#0", anchor='w', width=70)
            self.tablaCaja.column("#1", anchor='w', width=100)
            self.tablaCaja.column("#2", anchor='w', width=130)
            self.tablaCaja.column("#3", anchor='w', width=150)
            self.tablaCaja.column("#4", anchor='w', width=150)
            self.tablaCaja.column("#5", anchor='w', width=200)
            

        for p in self.listCaja:
            monto1 = "{:,.2f}".format(p[3]) 
            monto2 = "{:,.2f}".format(p[4]) 
            self.tablaCaja.insert('', 'end', text=p[0], values=(p[1], p[2], monto1, monto2, p[5]), tags=('evenrow',))

        # Botones debajo de la tabla
        if not hasattr(self, 'botones_frame'):
            self.botones_frame = tk.Frame(self, bg='#f0f0f0')
            self.botones_frame.pack(pady=10)

            #Botones
            self.btnNuevo = tk.Button(self.botones_frame, text='Nuevo Registro', command=self.habilitar)
            self.btnNuevo.config(width=20, font=('ARIAL',12,'bold'), fg='#ffffff', bg='#5CB85C')
            self.btnNuevo.grid(column=0, row=0, padx=10, pady=5)

            self.btnEditar = tk.Button(self.botones_frame, text='Editar', command=self.editarCaja)
            self.btnEditar.config(width=20, font=('ARIAL',12,'bold'), fg='#ffffff', bg='#007ACC')
            self.btnEditar.grid(column=1, row=0, padx=10, pady=5)

            self.btnEliminar = tk.Button(self.botones_frame, text='Eliminar', command=self.eliminarCaja)
            self.btnEliminar.config(width=20, font=('ARIAL',12,'bold'), fg='#ffffff', bg='#D9534F')
            self.btnEliminar.grid(column=3, row=0, padx=10, pady=5)

        if not hasattr(self, 'formulario_frame'):
            self.formulario_frame = tk.Frame(self, bg='#BBBBBB')
            self.formulario_frame.pack(fill='x', padx=20, pady=10)

            self.lblHoraInicio = tk.Label(self.formulario_frame, text='Hora de Apertura')
            self.lblHoraInicio.config(font=('ARIAl',15,'bold'), bg='#BBBBBB')
            self.lblHoraInicio.grid(column=0, row=0, padx=10, pady=5)

            self.lblHoraFin = tk.Label(self.formulario_frame, text='Hora de Cierre')
            self.lblHoraFin.config(font=('ARIAl',15,'bold'), bg='#BBBBBB')
            self.lblHoraFin.grid(column=0, row=1, padx=10, pady=5)

            self.lblMontoApertura = tk.Label(self.formulario_frame, text='Monto de Apertura')
            self.lblMontoApertura.config(font=('ARIAl',15,'bold'), bg='#BBBBBB')
            self.lblMontoApertura.grid(column=0, row=2, padx=10, pady=5)

            self.lblMontoFin = tk.Label(self.formulario_frame, text='Monto de Cierre')
            self.lblMontoFin.config(font=('ARIAl',15,'bold'), bg='#BBBBBB')
            self.lblMontoFin.grid(column=0, row=3, padx=10, pady=5)

            self.lblBox = tk.Label(self.formulario_frame, text='Usuarios')
            self.lblBox.config(font=('ARIAl',15,'bold'), bg='#BBBBBB')
            self.lblBox.grid(column=0, row=4, padx=10, pady=5)

            # Entrys
            self.svHinicio = tk.StringVar()
            self.entryHinicio = tk.Entry(self.formulario_frame, textvariable=self.svHinicio)
            self.entryHinicio.config(width=40, font=('ARIAL',15))
            self.entryHinicio.grid(column=1, row=0, padx=10, pady=5, columnspan=2)

            self.svHfin = tk.StringVar()
            self.entryHfin = tk.Entry(self.formulario_frame, textvariable=self.svHfin)
            self.entryHfin.config(width=40, font=('ARIAL',15))
            self.entryHfin.grid(column=1, row=1, padx=10, pady=5, columnspan=2)

            self.svMapertura = tk.StringVar()
            self.entryApertura = tk.Entry(self.formulario_frame, textvariable=self.svMapertura)
            self.entryApertura.config(width=40, font=('ARIAL',15))
            self.entryApertura.grid(column=1, row=2, padx=10, pady=5, columnspan=2)

            self.svMfin = tk.StringVar()
            self.entryMfin = tk.Entry(self.formulario_frame, textvariable=self.svMfin)
            self.entryMfin.config(width=40, font=('ARIAL',15))
            self.entryMfin.grid(column=1, row=3, padx=10, pady=5, columnspan=2)

            self.boxusuarios = ttk.Combobox(self.formulario_frame, state='readonly')
            self.boxusuarios.config(width=40, font=('Arial', 12))
            self.boxusuarios.grid(column=1, row=4, padx=10, pady=5, columnspan=2)

             # Botones
            self.btnGuardar = tk.Button(self.formulario_frame, text='Guardar', command=self.agregar)
            self.btnGuardar.config(width=20, font=('Arial', 12, 'bold'), fg='#ffffff', bg='#5CB85C')
            self.btnGuardar.grid(column=1, row=5, padx=10, pady=5)

            self.btnCancelar = tk.Button(self.formulario_frame, text='Cancelar', command=self.deshabilitar)
            self.btnCancelar.config(width=20, font=('Arial', 12, 'bold'), fg='#ffffff', bg='#D9534F')
            self.btnCancelar.grid(column=2, row=5, padx=10, pady=5)


    def cargar_usuarios(self):
        try:
            lista_users = obtener_Users_combobox()  # Obtener los usuarios
            self.boxusuarios['values'] = lista_users  # Asignar la lista de nombres de usuarios al Combobox
            if lista_users:
                self.boxusuarios.current(0)  # Establecer la selección inicial, si hay usuarios cargados
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar los usuarios: {e}")

    def agregar(self):
        self.usuario = self.boxusuarios.get()
        caja = Caja(self.svHinicio.get(), self.svHfin.get(), self.svMapertura.get(), self.svMfin.get())

        if self.idCaja == None:
            agregar(caja, self.usuario)
        else:
            editarCaja(caja, self.idCaja, self.usuario)
        
        self.tablaCajas()
        self.deshabilitar()
    
    def eliminarCaja(self):
        
            self.idCaja = self.tablaCaja.item(self.tablaCaja.selection())['text']
            eliminarCaja(self.idCaja)
            
            self.tablaCajas()

        

    def editarCaja(self):
        try:
            # Obtengo los datos
            self.idCaja                 = self.tablaCaja.item(self.tablaCaja.selection())['text'] #Trae el ID
            self.hinicio                    = self.tablaCaja.item(self.tablaCaja.selection())['values'][0]
            self.hfin                    = self.tablaCaja.item(self.tablaCaja.selection())['values'][1]
            self.maper                  = self.tablaCaja.item(self.tablaCaja.selection())['values'][2]
            self.mfin                 = self.tablaCaja.item(self.tablaCaja.selection())['values'][3]
            self.usuario                    = self.tablaCaja.item(self.tablaCaja.selection())['values'][4]
           
            
            self.habilitar()

            # Se agregan los datos obtenidos en el entry
            self.entryHinicio.insert(0, self.hinicio)
            self.entryHfin.insert(0, self.hfin)
            self.entryApertura.insert(0, self.maper)
            self.entryMfin.insert(0, self.mfin)
            self.boxusuarios.insert(0, self.usuario)

        except:
            title = 'Editar Caja'
            mensaje = 'Error al editar Caja'
            messagebox.showerror(title, mensaje)


    def habilitar(self):
        self.svHinicio.set('')
        self.svHfin.set('')
        self.svMapertura.set('')
        self.svMfin.set('')
        self.boxusuarios.set('')

        self.entryHinicio.config(state='normal')
        self.entryHfin.config(state='normal')
        self.entryApertura.config(state='normal')
        self.entryMfin.config(state='normal')
        self.boxusuarios.config(state='normal')

        self.btnGuardar.config(state='normal')
        self.btnCancelar.config(state='normal') 

    def deshabilitar(self):
        self.svHinicio.set('')
        self.svHfin.set('')
        self.svMapertura.set('')
        self.svMfin.set('')
        self.boxusuarios.set('')

        self.entryHinicio.config(state='disabled')
        self.entryHfin.config(state='disabled')
        self.entryApertura.config(state='disabled')
        self.entryMfin.config(state='disabled')
        self.boxusuarios.config(state='disabled')

        self.btnGuardar.config(state='disabled')
        self.btnCancelar.config(state='disabled') 

