from Conexion.Conexion import conexionBD
from tkinter import messagebox
import datetime

def crear_tabla_nomina():
    try:
        conexion = conexionBD()
        if conexion is None:
            return
        
        cursor = conexion.cursor()
        sql = """
            CREATE TABLE IF NOT EXISTS pago_nomina (
                id INT AUTO_INCREMENT PRIMARY KEY,
                id_empleado INT NOT NULL,
                monto DECIMAL(10, 2) NOT NULL,
                fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
                tipo_pago VARCHAR(20) NOT NULL, -- 'HORA' o 'FIJO'
                horas_pagadas DECIMAL(10, 2) DEFAULT 0,
                FOREIGN KEY (id_empleado) REFERENCES empleado(idEmpleado)
            )
        """
        cursor.execute(sql)
        conexion.commit()
        conexion.close()
    except Exception as e:
        print(f"Error al crear tabla nomina: {e}")

def obtener_empleados_para_nomina():
    try:
        conexion = conexionBD()
        if conexion is None:
            return []
        
        cursor = conexion.cursor()
        sql = """
            SELECT e.idEmpleado, CONCAT(p.nombre, ' ', p.apellido) as nombre_completo, e.horasTrabajadas
            FROM empleado e
            JOIN persona p ON e.idPersona = p.id
            WHERE e.estado = 1
        """
        cursor.execute(sql)
        resultados = cursor.fetchall()
        conexion.close()
        return resultados
    except Exception as e:
        print(f"Error al obtener empleados: {e}")
        return []

def registrar_pago(id_empleado, monto, tipo_pago, horas_pagadas=0):
    try:
        conexion = conexionBD()
        if conexion is None:
            return False
        
        cursor = conexion.cursor()
        fecha_actual = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        sql = """
            INSERT INTO pago_nomina (id_empleado, monto, fecha, tipo_pago, horas_pagadas)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (id_empleado, monto, fecha_actual, tipo_pago, horas_pagadas))
        
        # Si es pago por hora, resetear las horas del empleado
        if tipo_pago == 'HORA':
            sql_update = "UPDATE empleado SET horasTrabajadas = 0 WHERE idEmpleado = %s"
            cursor.execute(sql_update, (id_empleado,))
            
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        print(f"Error al registrar pago: {e}")
        return False

def calcular_nomina_rango(fecha_inicio, fecha_fin):
    try:
        conexion = conexionBD()
        if conexion is None:
            return 0.0
        
        cursor = conexion.cursor()
        # Asegurarse de incluir todo el día final
        fecha_fin_inclusive = f"{fecha_fin} 23:59:59"
        
        sql = """
            SELECT SUM(monto) 
            FROM pago_nomina 
            WHERE fecha BETWEEN %s AND %s
        """
        cursor.execute(sql, (fecha_inicio, fecha_fin_inclusive))
        resultado = cursor.fetchone()
        conexion.close()
        
        return resultado[0] if resultado and resultado[0] else 0.0
    except Exception as e:
        # Si la tabla no existe (primera ejecución antes de crearla), retornar 0
        print(f"Error al calcular nomina rango: {e}")
        return 0.0
