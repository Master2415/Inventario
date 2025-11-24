from tkinter import messagebox
from Conexion.Conexion import conexionBD


def listarProductosConPrecioPromedio():
    """
    Metodo que calclula el precio promedio de las compras por producto ademas de tener una columna que calcula el valor total en el stock del producto
    Se añade (AVG(p.precio) * ps.stock) AS valorInventario a la selección de columnas para calcular el valor del inventario.
    Se agrupa por ps.codigo, ps.nombre, y ps.stock para realizar los cálculos necesarios. 
    """
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return [], 0.0
    
    sql = """
            SELECT ps.codigo, ps.nombre, AVG(p.precio) AS precioPromedio, ps.stock, (AVG(p.precio) * ps.stock) AS valorInventario
            FROM productostock ps
            JOIN producto p ON ps.codigo = p.codigo
            WHERE ps.estado = 1
            GROUP BY ps.codigo, ps.nombre, ps.stock
          """
    
    try:
        cursor = conexion.cursor()
        cursor.execute(sql)
        productos = cursor.fetchall()  # Recupera todos los registros de la consulta
        
        total_valor_inventario = sum([producto[4] for producto in productos])  # Sumar el valorInventario
        
        return productos, total_valor_inventario

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo listar los productos: {e}")
        return [], 0.0

    finally:
        cursor.close()
        conexion.close()

def consulta_productos( fecha_inicio, fecha_fin):
        conexion = conexionBD()
        if conexion is None:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            return []
        
        sql = f"""
        SELECT 
            ps.codigo, 
            ps.nombre, 
            SUM(dv.cantidad) AS cantidad_total, 
            SUM(dv.subTotal) AS total_vendido
        FROM 
            detalleventa dv
        JOIN 
            productostock ps ON dv.producto_idProducto = ps.id
        JOIN 
            venta v ON dv.Venta_idVenta = v.idVenta
        WHERE 
            DATE(v.fecha) BETWEEN '{fecha_inicio}' AND '{fecha_fin}' AND ps.estado = 1
        GROUP BY 
            ps.codigo, ps.nombre
        """
        
        try:
            cursor = conexion.cursor()
            cursor.execute(sql)
            productos = cursor.fetchall()
            return productos
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo listar los productos: {e}")
            return []
        finally:
            cursor.close()
            conexion.close()

def consulta_productos_compra(fecha_inicio, fecha_fin):
        conexion = conexionBD()
        if conexion is None:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            return []
        
        sql = f"""
        SELECT 
            ps.codigo,
            ps.nombre, 
            ps.tipo, 
            ROUND(SUM(p.cantidadStock), 2) AS cantidad_comprada, 
            ROUND(AVG(p.precio), 2) AS precio_promedio, 
            ROUND(SUM(p.cantidadStock), 2) * ROUND(AVG(p.precio), 2) AS precio_total  
        FROM 
            producto p
        JOIN 
            productostock ps ON p.idProductoStock = ps.id
        WHERE 
            ps.estado = 1 AND
            DATE(p.fechaIngreso) BETWEEN '{fecha_inicio}' AND '{fecha_fin}'
        GROUP BY 
            ps.codigo, ps.nombre, ps.tipo
        """
        
        try:
            cursor = conexion.cursor()
            cursor.execute(sql)
            productos = cursor.fetchall()
            return productos
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo listar los productos: {e}")
            return []
        finally:
            cursor.close()
            conexion.close()