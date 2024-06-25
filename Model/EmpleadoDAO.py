from tkinter import messagebox
from mysql.connector import Error
from Conexion.Conexion import conexionBD

def obtener_Cargos_combobox():
    try:
        connection = conexionBD()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT nombreRol FROM rol")    
            resultados = cursor.fetchall()
            connection.close()
            
            # Crear un diccionario con los nombres de los proveedores
            lista_roles = [row[0] for row in resultados]
            return lista_roles
        else:
            return []  # Devolver una lista vacía si no se puede conectar a la base de datos

    except Exception as e:
        print(f"Error al obtener Roles: {e}")
        return []  # Manejar errores devolviendo una lista vacía

def eliminarEmpleado(idEmpleado):
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return
    
    sql_empleado = f"""UPDATE empleado SET estado = 0 WHERE idEmpleado = {idEmpleado}"""
    sql_persona = f"""UPDATE persona SET Status = 0 WHERE id = (
                        SELECT idPersona FROM empleado WHERE idEmpleado = {idEmpleado})"""
    
    try:
        cursor = conexion.cursor()
        
        # Ejecutar la actualización en la tabla empleado
        cursor.execute(sql_empleado)
        
        # Ejecutar la actualización en la tabla persona
        cursor.execute(sql_persona)
        
        conexion.commit()  # Asegura que los cambios se guarden en la base de datos
        
        title = 'Eliminar Empleado'
        mensaje = 'Empleado Eliminado Exitosamente'
        messagebox.showinfo(title, mensaje)
    
    except Exception as e:
        title = 'Eliminar Empleado'
        mensaje = f'Error al Eliminar el Empleado: {e}'
        messagebox.showerror(title, mensaje)
    
    finally:
        cursor.close()
        conexion.close()

def editarEmpleado(empleado, idEmpleado, rol):
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return
    
    sql_persona = f"""UPDATE persona SET
                        cedula = '{empleado.cedula}',
                        nombre = '{empleado.nombre}',
                        apellido = '{empleado.apellido}',
                        direccion = '{empleado.direccion}',
                        correo = '{empleado.correo}',
                        telefono_numero = '{empleado.telefono_numero}',
                        ciudad = '{empleado.ciudad}',
                        Status = 1
                    WHERE id = (SELECT idPersona FROM empleado WHERE idEmpleado = {idEmpleado})"""
    
    # SQL para actualizar en la tabla Empleado
    sql_empleado = f"""UPDATE empleado SET
                        horasTrabajadas = {empleado.horas_trabajadas},
                        fechaContrato = '{empleado.fecha_contrato}',
                        Rol_idRol = (SELECT idrol FROM rol WHERE nombreRol = '{rol}'),
                        estado = 1
                    WHERE idEmpleado = {idEmpleado}"""
    
    try:
        cursor = conexion.cursor()
        cursor.execute(sql_persona)
        cursor.execute(sql_empleado)
        conexion.commit()
        messagebox.showinfo("Editar Empleado", "Empleado editado exitosamente")
    
    except Error as e:
        print(f"Error al editar empleado: {e}")
        messagebox.showerror("Error", f"Error al editar empleado: {e}")
    
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()


def guardarEmpleado(empleado, rol):
    try:
        conexion = conexionBD()
        if conexion is None:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            return
        
        cursor = conexion.cursor()

        # SQL para insertar en la tabla Persona
        sql_persona = f"""INSERT INTO persona (cedula, nombre, apellido, direccion, correo, telefono_numero, ciudad, Status)
                        VALUES (
                        '{empleado.cedula}', 
                        '{empleado.nombre}', 
                        '{empleado.apellido}', 
                        '{empleado.direccion}',
                        '{empleado.correo}', 
                        '{empleado.telefono_numero}', 
                        '{empleado.ciudad}', 
                        1)"""
        
        #print("SQL Persona:", sql_persona)  # Imprimir la consulta SQL para depuración
        cursor.execute(sql_persona)
        conexion.commit()  # Hacer commit para asegurarse de que el registro se ha insertado correctamente

        # Obtener el ID del último registro insertado en la tabla Persona
        last_id = cursor.lastrowid
        
        # Obtener el idRol correspondiente al nombre del rol
        cursor.execute(f"SELECT idRol FROM rol WHERE nombreRol = '{rol}'")
        rol_id = cursor.fetchone()[0]

        # Asegurarse de que los valores no estén vacíos
        horas_trabajadas = empleado.horas_trabajadas if empleado.horas_trabajadas else 0
        fecha_contrato = empleado.fecha_contrato if empleado.fecha_contrato else '0000-00-00'

        # SQL para insertar en la tabla Empleado utilizando el ID obtenido
        sql_empleado = f"""INSERT INTO empleado (idPersona, horasTrabajadas, fechaContrato, Rol_idRol, estado)
                        VALUES (
                        {last_id}, 
                        {horas_trabajadas}, 
                        '{fecha_contrato}', 
                        {rol_id}, 
                        1)"""
        
        #print("SQL Empleado:", sql_empleado)  # Imprimir la consulta SQL para depuración
        cursor.execute(sql_empleado)
        conexion.commit()
        messagebox.showinfo('Registrar Empleado', 'Empleado Registrado Exitosamente')
    
    except Exception as e:
        title = 'Registrar Empleado'
        mensaje = f'Error al Registrar el Empleado: {e}'
        messagebox.showinfo(title, mensaje)
    finally:
        cursor.close()
        conexion.close()


def listarEmpleado():
    try:
        conexion = conexionBD()
        if conexion is None:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            return []
        
        cursor = conexion.cursor()

        # Consulta SQL para listar empleados con información adicional
        sql = """
              SELECT e.idEmpleado, p.cedula, p.nombre, p.apellido, p.direccion, p.correo, p.telefono_numero,
                     p.ciudad, e.horasTrabajadas, e.fechaContrato, r.nombreRol
              FROM empleado e
              JOIN persona p ON e.idPersona = p.id
              JOIN rol r ON e.Rol_idRol = r.idRol
              WHERE e.estado = 1
              """
        
        cursor.execute(sql)
        empleados = cursor.fetchall()
        
        # Cerrar cursor y conexión
        cursor.close()
        conexion.close()
        
        return empleados
        
    except Exception as e:
        print(f"Error al listar empleados: {e}")
        messagebox.showerror("Error", "Error al listar empleados")
        return []
    
def listarEmpleadoWhere(where):
    try:
        conexion = conexionBD()
        if conexion is None:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            return []
        
        cursor = conexion.cursor()

        # Consulta SQL para listar empleados con información adicional y condición WHERE
        sql = f"""
              SELECT e.idEmpleado, p.cedula, p.nombre, p.apellido, p.direccion, p.correo, p.telefono_numero,
                     p.ciudad, e.horasTrabajadas, e.fechaContrato, r.nombreRol
              FROM empleado e
              JOIN persona p ON e.idPersona = p.id
              JOIN rol r ON e.Rol_idRol = r.idRol
              WHERE e.estado = 1 AND {where}
              """
        
        cursor.execute(sql)
        empleados = cursor.fetchall()
        
        # Cerrar cursor y conexión
        cursor.close()
        conexion.close()
        
        return empleados
        
    except Exception as e:
        print(f"Error al listar empleados con condición {where}: {e}")
        messagebox.showerror("Error", f"Error al listar empleados con condición {where}")
        return []


    
class Empleado:
    def __init__(self, cedula, nombre, apellido, direccion, correo, telefono_numero, ciudad, horas_trabajadas, fecha_contrato):
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.direccion = direccion
        self.correo = correo
        self.telefono_numero = telefono_numero
        self.ciudad = ciudad
        self.horas_trabajadas = horas_trabajadas
        self.fecha_contrato = fecha_contrato
       
