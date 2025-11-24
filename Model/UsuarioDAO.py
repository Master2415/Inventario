from tkinter import messagebox
from mysql.connector import Error
from Conexion.Conexion import conexionBD

def obtenerIdUsuario(correo):
    try:
        connection = conexionBD()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT idusuario FROM usuario WHERE correo = %s", (correo,))
            resultado = cursor.fetchone()
            connection.close()
            if resultado:
                return resultado[0]
            else:
                return None
        else:
            return None
    except Exception as e:
        print(f"Error al obtener ID usuario: {e}")
        return None

def obtener_Users_combobox():
    try:
        connection = conexionBD()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT correo FROM usuario where estado = 1")    
            resultados = cursor.fetchall()
            connection.close()
            
            lista_Users = [row[0] for row in resultados]
            return lista_Users
        else:
            return []  # Devolver una lista vacía si no se puede conectar a la base de datos

    except Exception as e:
        print(f"Error al obtener Roles: {e}")
        return []  # Manejar errores devolviendo una lista vacía

def obtener_empleados_para_combo():
    try:
        connection = conexionBD()
        if connection:
            cursor = connection.cursor()
            # Seleccionar id, nombre, apellido y cedula de empleados activos
            sql = """
                SELECT e.idEmpleado, p.nombre, p.apellido, p.cedula 
                FROM empleado e 
                JOIN persona p ON e.idPersona = p.id 
                WHERE e.estado = 1
            """
            cursor.execute(sql)
            resultados = cursor.fetchall()
            connection.close()
            return resultados # Retorna lista de tuplas (id, nombre, apellido, cedula)
        else:
            return []
    except Exception as e:
        print(f"Error al obtener empleados: {e}")
        return []

def eliminarUsuario(idUsuario):
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return
    
    # Consulta SQL para cambiar el estado del usuario a 0
    sql = f"""UPDATE usuario SET estado = 0 WHERE idusuario = {idUsuario}"""
    
    try:
        cursor = conexion.cursor()
        cursor.execute(sql)  # Ejecuta la consulta SQL utilizando el cursor de la conexión
        conexion.commit()  # Asegura que los cambios se guarden en la base de datos
        title = 'Eliminar Usuario'  
        mensaje = 'Usuario Eliminado Exitosamente'  
        messagebox.showinfo(title, mensaje) 

    except Exception as e:
        title = 'Eliminar Usuario'
        mensaje = f'Error al Eliminar el Usuario: {e}'
        messagebox.showinfo(title, mensaje)
    
    finally:
        cursor.close()
        conexion.close()

def listarUser():
    try:
        conexion = conexionBD()
        if conexion is None:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            return []
        
        cursor = conexion.cursor()

        # Consulta SQL para listar empleados con información adicional
        sql = """
              SELECT u.idusuario, u.correo, u.contrasena, p.nombre, p.apellido, p.cedula, r.nombreRol, e.idEmpleado
          FROM usuario u
          JOIN empleado e ON u.idEmpleado = e.idEmpleado
          JOIN persona p ON e.idPersona = p.id
          JOIN rol r ON e.Rol_idRol = r.idRol WHERE u.estado = 1
              """
        
        cursor.execute(sql)
        empleados = cursor.fetchall()
        
        # Cerrar cursor y conexión
        cursor.close()
        conexion.close()
        
        return empleados
        
    except Exception as e:
        print(f"Error al listar usuario: {e}")
        messagebox.showerror("Error", "Error al listar usuario")
        return []
    
def listarUserWhere(where):
    try:
        conexion = conexionBD()
        if conexion is None:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            return []
        
        cursor = conexion.cursor()

        # Consulta SQL para listar empleados con información adicional y condición WHERE
        sql = f"""
              SELECT idusuario, correo, contrasena from usuario {where}
              """
        
        cursor.execute(sql)
        empleados = cursor.fetchall()
        
        # Cerrar cursor y conexión
        cursor.close()
        conexion.close()
        
        return empleados
        
    except Exception as e:
        print(f"Error al listar usuario con condición {where}: {e}")
        messagebox.showerror("Error", f"Error al listar usuario con condición {where}")
        return []

def editarUsuario(idUsuario, usuario, idEmpleado):
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return
    
    try:
        cursor = conexion.cursor()
        
        sql = f"""UPDATE usuario SET 
                    correo = '{usuario.correo}',
                    contrasena = '{usuario.contrasena}',
                    idEmpleado = {idEmpleado}
                    WHERE idusuario = {idUsuario}"""
        cursor.execute(sql)
        conexion.commit()
        messagebox.showinfo('Editar usuario', 'Usuario editado exitosamente')
    
    except Exception as e:
        messagebox.showerror('Editar usuario', f'Error al editar el usuario: {e}')
    
    finally:
        cursor.close()
        conexion.close()

def guardarUsuario(usuario, idEmpleado):
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return
    
    try:
        cursor = conexion.cursor()

        # Verificar si el correo ya existe
        cursor.execute("SELECT COUNT(*) FROM usuario WHERE correo = %s", (usuario.correo,))
        correo_result = cursor.fetchone()
        
        if correo_result[0] > 0:
            messagebox.showwarning('Registrar el usuario', 'El correo proporcionado ya está registrado')
        else:
            # Insertar el nuevo usuario
            cursor.execute("""
                INSERT INTO usuario (correo, contrasena, estado, idEmpleado)
                VALUES (%s, %s, %s, %s)
            """, (usuario.correo, usuario.contrasena, 1, idEmpleado))
            
            conexion.commit()  # Asegura que los cambios se guarden en la base de datos
            messagebox.showinfo('Registrar el usuario', 'Usuario registrado exitosamente')
    
    except Exception as e:
        messagebox.showerror('Registrar el usuario', f'Error al registrar el usuario: {e}')
    
    finally:
        cursor.close()
        conexion.close()



class Usuario:
    def __init__(self, correo, contrasena):
        self.correo = correo
        self.contrasena = contrasena