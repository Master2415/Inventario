from tkinter import messagebox
from Conexion.Conexion import conexionBD
from datetime import datetime

def verificarCajaAbierta(idUsuario):
    conexion = conexionBD()
    if conexion is None:
        return None
    
    try:
        cursor = conexion.cursor()
        # Verificar si hay una caja con estado 1 (abierta) para este usuario
        cursor.execute("SELECT idCaja FROM caja WHERE idUser = %s AND estado = 1 LIMIT 1", (idUsuario,))
        resultado = cursor.fetchone()
        if resultado:
            return resultado[0] # Retorna el idCaja
        else:
            return None
    except Exception as e:
        messagebox.showerror("Error", f"Error al verificar caja: {e}")
        return None
    finally:
        cursor.close()
        conexion.close()

def abrirCaja(idUsuario, montoInicial):
    conexion = conexionBD()
    if conexion is None:
        return False
    
    try:
        cursor = conexion.cursor()
        fecha_inicio = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        sql = """INSERT INTO caja (horaInicio, montoApertura, estado, idUser) 
                 VALUES (%s, %s, 1, %s)"""
        cursor.execute(sql, (fecha_inicio, montoInicial, idUsuario))
        conexion.commit()
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Error al abrir caja: {e}")
        return False
    finally:
        cursor.close()
        conexion.close()

def cerrarCaja(idCaja, montoFinal):
    conexion = conexionBD()
    if conexion is None:
        return False
    
    try:
        cursor = conexion.cursor()
        fecha_fin = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        sql = """UPDATE caja 
                 SET horaFin = %s, montoFin = %s, estado = 0 
                 WHERE idCaja = %s"""
        cursor.execute(sql, (fecha_fin, montoFinal, idCaja))
        conexion.commit()
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Error al cerrar caja: {e}")
        return False
    finally:
        cursor.close()
        conexion.close()

def obtenerDatosCaja(idCaja):
    conexion = conexionBD()
    if conexion is None:
        return None
    
    try:
        cursor = conexion.cursor()
        # Obtener datos de la caja y el total de ventas asociado
        sql = """
            SELECT 
                c.horaInicio, 
                c.montoApertura,
                (SELECT COALESCE(SUM(v.total), 0) 
                 FROM venta v 
                 WHERE v.usuario_id = c.idUser 
                 AND v.fecha >= c.horaInicio) as totalVentas
            FROM caja c
            WHERE c.idCaja = %s
        """
        cursor.execute(sql, (idCaja,))
        resultado = cursor.fetchone()
        return resultado
    except Exception as e:
        messagebox.showerror("Error", f"Error al obtener datos de caja: {e}")
        return None
    finally:
        cursor.close()
        conexion.close()

def listarHistorialCajas():
    conexion = conexionBD()
    if conexion is None:
        return []
    
    try:
        cursor = conexion.cursor()
        # Listar solo cajas cerradas (estado 0)
        cursor.execute("""
                        SELECT 
                            c.idCaja, 
                            c.horaInicio, 
                            c.horaFin, 
                            c.montoApertura, 
                            c.montoFin, 
                            u.correo,
                            (SELECT COALESCE(SUM(v.total), 0) 
                             FROM venta v 
                             WHERE v.usuario_id = c.idUser 
                             AND v.fecha >= c.horaInicio 
                             AND v.fecha <= c.horaFin) as totalVentas
                        FROM caja c 
                        JOIN usuario u on c.idUser = u.idusuario
                        WHERE c.estado = 0 
                        ORDER BY c.idCaja DESC
                        """)  
        cajas = cursor.fetchall()
        return cajas
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo listar el historial: {e}")
        return []
    finally:
        cursor.close()
        conexion.close()
