import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from Model.CajaDAO import *
from Model.UsuarioDAO import obtenerIdUsuario
from Conexion.Conexion import conexionBD

class Frame_Caja(tk.Frame):
    def __init__(self, root, width=1745, height=750):
        super().__init__(root, width=width, height=height)
        self.root = root
        self.config(bg='#f0f2f5')
        self.pack(fill='both', expand=True)
        
        # Obtener ID del usuario actual desde la aplicación principal
        # self.root es frame_main, su master es la instancia de Aplicacion
        self.idUsuario = obtenerIdUsuario(self.root.master.usuario_actual)
        
        self.crear_tabs()
        self.verificar_estado_caja()

    def crear_tabs(self):
        self.tabControl = ttk.Notebook(self)
        
        # Tab Control de Caja
        self.tab_control = tk.Frame(self.tabControl, bg='#f0f2f5')
        self.tabControl.add(self.tab_control, text='Control de Caja')
        
        # Tab Historial
        self.tab_historial = tk.Frame(self.tabControl, bg='#f0f2f5')
        self.tabControl.add(self.tab_historial, text='Historial')
        
        self.tabControl.pack(expand=1, fill="both", padx=10, pady=10)
        
        # Inicializar contenido de Historial
        self.crear_tabla_historial()

    def verificar_estado_caja(self):
        # Limpiar tab de control
        for widget in self.tab_control.winfo_children():
            widget.destroy()
            
        if self.idUsuario:
            self.idCajaAbierta = verificarCajaAbierta(self.idUsuario)
            
            if self.idCajaAbierta:
                self.mostrar_panel_caja_abierta()
            else:
                self.mostrar_panel_apertura()
        else:
            tk.Label(self.tab_control, text="Error: No se pudo identificar al usuario.", bg='#f0f2f5', fg='red').pack(pady=20)

    def mostrar_panel_apertura(self):
        frame_apertura = tk.Frame(self.tab_control, bg='white', padx=40, pady=40)
        frame_apertura.place(relx=0.5, rely=0.5, anchor='center')
        frame_apertura.configure(highlightbackground="#d1d1d1", highlightthickness=1)

        tk.Label(frame_apertura, text="APERTURA DE CAJA", font=('Segoe UI', 20, 'bold'), bg='white', fg='#2c3e50').pack(pady=(0, 20))
        
        tk.Label(frame_apertura, text="Monto Inicial (Efectivo en caja)", font=('Segoe UI', 12), bg='white').pack(anchor='w')
        self.svMontoInicial = tk.StringVar()
        entry_monto = tk.Entry(frame_apertura, textvariable=self.svMontoInicial, font=('Segoe UI', 14), width=20)
        entry_monto.pack(pady=(5, 20))
        
        btn_abrir = tk.Button(frame_apertura, text="ABRIR CAJA", command=self.accion_abrir_caja,
                            font=('Segoe UI', 12, 'bold'), fg='white', bg='#27ae60', relief='flat', cursor='hand2', width=20)
        btn_abrir.pack(pady=10)

    def mostrar_panel_caja_abierta(self):
        datos = obtenerDatosCaja(self.idCajaAbierta)
        if not datos:
            messagebox.showerror("Error", "No se pudieron obtener los datos de la caja.")
            return

        hora_inicio = datos[0]
        monto_inicial = datos[1]
        total_ventas = datos[2]
        total_esperado = monto_inicial + total_ventas

        frame_info = tk.Frame(self.tab_control, bg='#f0f2f5')
        frame_info.pack(fill='both', expand=True, padx=50, pady=20)

        # Encabezado
        tk.Label(frame_info, text="CAJA ABIERTA", font=('Segoe UI', 24, 'bold'), bg='#f0f2f5', fg='#27ae60').pack(pady=20)

        # Tarjetas de Información
        frame_cards = tk.Frame(frame_info, bg='#f0f2f5')
        frame_cards.pack(pady=20)

        self.crear_card(frame_cards, "Hora Apertura", str(hora_inicio), 0, 0)
        self.crear_card(frame_cards, "Monto Inicial", f"${monto_inicial:,.2f}", 0, 1)
        self.crear_card(frame_cards, "Ventas del Turno", f"${total_ventas:,.2f}", 0, 2)
        self.crear_card(frame_cards, "Total Esperado", f"${total_esperado:,.2f}", 0, 3)

        # Sección de Cierre
        frame_cierre = tk.Frame(frame_info, bg='white', padx=30, pady=30)
        frame_cierre.pack(pady=40)
        frame_cierre.configure(highlightbackground="#d1d1d1", highlightthickness=1)

        tk.Label(frame_cierre, text="CERRAR CAJA", font=('Segoe UI', 16, 'bold'), bg='white', fg='#c0392b').pack(pady=(0, 15))
        
        tk.Label(frame_cierre, text="Monto Final (Conteo de Efectivo)", font=('Segoe UI', 12), bg='white').pack(anchor='w')
        self.svMontoFinal = tk.StringVar()
        entry_final = tk.Entry(frame_cierre, textvariable=self.svMontoFinal, font=('Segoe UI', 14), width=20)
        entry_final.pack(pady=(5, 20))

        btn_cerrar = tk.Button(frame_cierre, text="Confirmar Cierre", command=self.accion_cerrar_caja,
                             font=('Segoe UI', 12, 'bold'), fg='white', bg='#c0392b', relief='flat', cursor='hand2', width=20)
        btn_cerrar.pack()

    def crear_card(self, parent, title, value, row, col):
        card = tk.Frame(parent, bg='white', padx=20, pady=15, width=200)
        card.grid(row=row, column=col, padx=10)
        card.configure(highlightbackground="#e0e0e0", highlightthickness=1)
        
        tk.Label(card, text=title, font=('Segoe UI', 10, 'bold'), bg='white', fg='#7f8c8d').pack()
        tk.Label(card, text=value, font=('Segoe UI', 14, 'bold'), bg='white', fg='#2c3e50').pack(pady=(5,0))

    def accion_abrir_caja(self):
        try:
            monto = float(self.svMontoInicial.get())
            if abrirCaja(self.idUsuario, monto):
                messagebox.showinfo("Éxito", "Caja abierta correctamente.")
                self.verificar_estado_caja()
        except ValueError:
            messagebox.showerror("Error", "Ingrese un monto válido.")

    def accion_cerrar_caja(self):
        try:
            monto = float(self.svMontoFinal.get())
            if cerrarCaja(self.idCajaAbierta, monto):
                messagebox.showinfo("Éxito", "Caja cerrada correctamente.")
                self.verificar_estado_caja()
                self.cargar_historial() # Actualizar historial
        except ValueError:
            messagebox.showerror("Error", "Ingrese un monto válido.")

    def crear_tabla_historial(self):
        # Frame para la tabla
        frame_tabla = tk.Frame(self.tab_historial, bg='#f0f2f5')
        frame_tabla.pack(fill='both', expand=True, padx=20, pady=20)

        columns = ('ID', 'Apertura', 'Cierre', 'Monto Inicial', 'Monto Final', 'Usuario', 'Ventas')
        self.tree_historial = ttk.Treeview(frame_tabla, columns=columns, show='headings')
        
        for col in columns:
            self.tree_historial.heading(col, text=col)
            self.tree_historial.column(col, width=120, anchor='center')
        
        self.tree_historial.column('Apertura', width=150)
        self.tree_historial.column('Cierre', width=150)

        scrollbar = ttk.Scrollbar(frame_tabla, orient='vertical', command=self.tree_historial.yview)
        self.tree_historial.configure(yscroll=scrollbar.set)
        
        self.tree_historial.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Botón actualizar
        btn_refresh = tk.Button(self.tab_historial, text="Actualizar Historial", command=self.cargar_historial,
                              font=('Segoe UI', 10), bg='#3498db', fg='white', relief='flat', cursor='hand2')
        btn_refresh.pack(pady=10)
        
        self.cargar_historial()

    def cargar_historial(self):
        for item in self.tree_historial.get_children():
            self.tree_historial.delete(item)
            
        historial = listarHistorialCajas()
        for h in historial:
            # h = (id, inicio, fin, m_ini, m_fin, usuario, ventas)
            self.tree_historial.insert('', 'end', values=(
                h[0], h[1], h[2], 
                f"${h[3]:,.2f}", f"${h[4]:,.2f}", 
                h[5], f"${h[6]:,.2f}"
            ))
