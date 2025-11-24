from tkinter import messagebox
from Conexion.Conexion import conexionBD
from Model.ProductoDAO import listarProductos
from Model.ClienteDao import listarClientes
from Model.EmpleadoDAO import listarEmpleado

def obtener_ventas_rango(fecha_inicio, fecha_fin):
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return []
    
    try:
        cursor = conexion.cursor()
        # Asegurarse de incluir la hora final del día para fecha_fin si es necesario, 
        # o asumir que fecha_fin es inclusiva hasta el final del día.
        # Aquí asumimos que las fechas vienen como strings 'YYYY-MM-DD'
        
        sql = """
            SELECT 
                v.idVenta, 
                v.total, 
                v.fecha, 
                u.correo AS correo_usuario, 
                p.cedula AS cedula_cliente,
                p.nombre AS nombre_cliente,
                p.apellido AS apellido_cliente
            FROM 
                venta v
            LEFT JOIN 
                usuario u ON v.usuario_id = u.idusuario
            LEFT JOIN 
                cliente c ON v.cliente_id = c.id
            LEFT JOIN 
                persona p ON c.id = p.id
            WHERE 
                DATE(v.fecha) BETWEEN %s AND %s;
        """
        cursor.execute(sql, (fecha_inicio, fecha_fin))
        ventas = cursor.fetchall()
        return ventas

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo obtener el reporte de ventas: {e}")
        return []

    finally:
        cursor.close()
        conexion.close()
