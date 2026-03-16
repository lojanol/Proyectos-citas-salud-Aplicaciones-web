import mysql.connector

def obtener_conexion():
    try:
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='clinica_lojano' # Asegúrate que se llame así en XAMPP
        )
    except mysql.connector.Error as err:
        print(f"Error de conexión: {err}")
        return None