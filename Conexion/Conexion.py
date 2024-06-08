import mysql.connector
from mysql.connector import Error


try:
    connection = mysql.connector.connect(
        host='localhost',      
        database='expendio',
        user='root',
        password='root'
    )

    if connection.is_connected():
        print("Conexión a MySQL exitosa")
        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE();")
        record = cursor.fetchone()
        print("Conectado a la base de datos:", record)

except Error as e:
    print("Error al conectar a MySQL", e)

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("Conexión a MySQL cerrada")

