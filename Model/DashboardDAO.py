from Conexion.Conexion import conexionBD

def obtener_ventas_por_rango(fecha_inicio, fecha_fin):
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
        print(f"Error al obtener ventas por rango: {e}")
        return 0.0

def obtener_top_productos(limit=5):
    try:
        conexion = conexionBD()
        if conexion is None:
            return []
        
        cursor = conexion.cursor()
        # Top productos vendidos (cantidad total vendida)
        # Corregido: Tabla detalleventa (sin guion bajo) y join con productostock
        sql = f"""
            SELECT ps.nombre, SUM(dv.cantidad) as total_vendido
            FROM detalleventa dv
            JOIN productostock ps ON dv.producto_idProducto = ps.id
            JOIN venta v ON dv.Venta_idVenta = v.idVenta
            GROUP BY ps.id
            ORDER BY total_vendido DESC
            LIMIT {limit}
        """
        cursor.execute(sql)
        resultados = cursor.fetchall()
        conexion.close()
        
        return resultados
    except Exception as e:
        print(f"Error al obtener top productos: {e}")
        return []

def obtener_bajo_stock(limit=10, umbral=10):
    try:
        conexion = conexionBD()
        if conexion is None:
            return []
        
        cursor = conexion.cursor()
        # Productos con stock bajo
        # Corregido: Usar tabla productostock directamente para nombre y stock
        sql = f"""
            SELECT nombre, stock
            FROM productostock
            WHERE stock < {umbral} AND estado = 1
            ORDER BY stock ASC
            LIMIT {limit}
        """
        cursor.execute(sql)
        resultados = cursor.fetchall()
        conexion.close()
        
        return resultados
    except Exception as e:
        print(f"Error al obtener bajo stock: {e}")
        return []
