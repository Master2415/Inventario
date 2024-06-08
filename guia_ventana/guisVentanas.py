import tkinter as tk
from tkinter import ttk

class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplicación con Barra Lateral")
        self.geometry("800x600")
        self.config(bg='#CDD8FF')

        # Crear el marco de la barra lateral
        self.frame_sidebar = tk.Frame(self, width=200, bg='#53005B')
        self.frame_sidebar.pack(side='right', fill='y')

        # Crear el marco de contenido principal
        self.frame_main = tk.Frame(self, bg='#FFFFFF')
        self.frame_main.pack(side='right', expand=True, fill='both')

        # Botones de la barra lateral
        self.btnAgregarHistoria = tk.Button(self.frame_sidebar, text="Agregar Historia", command=self.mostrarAgregarHistoria)
        self.btnAgregarHistoria.pack(fill='x', pady=5, padx=5)

        self.btnOtraOpcion = tk.Button(self.frame_sidebar, text="Otra Opción", command=self.mostrarOtraOpcion)
        self.btnOtraOpcion.pack(fill='x', pady=5, padx=5)

    def mostrarAgregarHistoria(self):
        # Limpiar el contenido anterior del marco principal
        for widget in self.frame_main.winfo_children():
            widget.destroy()

        # Agregar widgets para "Agregar Historia"
        lblMotivoHistoria = tk.Label(self.frame_main, text='Motivo de la Historia Medica', width=30, font=('ARIAL', 15, 'bold'), bg='#CDD8FF')
        lblMotivoHistoria.grid(row=0, column=0, padx=5, pady=3)

        entryMotivoHistoria = tk.Entry(self.frame_main, width=64, font=('ARIAL', 15))
        entryMotivoHistoria.grid(row=0, column=1, padx=5, pady=3, columnspan=2)

        # Agrega más widgets según sea necesario

    def mostrarOtraOpcion(self):
        # Limpiar el contenido anterior del marco principal
        for widget in self.frame_main.winfo_children():
            widget.destroy()

        # Agregar widgets para "Otra Opción"
        lblOtraOpcion = tk.Label(self.frame_main, text='Otra Opción Seleccionada', font=('ARIAL', 15, 'bold'), bg='#CDD8FF')
        lblOtraOpcion.pack(pady=20)

        # Agrega más widgets según sea necesario

if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()
