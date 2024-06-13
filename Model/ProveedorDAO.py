from tkinter import messagebox
from Conexion.Conexion import conexionBD

def listarProveedoresID(idProducto):
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return []
    
    try:
        cursor = conexion.cursor()
        query = """
        SELECT p.idProveedor, p.nombre, p.tipo_proveedor, p.telefono, p.direccion, p.correo
        FROM proveedor p 
        WHERE p.Producto_id = %s AND p.estado = 1   
        """
        cursor.execute(query, (idProducto,))
        proveedores = cursor.fetchall()  # Recupera todos los registros de la consulta
        
        return proveedores

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo listar los Proveedores: {e}")
        return []

    finally:
        cursor.close()
        conexion.close()

def listarProveedores():
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return []
    
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM proveedor WHERE estado = 1")  # Consulta para seleccionar todos los productos
        productos = cursor.fetchall()  # Recupera todos los registros de la consulta
        
        return productos

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo listar los Proveedores: {e}")
        return []

    finally:
        cursor.close()
        conexion.close()

class Proveedor():
    def __init__(self, nombre, tipo_proveedor, telefono, direccion, correo, estado):
        self.nombre = nombre
        self.tipo_proveedor = tipo_proveedor
        self.telefono = telefono
        self.direccion = direccion
        self.correo = correo
        self.estado = estado