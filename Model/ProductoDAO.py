from tkinter import messagebox
from Conexion.Conexion import conexionBD

def obtener_id_por_producto(codigo):
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return None
    
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id FROM productoStock WHERE codigo = %s", (codigo,))
        print("busco el codigo")
        resultado = cursor.fetchone()
        if resultado:
            return resultado[0]
        else:
            return None
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo obtener el ID: {e}")
        return None
    finally:
        cursor.close()
        conexion.close()

def actualizar_stock_db(idProducto, cantidad):
    connection = conexionBD()
    if connection:
        cursor = connection.cursor()
        cursor.execute("UPDATE productoStock SET stock = stock + %s WHERE id = %s", (cantidad, idProducto))
        connection.commit()
        connection.close()
        print("Stock actualizado en la base de datos")

def listarCondiciones(where):
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return []
    
    listarProductos = []
    sql = f"""SELECT 
                p.idProducto, 
                p.codigo, 
                ps.nombre AS nombre_productostock, 
                ps.tipo AS tipo_productostock, 
                p.cantidadStock, 
                p.precio, 
                p.fechaIngreso, 
                prov.nombre AS nombre_proveedor
            FROM 
                Producto p
                LEFT JOIN productostock ps ON p.idProductoStock = ps.id
                LEFT JOIN proveedor prov ON p.idProveedor = prov.idProveedor
            {where}"""

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


def listarProductos():
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return []
    
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT 
                p.idProducto, 
                p.codigo, 
                ps.nombre AS nombre_productostock, 
                ps.tipo AS tipo_productostock, 
                p.cantidadStock, 
                p.precio, 
                p.fechaIngreso, 
                prov.nombre AS nombre_proveedor
            FROM 
                Producto p
                LEFT JOIN productostock ps ON p.idProductoStock = ps.id
                LEFT JOIN proveedor prov ON p.idProveedor = prov.idProveedor
        """)  # Consulta para seleccionar todos los productos con información extendida
        productos = cursor.fetchall()  # Recupera todos los registros de la consulta
        
        return productos

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo listar los productos: {e}")
        return []

    finally:
        cursor.close()
        conexion.close()


def listarCondicionesTabla_Productos(where):
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return []
    
    listarProductos = []
    sql = f'SELECT codigo, nombre, precioTotal, stock FROM productostock {where}'

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


def listarProductos_En_Venta():
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return []
    
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT codigo, nombre, precioTotal, stock FROM productostock")  # Consulta para seleccionar todos los productos
        productos = cursor.fetchall()  # Recupera todos los registros de la consulta
        
        return productos

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo listar los productos: {e}")
        return []

    finally:
        cursor.close()
        conexion.close()


def editarProducto(producto, idProducto, nombreProveedor):
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return
    
    sql = f"""UPDATE Producto SET 
                codigo = '{producto.codigo}', 
                tipoProducto = '{producto.tipoProducto}', 
                nombre = '{producto.nombre}', 
                cantidadStock = {producto.cantidadStock}, 
                precio = {producto.precio}, 
                fechaIngreso = '{producto.fechaIngreso}',
                idProductoStock = (SELECT id FROM productostock WHERE codigo= '{producto.codigo}'),
                idProveedor = (SELECT idProveedor FROM Proveedor WHERE nombre = '{nombreProveedor}')
            WHERE idProducto = {idProducto}"""
    
    try:
        cursor = conexion.cursor()
        cursor.execute(sql)
        conexion.commit()
        title = 'Editar Producto'
        mensaje = 'Producto Editado Exitosamente'
        messagebox.showinfo(title, mensaje)
    
    except Exception as e:
        title = 'Editar Producto'
        mensaje = f'Error al Editar el Producto: {e}'
        messagebox.showerror(title, mensaje)
    
    finally:
        cursor.close()
        conexion.close()



def guardarProducto(producto, nombreProveedor):
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return
    
    sql = f"""INSERT INTO Producto (codigo, tipoProducto, nombre, cantidadStock, precio, fechaIngreso, idProductoStock, idProveedor) VALUES
            ('{producto.codigo}', '{producto.tipoProducto}', '{producto.nombre}', {producto.cantidadStock}, {producto.precio}, '{producto.fechaIngreso}', 
            (SELECT id FROM productostock WHERE codigo= '{producto.codigo}'),
            (SELECT idProveedor FROM Proveedor WHERE nombre = '{nombreProveedor}'))"""
    
    try:
        cursor = conexion.cursor()
        cursor.execute(sql)
        conexion.commit()
        title = 'Registrar Producto'
        mensaje = 'Producto Registrado Exitosamente'
        messagebox.showinfo(title, mensaje)
    
    except Exception as e:
        title = 'Registrar Producto'
        mensaje = f'Error al Registrar el Producto: {e}'
        messagebox.showerror(title, mensaje)
    
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


