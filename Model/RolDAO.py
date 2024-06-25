from tkinter import messagebox
from Conexion.Conexion import conexionBD


def eliminarRol(idRol):
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return
    
    sql = f"""DELETE FROM rol WHERE idRol = {idRol}"""
    
    try:
        cursor = conexion.cursor()
        cursor.execute(sql)  # Ejecuta la consulta SQL utilizando el cursor de la conexión
        conexion.commit()  # Asegura que los cambios se guarden en la base de datos
        title = 'Eliminar Rol'  
        mensaje = 'Rol Eliminado Exitosamente'  
        messagebox.showinfo(title, mensaje) 

    except Exception as e:
        title = 'Eliminar Rol'
        mensaje = f'Error al Eliminar el Rol: {e}'
        messagebox.showinfo(title, mensaje)
    
    finally:
        cursor.close()
        conexion.close()

def editarRol(rol, idRol):
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return

    sql = f"""UPDATE rol SET 
         nombreRol = '{rol.nombreRol}',
         salario = '{rol.salario}'
         WHERE idRol = {idRol}"""
    
    try:
        cursor = conexion.cursor()
        cursor.execute(sql)  # Ejecuta la consulta SQL utilizando el cursor de la conexión
        conexion.commit()  # Asegura que los cambios se guarden en la base de datos
        title = 'Editar Rol'  
        mensaje = 'Rol Editado Exitosamente'  
        messagebox.showinfo(title, mensaje) 

    except Exception as e:
        title = 'Editar Rol'
        mensaje = f'Error al Editar el Rol: {e}'
        messagebox.showinfo(title, mensaje)
    
    finally:
        cursor.close()
        conexion.close()

def guardarRol(rol):
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return
    
    sql = f"""INSERT INTO rol (nombrerol, salario) VALUES
            ('{rol.nombreRol}', 
            '{rol.salario}')"""
    
    try:
        cursor = conexion.cursor()
        cursor.execute(sql)  # Ejecuta la consulta SQL utilizando el cursor de la conexión
        conexion.commit()  # Asegura que los cambios se guarden en la base de datos
        title = 'Registrar el Rol'  
        mensaje = 'Rol Registrado Exitosamente'  
        messagebox.showinfo(title, mensaje) 

    except Exception as e:
        title = 'Registrar el Rol'
        mensaje = f'Error al Registrar el Rol: {e}'
        messagebox.showinfo(title, mensaje)
    
    finally:
        cursor.close()
        conexion.close() 

def listarRol():
    try:
        conexion = conexionBD()
        if conexion is None:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            return []
        
        cursor = conexion.cursor()

        # Consulta SQL para listar empleados con información adicional
        sql = """
              SELECT * from rol
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
    
def listarRolWhere(where):
    try:
        conexion = conexionBD()
        if conexion is None:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            return []
        
        cursor = conexion.cursor()

        # Consulta SQL para listar empleados con información adicional y condición WHERE
        sql = f"""
              SELECT * from rol {where}
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


class Rol():
    def __init__(self, nombreRol, salario):
        self.nombreRol = nombreRol
        self.salario = salario
