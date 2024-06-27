from tkinter import messagebox
from Conexion.Conexion import conexionBD

def editarCaja(caja, idcaja, nombreUsuario):
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return
    
    montoApertura = str(caja.montoApertura).replace(',', '')
    montoFin = str(caja.montoFin).replace(',', '')
    
    sql = f"""
            UPDATE caja SET 
                horaInicio = '{caja.horaInicio}', 
                horaFin = '{caja.horaFin}', 
                montoApertura = {montoApertura}, 
                montoFin = {montoFin},
                estado = 1,
                idUser = (SELECT idusuario FROM usuario WHERE correo = '{nombreUsuario}')
            WHERE idProducto = {idcaja}
            """
    
    try:
        cursor = conexion.cursor()
        cursor.execute(sql)
        conexion.commit()
        title = 'Editar Caja'
        mensaje = 'Caja Editado Exitosamente'
        messagebox.showinfo(title, mensaje)
    
    except Exception as e:
        title = 'Editar Caja'
        mensaje = f'Error al Editar la Caja: {e}'
        messagebox.showerror(title, mensaje)
    
    finally:
        cursor.close()
        conexion.close()

def agregar(caja, nombreUsuario):
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return
    
    montoApertura = str(caja.montoApertura).replace(',', '')
    montoFin = str(caja.montoFin).replace(',', '')
    
    sql = f"""INSERT INTO caja 
            (horaInicio, horaFin, montoApertura, montoFin, estado, idUser) VALUES
            ('{caja.horaInicio}', 
            '{caja.horaFin}', 
            {montoApertura}, 
            {montoFin}, 1,  
            (SELECT idusuario FROM usuario WHERE correo = '{nombreUsuario}'))"""
    
    try:
        cursor = conexion.cursor()
        cursor.execute(sql)
        conexion.commit()
        title = 'Registro de caja'
        mensaje = 'Registro Exitoso'
        messagebox.showinfo(title, mensaje)
    
    except Exception as e:
        title = 'Registro de caja'
        mensaje = f'Error al Registrar la caja: {e}'
        messagebox.showerror(title, mensaje)
    
    finally:
        cursor.close()
        conexion.close()

def listarCaja():
    conexion = conexionBD()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return []
    
    try:
        cursor = conexion.cursor()
        cursor.execute("""SELECT c.idCaja, c.horaInicio, c.horaFin, c.montoApertura, c.montoFin, u.correo 
                       FROM caja c 
                       JOIN usuario u on c.idcaja = u.idusuario
                       WHERE c.estado = 1 """)  # Consulta para seleccionar todos los productos
        productos = cursor.fetchall()  # Recupera todos los registros de la consulta
        
        return productos

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo listar los productos: {e}")
        return []

    finally:
        cursor.close()
        conexion.close
    


class Caja:
    def __init__(self, horaInicio, horaFin, montoApertura, montoFin):
        self.horaInicio = horaInicio
        self.horaFin = horaFin
        self.montoApertura = montoApertura
        self.montoFin = montoFin

