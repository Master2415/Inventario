from tkinter import messagebox
from mysql.connector import Error
from Conexion.Conexion import conexionBD

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
              SELECT u.idusuario, u.correo, u.contrasena, p.nombre, p.apellido, p.cedula, r.nombreRol
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

def editarUsuario(idUsuario, usuario, cedula):
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return
    
    try:
        cursor = conexion.cursor()

        # Verificar si la cédula existe en la tabla persona
        cursor.execute("SELECT id FROM persona WHERE cedula = %s", (cedula,))
        persona_result = cursor.fetchone()
        
        if persona_result:
            idPersona = persona_result[0]
            
            # Verificar si el idPersona tiene un empleado asociado en la tabla empleado
            cursor.execute("SELECT idEmpleado FROM empleado WHERE idPersona = %s", (idPersona,))
            empleado_result = cursor.fetchone()
            
            if empleado_result:
                idEmpleado = empleado_result[0]
                sql = f"""UPDATE usuario SET 
                         correo = '{usuario.correo}',
                         contrasena = '{usuario.contrasena}',
                         idEmpleado = {idEmpleado}
                         WHERE idusuario = {idUsuario}"""
                cursor.execute(sql)  # Ejecuta la consulta SQL utilizando el cursor de la conexión
                conexion.commit()  # Asegura que los cambios se guarden en la base de datos
                messagebox.showinfo('Editar usuario', 'Usuario editado exitosamente')
            else:
                messagebox.showwarning('Editar usuario', 'No se encontró un empleado asociado con la cédula proporcionada')
        else:
            messagebox.showwarning('Editar usuario', 'No se encontró una persona con la cédula proporcionada')
    
    except Exception as e:
        messagebox.showerror('Editar usuario', f'Error al editar el usuario: {e}')
    
    finally:
        cursor.close()
        conexion.close()

def guardarUsuario(usuario, cedula):
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return
    
    try:
        cursor = conexion.cursor()

        # Comprobar si existe un idPersona con la cedula dada
        cursor.execute("SELECT id FROM persona WHERE cedula = %s", (cedula,))
        persona_result = cursor.fetchone()
        
        if persona_result:
            idPersona = persona_result[0]
            
            # Verificar si el idPersona tiene un empleado asociado en la tabla empleado
            cursor.execute("SELECT idEmpleado FROM empleado WHERE idPersona = %s", (idPersona,))
            empleado_result = cursor.fetchone()
            
            if empleado_result:
                idEmpleado = empleado_result[0]
                
                # Insertar el nuevo usuario
                cursor.execute("""
                    INSERT INTO usuario (correo, contrasena, estado, idEmpleado)
                    VALUES (%s, %s, %s, %s)
                """, (usuario.correo, usuario.contrasena, 1, idEmpleado))
                
                conexion.commit()  # Asegura que los cambios se guarden en la base de datos
                messagebox.showinfo('Registrar el usuario', 'Usuario registrado exitosamente')
            else:
                messagebox.showwarning('Registrar el usuario', 'No se encontró un empleado asociado con la cédula proporcionada')
        else:
            messagebox.showwarning('Registrar el usuario', 'No se encontró una persona con la cédula proporcionada')
    
    except Exception as e:
        messagebox.showerror('Registrar el usuario', f'Error al registrar el usuario: {e}')
    
    finally:
        cursor.close()
        conexion.close()


class Usuario:
    def __init__(self, correo, contrasena):
        self.correo = correo
        self.contrasena = contrasena