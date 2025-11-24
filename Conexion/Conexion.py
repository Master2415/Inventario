import os
import mysql.connector
from mysql.connector import Error

def conexionBD():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME', 'inventario'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', 'root')
        )

        if connection.is_connected():
            #print("Conexión a MySQL exitosa")
            return connection

    except Error as e:
        print("Error al conectar a MySQL", e)
        return None


