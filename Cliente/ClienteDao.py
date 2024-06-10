from tkinter import messagebox
from Conexion.Conexion import conexionBD

def listarCondicion(where):
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return []
    
    listarClientes = []
    sql = f'SELECT p.*, c.tipo_cliente FROM Persona p JOIN Cliente c ON p.id = c.id {where}'

    try:
        cursor = conexion.cursor()
        cursor.execute(sql)  
        listarClientes = cursor.fetchall()  # Obtener todos los resultados de la consulta
        conexion.commit()  

    except Exception as e:
        messagebox.showerror('Error', f'Error al listar Clientes: {e}')
    
    finally:
        cursor.close()
        conexion.close()

    return listarClientes  # Devolver los resultados de la consulta


def listarClientes():
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return []
    
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT p.*, c.tipo_cliente FROM Persona p JOIN Cliente c ON p.id = c.id")  # Consulta para seleccionar todos los productos
        productos = cursor.fetchall()  # Recupera todos los registros de la consulta
        
        return productos

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo listar los productos: {e}")
        return []

    finally:
        cursor.close()
        conexion.close()


class Cliente():
    def __init__(self, cedula, nombre, apellido, direccion, correo, telefono, ciudad, tipo):
        self.id = None
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.direccion = direccion
        self.correo = correo
        self.telefono = telefono
        self.ciudad = ciudad
        self.tipo = tipo