from tkinter import messagebox
from Conexion.Conexion import conexionBD

def editarCliente(cliente, idCliente):
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return
    
    sql = f""" consulta para editar """
    
    try:
        cursor = conexion.cursor()
        cursor.execute(sql)  # Ejecuta la consulta SQL utilizando el cursor de la conexión
        conexion.commit()  # Asegura que los cambios se guarden en la base de datos
        title = 'Editar Cliente'  
        mensaje = 'Cliente Editado Exitosamente'  
        messagebox.showinfo(title, mensaje) 

    except Exception as e:
        title = 'Editar Cliente'
        mensaje = f'Error al Editar el Cliente: {e}'
        messagebox.showinfo(title, mensaje)
    
    finally:
        cursor.close()
        conexion.close() 

def guardarCliente(cliente):
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return
    
    # SQL para insertar en la tabla Persona
    sql_persona = f"""INSERT INTO Persona (cedula, nombre, apellido, direccion, correo, Telefono_numero, Ciudad) VALUES
                    ({cliente.cedula}, '{cliente.nombre}', '{cliente.apellido}', '{cliente.direccion}', '{cliente.correo}', '{cliente.Telefono_numero}', '{cliente.Ciudad}', '1')"""
    
    try:
        cursor = conexion.cursor()
        cursor.execute(sql_persona)
        last_id = cursor.lastrowid # Obtener el ID del registro recién insertado en Persona
        # SQL para insertar en la tabla Cliente utilizando el ID obtenido
        sql_cliente = f"""INSERT INTO Cliente (id, tipo_cliente) VALUES
                        ({last_id}, '{cliente.tipo_cliente}')"""
        # Ejecutar la consulta SQL para insertar en Cliente
        cursor.execute(sql_cliente)
        # Asegurar que los cambios se guarden en la base de datos
        conexion.commit()
        title = 'Registrar Cliente'
        mensaje = 'Cliente Registrado Exitosamente'
        messagebox.showinfo(title, mensaje)
    except Exception as e:
        title = 'Registrar Cliente'
        mensaje = f'Error al Registrar el Cliente: {e}'
        messagebox.showinfo(title, mensaje)
    finally:
        cursor.close()
        conexion.close()


def listarCondicion(where):
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return []
    
    listarClientes = []
    sql = f'SELECT p.*, c.tipo_cliente FROM Persona p JOIN Cliente c ON p.id = c.id {where}'

    try:
        cursor = conexion.cursor()
        cursor.execute(sql)  
        listarClientes = cursor.fetchall()  # Obtener todos los resultados de la consulta
        conexion.commit()  

    except Exception as e:
        messagebox.showerror('Error', f'Error al listar Clientes: {e}')
    
    finally:
        cursor.close()
        conexion.close()

    return listarClientes  # Devolver los resultados de la consulta


def listarClientes():
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return []
    
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT p.*, c.tipo_cliente FROM Persona p JOIN Cliente c ON p.id = c.id")  # Consulta para seleccionar todos los productos
        productos = cursor.fetchall()  # Recupera todos los registros de la consulta
        
        return productos

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo listar los productos: {e}")
        return []

    finally:
        cursor.close()
        conexion.close()


class Cliente():
    def __init__(self, cedula, nombre, apellido, direccion, correo, telefono, ciudad, tipo):
        self.id = None
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.direccion = direccion
        self.correo = correo
        self.Telefono_numero = telefono
        self.ciudad = ciudad
        self.tipo = tipo