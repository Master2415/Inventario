from tkinter import messagebox
from Conexion.Conexion import conexionBD

def listarVentas():
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return []
    
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM venta") 
        ventas = cursor.fetchall() 
        
        return ventas

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo listar las Ventas: {e}")
        return []

    finally:
        cursor.close()
        conexion.close()

class Ventas:
    def __init__(self, total, fecha, usuario_id, cliente_id):
        self.idVenta = None
        self.total = total
        self.fecha = fecha
        self.usuario_id = usuario_id
        self.cliente_id = cliente_id

