from tkinter import messagebox
from Conexion.Conexion import conexionBD

def obtener_id_venta_reciente():
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return None
    
    try:
        cursor = conexion.cursor()
        # Consulta para obtener el ID de la venta más reciente
        cursor.execute("SELECT idVenta FROM Venta ORDER BY idVenta DESC LIMIT 1")
        resultado = cursor.fetchone()

        if resultado:
            return resultado[0]  # Devuelve el primer campo del resultado, que es el ID de la venta más reciente
        else:
            return None  # Retorna None si no se encontró ninguna venta

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo obtener el ID de la venta reciente: {e}")
        return None

    finally:
        cursor.close()
        conexion.close()


def listaDetalleVenta(idVenta):
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return []
    
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT dv.id, dv.cantidad, dv.precio, dv.subTotal, p.nombre, p.codigo 
            FROM detalleventa dv
            JOIN productostock p ON dv.producto_idProducto = p.id
            WHERE dv.Venta_idVenta = %s
        """, (idVenta,))
        resultado = cursor.fetchall()
        return resultado

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo listar los detalles de venta: {e}")
        return []

    finally:
        cursor.close()
        conexion.close()


def guardarDetalle_venta(detalle):
    try:
        conexion = conexionBD()
        if conexion is None:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            return 
        # SQL para insertar en la tabla detalleventa
        sql_detalle = """INSERT INTO detalleventa (cantidad, precio, subTotal, Venta_idVenta, producto_idProducto) 
                         VALUES (%s, %s, %s, %s, %s)"""  
        cursor = conexion.cursor()
        # Ejecutar la consulta SQL para insertar en detalleventa
        cursor.execute(sql_detalle, (detalle['cantidad'], detalle['precio'], detalle['subtotal'], detalle['idVenta'], detalle['idProducto']))
        # Asegurar que los cambios se guarden en la base de datos
        conexion.commit()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el detalle de venta: {e}")
    finally:
        cursor.close()
        conexion.close()

class DetalleVenta:
    def __init__(self, cantidad, precio, subtotal, Venta_idVenta, producto_idProducto):
        self.id = None
        self.cantidad = cantidad
        self.precio = precio
        self.subtotal = subtotal
        self.Venta_idVenta = Venta_idVenta
        self.producto_idProducto = producto_idProducto 