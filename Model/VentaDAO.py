from tkinter import messagebox
from Conexion.Conexion import conexionBD


def listarVentasUsuario(idUsuario):
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return []
    
    try:
        cursor = conexion.cursor()
        cursor.execute("""
                        SELECT 
                            v.idVenta, 
                            v.total, 
                            v.fecha, 
                            u.correo AS correo_usuario, 
                            p.cedula AS cedula_cliente
                        FROM 
                            venta v
                        LEFT JOIN 
                            usuario u ON v.usuario_id = u.idusuario
                        LEFT JOIN 
                            cliente c ON v.cliente_id = c.id
                        LEFT JOIN 
                            persona p ON c.id = p.id
                        WHERE 
                            v.usuario_id = %s;
                    """, (idUsuario,)) 
        ventas = cursor.fetchall() 
        
        return ventas

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo listar las Ventas: {e}")
        return []

    finally:
        cursor.close()
        conexion.close()


def listarVentasCliente(idCliente):
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return []
    
    try:
        cursor = conexion.cursor()
        cursor.execute("""
                        SELECT 
                            v.idVenta, 
                            v.total, 
                            v.fecha, 
                            u.correo AS correo_usuario, 
                            p.cedula AS cedula_cliente
                        FROM 
                            venta v
                        LEFT JOIN 
                            usuario u ON v.usuario_id = u.idusuario
                        LEFT JOIN 
                            cliente c ON v.cliente_id = c.id
                        LEFT JOIN 
                            persona p ON c.id = p.id
                        WHERE 
                            v.cliente_id = %s;
                    """, (idCliente,)) 
        ventas = cursor.fetchall() 
        
        return ventas

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo listar las Ventas: {e}")
        return []

    finally:
        cursor.close()
        conexion.close()


def guardarVenta(venta):
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return
    ventaTotal = str(venta.total).replace(',', '')
    
    sql = """INSERT INTO venta(total, fecha, usuario_id, cliente_id) VALUES
             (%s, %s, %s, %s)"""

    try:
        cursor = conexion.cursor()
        cursor.execute(sql, (ventaTotal, venta.fecha, venta.usuario_id, venta.cliente_id))
        conexion.commit()  # Asegura que los cambios se guarden en la base de datos
        title = 'Registrar Venta'
        mensaje = 'Venta Registrada Exitosamente'
        messagebox.showinfo(title, mensaje) 

    except Exception as e:
        title = 'Registrar Venta'
        mensaje = f'Error al Registrar la Venta: {e}'
        messagebox.showinfo(title, mensaje)
    
    finally:
        cursor.close()
        conexion.close()


def listarVentas():
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return []
    
    try:
        cursor = conexion.cursor()
        cursor.execute("""
                        SELECT 
                            v.idVenta, 
                            v.total, 
                            v.fecha, 
                            u.correo AS correo_usuario, 
                            p.cedula AS cedula_cliente
                        FROM 
                            venta v
                        LEFT JOIN 
                            usuario u ON v.usuario_id = u.idusuario
                        LEFT JOIN 
                            cliente c ON v.cliente_id = c.id
                        LEFT JOIN 
                            persona p ON c.id = p.id
                        WHERE 
                            DATE(v.fecha) = CURDATE();
                    """) 
        ventas = cursor.fetchall() 
        
        return ventas

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo listar las Ventas: {e}")
        return []

    finally:
        cursor.close()
        conexion.close()


class Venta:
    def __init__(self, total, fecha, usuario_id, cliente_id):
        self.idVenta = None
        self.total = total
        self.fecha = fecha
        self.usuario_id = usuario_id
        self.cliente_id = cliente_id

