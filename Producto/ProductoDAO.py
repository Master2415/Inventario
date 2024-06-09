from tkinter import messagebox
from Conexion.Conexion import conexionBD
from datetime import date

def guardarProducto(producto):
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return
    
    sql = f"""INSERT INTO producto (idProducto, tipoProducto, nombre, cantidadStock, precio, fechaIngreso) VALUES
            ({producto.idProducto}, '{producto.tipoProducto}', '{producto.nombre}', {producto.cantidadStock}, {producto.precio}, '{producto.fechaIngreso}')"""
    
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
        def __init__(self, idProducto, tipoProducto, nombre, cantidadStock, precio, fechaIngreso):
            self.idProducto = idProducto
            self.tipoProducto = tipoProducto
            self.nombre = nombre
            self.cantidadStock = cantidadStock
            self.precio = precio
            self.fechaIngreso = fechaIngreso
        
        def __str__(self):
            return (f"Producto [ID: {self.idProducto}, Tipo: {self.tipoProducto}, Nombre: {self.nombre}, "
                f"Stock: {self.cantidadStock}, Precio: {self.precio}, Fecha de Ingreso: {self.fechaIngreso}]")



# Comprobar inserccion 
"""if __name__ == "__main__":
    
    # Crear una instancia de Producto
    nuevo_producto = Producto(100122, 'Electrónica', 'Laptop', 10.0, 750.00, date.today())
    guardarProducto(nuevo_producto)"""
