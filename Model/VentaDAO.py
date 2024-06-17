from tkinter import messagebox
from Conexion.Conexion import conexionBD

def guardarVenta(venta):
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return
    
    sql = f"""INSERT INTO venta(total, fecha, usuario_id, cliente_id) VALUES
            ({venta.total}, '{venta.fecha}', {venta.usuario_id}, {venta.cliente_id}) """

    try:
        cursor = conexion.cursor()
        cursor.execute(sql)  # Ejecuta la consulta SQL utilizando el cursor de la conexión
        conexion.commit()  # Asegura que los cambios se guarden en la base de datos
        title = 'Registrar Venta'  
        mensaje = 'Venta Registrado Exitosamente'  
        #messagebox.showinfo(title, mensaje) 

    except Exception as e:
        title = 'Registrar Venta'
        mensaje = f'Error al Registrar el Venta: {e}'
        messagebox.showinfo(title, mensaje)
    
    
    finally:
        cursor.close()
        conexion.close() 


def listarVentas():
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return []
    
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM venta") 
        ventas = cursor.fetchall() 
        
        return ventas

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo listar las Ventas: {e}")
        return []

    finally:
        cursor.close()
        conexion.close()

class Venta:
    def __init__(self, total, fecha, usuario_id, cliente_id):
        self.idVenta = None
        self.total = total
        self.fecha = fecha
        self.usuario_id = usuario_id
        self.cliente_id = cliente_id

