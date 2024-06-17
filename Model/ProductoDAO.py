from tkinter import messagebox
from Conexion.Conexion import conexionBD


def actualizar_stock_db(codigo, cantidad):
    connection = conexionBD()
    if connection:
        cursor = connection.cursor()
        cursor.execute("UPDATE producto SET cantidadStock = cantidadStock + %s WHERE codigo = %s", (cantidad, codigo))
        connection.commit()
        connection.close()
        #print("Stock actualizado en la base de datos")

def listarCondiciones(where):
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return []
    
    listarProductos = []
    sql = f'SELECT * FROM Producto {where}'

    try:
        cursor = conexion.cursor()
        cursor.execute(sql)  
        listarProductos = cursor.fetchall()  # Obtener todos los resultados de la consulta
        conexion.commit()  

    except Exception as e:
        messagebox.showerror('Error', f'Error al listar productos: {e}')
    
    finally:
        cursor.close()
        conexion.close()

    return listarProductos  # Devolver los resultados de la consulta

def listarCondiciones1(where):
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return []
    
    listarProductos = []
    sql = f'SELECT codigo, nombre, precio, cantidadStock FROM Producto {where}'

    try:
        cursor = conexion.cursor()
        cursor.execute(sql)  
        listarProductos = cursor.fetchall()  # Obtener todos los resultados de la consulta
        conexion.commit()  

    except Exception as e:
        messagebox.showerror('Error', f'Error al listar productos: {e}')
    
    finally:
        cursor.close()
        conexion.close()

    return listarProductos  # Devolver los resultados de la consulta

def eliminarProducto(idProducto):
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return
    sql = f"""DELETE FROM Producto WHERE idProducto = {idProducto}"""
    try:
        cursor = conexion.cursor()
        cursor.execute(sql)  # Ejecuta la consulta SQL utilizando el cursor de la conexión
        conexion.commit()  # Asegura que los cambios se guarden en la base de datos
        title = 'Eliminar Producto'  
        mensaje = 'Producto Eliminado Exitosamente'  
        messagebox.showinfo(title, mensaje) 

    except Exception as e:
        title = 'Eliminar Producto'
        mensaje = f'Error al Eliminar el Producto: {e}'
        messagebox.showinfo(title, mensaje)
    
    finally:
        cursor.close()
        conexion.close()

def editarProducto(producto, idProducto):
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return
    
    sql = f"""UPDATE Producto SET  codigo = '{producto.codigo}', tipoProducto = '{producto.tipoProducto}', nombre = '{producto.nombre}', cantidadStock = {producto.cantidadStock}, 
            precio = {producto.precio}, fechaIngreso = '{producto.fechaIngreso}' WHERE idProducto = {idProducto}"""
    
    try:
        cursor = conexion.cursor()
        cursor.execute(sql)  # Ejecuta la consulta SQL utilizando el cursor de la conexión
        conexion.commit()  # Asegura que los cambios se guarden en la base de datos
        title = 'Editar Producto'  
        mensaje = 'Producto Editado Exitosamente'  
        messagebox.showinfo(title, mensaje) 

    except Exception as e:
        title = 'Editar Producto'
        mensaje = f'Error al Editar el Producto: {e}'
        messagebox.showinfo(title, mensaje)
    
    finally:
        cursor.close()
        conexion.close() 

def listarProductos():
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return []
    
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM producto")  # Consulta para seleccionar todos los productos
        productos = cursor.fetchall()  # Recupera todos los registros de la consulta
        
        return productos

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo listar los productos: {e}")
        return []

    finally:
        cursor.close()
        conexion.close()

def listarProductos1():
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return []
    
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT codigo, nombre, precio, cantidadStock FROM producto")  # Consulta para seleccionar todos los productos
        productos = cursor.fetchall()  # Recupera todos los registros de la consulta
        
        return productos

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo listar los productos: {e}")
        return []

    finally:
        cursor.close()
        conexion.close()

def guardarProducto(producto):
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return
    
    sql = f"""INSERT INTO producto (codigo, tipoProducto, nombre, cantidadStock, precio, fechaIngreso) VALUES
            ({producto.codigo}, '{producto.tipoProducto}', '{producto.nombre}', {producto.cantidadStock}, {producto.precio}, '{producto.fechaIngreso}')"""
    
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


class Producto:
        def __init__(self, codigo, tipoProducto, nombre, cantidadStock, precio, fechaIngreso):
            self.idProducto = None
            self.codigo = codigo
            self.tipoProducto = tipoProducto
            self.nombre = nombre
            self.cantidadStock = cantidadStock
            self.precio = precio
            self.fechaIngreso = fechaIngreso
        
        def __str__(self):
            return (f"Producto [ID: {self.idProducto}, Tipo: {self.tipoProducto}, Nombre: {self.nombre}, "
                f"Stock: {self.cantidadStock}, Precio: {self.precio}, Fecha de Ingreso: {self.fechaIngreso}]")


