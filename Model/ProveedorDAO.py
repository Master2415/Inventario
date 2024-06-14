from tkinter import messagebox
from Conexion.Conexion import conexionBD

def eliminarProveedor(idProveedor):
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return
    
    sql = f"""UPDATE proveedor SET estado = 0 WHERE idProveedor = {idProveedor}"""
    
    try:
        cursor = conexion.cursor()
        cursor.execute(sql)  # Ejecuta la consulta SQL utilizando el cursor de la conexión
        conexion.commit()  # Asegura que los cambios se guarden en la base de datos
        title = 'Eliminar Proveedor'  
        mensaje = 'Proveedor Eliminado Exitosamente'  
        messagebox.showinfo(title, mensaje) 

    except Exception as e:
        title = 'Eliminar Proveedor'
        mensaje = f'Error al Eliminar el Proveedor: {e}'
        messagebox.showinfo(title, mensaje)
    
    finally:
        cursor.close()
        conexion.close()


def editarProveedor(Proveedor, idProveedor):
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return
    
    sql = f"""UPDATE proveedor SET 
             nombre = '{Proveedor.nombre}',
             tipo_proveedor = '{Proveedor.tipo_proveedor}',
             telefono = '{Proveedor.telefono}',
             direccion = '{Proveedor.direccion}',
             correo = '{Proveedor.correo}'
             WHERE idProveedor = {idProveedor}"""
    
    try:
        cursor = conexion.cursor()
        cursor.execute(sql)  # Ejecuta la consulta SQL utilizando el cursor de la conexión
        conexion.commit()  # Asegura que los cambios se guarden en la base de datos
        title = 'Editar Proveedor'  
        mensaje = 'Proveedor Editado Exitosamente'  
        messagebox.showinfo(title, mensaje) 

    except Exception as e:
        title = 'Editar Proveedor'
        mensaje = f'Error al Editar el Proveedor: {e}'
        messagebox.showinfo(title, mensaje)
    
    finally:
        cursor.close()
        conexion.close()


def agregarProveedor(Proveedor, Producto_id):
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return
    
    sql = f"""INSERT INTO proveedor (nombre, tipo_proveedor, telefono, direccion, correo, estado, Producto_id) VALUES
            ('{Proveedor.nombre}', '{Proveedor.tipo_proveedor}', '{Proveedor.telefono}', '{Proveedor.direccion}', '{Proveedor.correo}', 1, {Producto_id})"""
    
    try:
        cursor = conexion.cursor()
        cursor.execute(sql)  # Ejecuta la consulta SQL utilizando el cursor de la conexión
        conexion.commit()  # Asegura que los cambios se guarden en la base de datos
        title = 'Registrar Producto'  
        mensaje = 'Producto Registrado Exitosamente'  
        messagebox.showinfo(title, mensaje) 

    except Exception as e:
        title = 'Registrar Producto'
        mensaje = f'Error al Registrar el Producto: {e}'
        messagebox.showinfo(title, mensaje)
    
    finally:
        cursor.close()
        conexion.close()    


def listarProveedoresID(idProducto):
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return []
    
    try:
        cursor = conexion.cursor()
        query = """
        SELECT p.idProveedor, p.nombre, p.tipo_proveedor, p.telefono, p.direccion, p.correo
        FROM proveedor p 
        WHERE p.Producto_id = %s AND p.estado = 1   
        """
        cursor.execute(query, (idProducto,))
        proveedores = cursor.fetchall()  # Recupera todos los registros de la consulta
        
        return proveedores

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo listar los Proveedores: {e}")
        return []

    finally:
        cursor.close()
        conexion.close()

def listarProveedores():
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return []
    
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM proveedor WHERE estado = 1")  # Consulta para seleccionar todos los productos
        productos = cursor.fetchall()  # Recupera todos los registros de la consulta
        
        return productos

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo listar los Proveedores: {e}")
        return []

    finally:
        cursor.close()
        conexion.close()

class Proveedor():
    def __init__(self, nombre, tipo_proveedor, telefono, direccion, correo):
        self.idProveedor = None
        self.nombre = nombre
        self.tipo_proveedor = tipo_proveedor
        self.telefono = telefono
        self.direccion = direccion
        self.correo = correo
        #self.estado = estado
        #self.Producto_id = Producto_id