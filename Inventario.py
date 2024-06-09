import tkinter as tk
from Producto.ProductoView import Frame_Producto

def main():
    root = tk.Tk()
    root.title('Historial Medico')
    root.resizable(0, 0)

    app = Frame_Producto(root)
    app.mainloop()  # Para que se mantenga ejecutado


if __name__ == '__main__':
    main()
