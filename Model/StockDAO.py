from tkinter import messagebox
from Conexion.Conexion import conexionBD


def listarStock():
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return []
    
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id, codigo, nombre, tipo, utilidad, iva, precioTotal, stock FROM productoStock")  # Consulta para seleccionar todos los productos del stock
        productos = cursor.fetchall()  # Recupera todos los registros de la consulta
        
        return productos

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo listar los productos: {e}")
        return []

    finally:
        cursor.close()
        conexion.close()

def guardarProStock(producto):
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return
    
    # SQL para insertar en la tabla productoStock
    sql_productoStock = f"""INSERT INTO productoStock (codigo, nombre, tipo, utilidad, iva, precioTotal, stock) VALUES
                            ('{producto.codigo}', '{producto.nombre}', '{producto.tipo}', {producto.utilidad}, {producto.iva}, {producto.precioTotal}, {producto.stock})"""
    
    try:
        cursor = conexion.cursor()
        cursor.execute(sql_productoStock)
        conexion.commit() # Asegurar que los cambios se guarden en la base de datos
        title = 'Registrar Producto'
        mensaje = 'Producto Registrado Exitosamente'
        messagebox.showinfo(title, mensaje)
    except Exception as e:
        title = 'Registrar Producto'
        mensaje = f'Error al Registrar el Producto: {e}'
        messagebox.showinfo(title, mensaje)
    finally:
        cursor.close()
        conexion.close()


class productoStock():
    def __init__(self, codigo, nombre, tipo, utilidad, iva, precioTotal, stock):
        self.id = None
        self.codigo = codigo
        self.nombre = nombre
        self.tipo = tipo
        self.utilidad = utilidad
        self.iva = iva
        self.precioTotal = precioTotal
        self.stock = stock