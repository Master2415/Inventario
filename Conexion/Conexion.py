import mysql.connector
from mysql.connector import Error

def conexionBD():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='inventario',
            user='root',
            password='root'
        )

        if connection.is_connected():
            #print("Conexión a MySQL exitosa")
            return connection

    except Error as e:
        print("Error al conectar a MySQL", e)
        return None


