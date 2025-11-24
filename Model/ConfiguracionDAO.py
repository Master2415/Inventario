from Conexion.Conexion import conexionBD
from tkinter import messagebox

def crear_tabla_configuracion():
    try:
        conexion = conexionBD()
        if conexion is None:
            return
        
        cursor = conexion.cursor()
        sql = """
            CREATE TABLE IF NOT EXISTS configuracion_empresa (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre_empresa VARCHAR(100),
                nit_rut VARCHAR(50),
                direccion VARCHAR(200),
                telefono VARCHAR(50),
                slogan VARCHAR(200),
                mensaje_final VARCHAR(200)
            )
        """
        cursor.execute(sql)
        conexion.commit()
        
        # Insertar registro por defecto si no existe
        cursor.execute("SELECT COUNT(*) FROM configuracion_empresa")
        if cursor.fetchone()[0] == 0:
            sql_insert = """
                INSERT INTO configuracion_empresa (nombre_empresa, nit_rut, direccion, telefono, slogan, mensaje_final)
                VALUES ('Mi Empresa', '000000000', 'Dirección Local', '0000000', 'Slogan de la empresa', '¡Gracias por su compra!')
            """
            cursor.execute(sql_insert)
            conexion.commit()
            
        conexion.close()
    except Exception as e:
        print(f"Error al crear tabla configuracion: {e}")

def obtener_configuracion():
    try:
        conexion = conexionBD()
        if conexion is None:
            return None
        
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM configuracion_empresa LIMIT 1")
        resultado = cursor.fetchone()
        conexion.close()
        return resultado
    except Exception as e:
        print(f"Error al obtener configuracion: {e}")
        return None

def guardar_configuracion(nombre, nit, direccion, telefono, slogan, mensaje):
    try:
        conexion = conexionBD()
        if conexion is None:
            return False
        
        cursor = conexion.cursor()
        # Actualizar el único registro existente
        sql = """
            UPDATE configuracion_empresa 
            SET nombre_empresa=%s, nit_rut=%s, direccion=%s, telefono=%s, slogan=%s, mensaje_final=%s
            WHERE id = (SELECT id FROM (SELECT id FROM configuracion_empresa LIMIT 1) as t)
        """
        cursor.execute(sql, (nombre, nit, direccion, telefono, slogan, mensaje))
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        print(f"Error al guardar configuracion: {e}")
        return False
