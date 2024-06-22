from tkinter import messagebox
from Conexion.Conexion import conexionBD

def obtener_Productos_combobox():
    try:
        connection = conexionBD()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT nombre FROM productostock WHERE estado = 1")    
            resultados = cursor.fetchall()
            connection.close()
            
            # Crear un diccionario con los nombres de los proveedores
            lista_proveedores = [row[0] for row in resultados]
            return lista_proveedores
        else:
            return []  # Devolver una lista vacía si no se puede conectar a la base de datos

    except Exception as e:
        print(f"Error al obtener proveedores: {e}")
        return []  # Manejar errores devolviendo una lista vacía


def listarStock():
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return []
    
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id, codigo, nombre, tipo, utilidad, iva, precioTotal, stock, precio_neto FROM productoStock WHERE estado = 1")  # Consulta para seleccionar todos los productos del stock
        productos = cursor.fetchall()  # Recupera todos los registros de la consulta
        
        return productos

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo listar los productos: {e}")
        return []

    finally:
        cursor.close()
        conexion.close()

def listarStockWhere(where):
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return []
    
    try:
        cursor = conexion.cursor()
        query = f"SELECT id, codigo, nombre, tipo, utilidad, iva, precioTotal, stock, precio_neto FROM productoStock WHERE estado = 1 AND {where}"
        cursor.execute(query)  # Ejecutar consulta
        productos = cursor.fetchall()  # Recupera todos los registros de la consulta
        
        return productos

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo listar los productos: {e}")
        return []

    finally:
        cursor.close()
        conexion.close()

def editarProStock(idStock, producto):
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return
    
    # SQL para actualizar en la tabla productoStock
    sql_productoStock = f"""UPDATE productoStock SET 
                            codigo = '{producto.codigo}', 
                            nombre = '{producto.nombre}', 
                            tipo = '{producto.tipo}', 
                            utilidad = {producto.utilidad}, 
                            iva = {producto.iva}, 
                            precioTotal = {producto.precioTotal},
                            precio_neto = {producto.precio_neto}
                            WHERE id = {idStock}"""
    
    try:
        cursor = conexion.cursor()
        cursor.execute(sql_productoStock)
        conexion.commit() # Asegurar que los cambios se guarden en la base de datos
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

def eliminarProStock(id_producto):
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return
    
    # SQL para actualizar el estado a 0 en la tabla productoStock
    sql_productoStock = f"UPDATE productoStock SET estado = 0 WHERE id = {id_producto}"
    
    try:
        cursor = conexion.cursor()
        cursor.execute(sql_productoStock)
        conexion.commit() # Asegurar que los cambios se guarden en la base de datos
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


def guardarProStock(producto):
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return
    
    # SQL para insertar en la tabla productoStock
    sql_productoStock = f"""INSERT INTO productoStock (codigo, nombre, tipo, utilidad, iva, precioTotal,stock, precio_neto, estado) VALUES
                            ('{producto.codigo}', 
                            '{producto.nombre}', 
                            '{producto.tipo}', 
                            {producto.utilidad}, 
                            {producto.iva}, 
                            {producto.precioTotal}, 
                            0.0,
                            {producto.precio_neto},
                            1)"""
    
    try:
        cursor = conexion.cursor()
        cursor.execute(sql_productoStock)
        conexion.commit() # Asegurar que los cambios se guarden en la base de datos
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


class ProductoStock():
    def __init__(self, codigo, nombre, tipo, utilidad, iva, precioTotal, precio_neto):
        self.codigo = codigo
        self.nombre = nombre
        self.tipo = tipo
        self.utilidad = utilidad
        self.iva = iva
        self.precioTotal = precioTotal
        self.precio_neto = precio_neto