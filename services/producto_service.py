from Conexion.conexion import obtener_conexion

class ProductoService:
    @staticmethod
    def listar_todos():
        db = obtener_conexion()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM servicios")
        datos = cursor.fetchall()
        cursor.close()
        db.close()
        return datos

    @staticmethod
    def insertar(nombre, precio, stock):
        db = obtener_conexion()
        cursor = db.cursor()
        sql = "INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s)"
        cursor.execute(sql, (nombre, precio, stock))
        db.commit()
        db.close()

        @staticmethod
        def eliminar(id_producto):
         db = obtener_conexion()
        cursor = db.cursor()
        cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id_producto,))
        db.commit()
        db.close()

    @staticmethod
    def obtener_por_id(id_producto):
        db = obtener_conexion()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id_producto,))
        dato = cursor.fetchone()
        cursor.close()
        db.close()
        return dato

    @staticmethod
    def actualizar(id_producto, nombre, precio, stock):
        db = obtener_conexion()
        cursor = db.cursor()
        sql = "UPDATE productos SET nombre=%s, precio=%s, stock=%s WHERE id_producto=%s"
        cursor.execute(sql, (nombre, precio, stock, id_producto))
        db.commit()
        db.close()