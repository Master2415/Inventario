from tkinter import messagebox
from Conexion.Conexion import conexionBD

def calcular_ventas_totales(fecha_inicio, fecha_fin):
    try:
        conexion = conexionBD()
        if conexion is None:
            return 0.0
        
        cursor = conexion.cursor()
        sql = f"""
            SELECT SUM(total) 
            FROM venta 
            WHERE DATE(fecha) BETWEEN '{fecha_inicio}' AND '{fecha_fin}'
        """
        cursor.execute(sql)
        resultado = cursor.fetchone()
        conexion.close()
        
        return resultado[0] if resultado and resultado[0] else 0.0
    except Exception as e:
        print(f"Error al calcular ventas totales: {e}")
        return 0.0

def calcular_compras_totales(fecha_inicio, fecha_fin):
    try:
        conexion = conexionBD()
        if conexion is None:
            return 0.0
        
        cursor = conexion.cursor()
        # Se asume que el costo de compra es precio * cantidadStock en la tabla producto
        # producto.precio es el precio de compra/costo
        sql = f"""
            SELECT SUM(p.precio * p.cantidadStock) 
            FROM producto p
            JOIN productostock ps ON p.idProductoStock = ps.id
            WHERE ps.estado = 1 AND DATE(p.fechaIngreso) BETWEEN '{fecha_inicio}' AND '{fecha_fin}'
        """
        cursor.execute(sql)
        resultado = cursor.fetchone()
        conexion.close()
        
        return resultado[0] if resultado and resultado[0] else 0.0
    except Exception as e:
        print(f"Error al calcular compras totales: {e}")
        return 0.0

def calcular_horas_trabajadas_totales():
    try:
        conexion = conexionBD()
        if conexion is None:
            return 0.0
        
        cursor = conexion.cursor()
        sql = "SELECT SUM(horasTrabajadas) FROM empleado WHERE estado = 1"
        cursor.execute(sql)
        resultado = cursor.fetchone()
        conexion.close()
        
        return resultado[0] if resultado and resultado[0] else 0.0
    except Exception as e:
        print(f"Error al calcular horas trabajadas: {e}")
        return 0.0
