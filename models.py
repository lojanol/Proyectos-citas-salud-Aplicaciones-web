import sqlite3

# Clase Producto (en tu caso, Servicio de Salud)
class Servicio:
    def __init__(self, id, nombre, especialidad, costo):
        self.id = id
        self.nombre = nombre
        self.especialidad = especialidad
        self.costo = costo

# Clase Inventario (Gestión de la DB y Colecciones)
class GestionSalud:
    def __init__(self, db_name='citas_salud.db'):
        self.db_name = db_name
        self.crear_tabla()

    def conectar(self):
        return sqlite3.connect(self.db_name)

    def crear_tabla(self):
        with self.conectar() as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS servicios 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             nombre TEXT NOT NULL, 
                             especialidad TEXT, 
                             costo REAL)''')

    def agregar_servicio(self, nombre, especialidad, costo):
        with self.conectar() as conn:
            conn.execute("INSERT INTO servicios (nombre, especialidad, costo) VALUES (?, ?, ?)",
                         (nombre, especialidad, costo))

    def obtener_todos(self):
        with self.conectar() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM servicios")
            # Uso de Colección: Lista de diccionarios
            return [dict(fila) for fila in cursor.fetchall()]

    def eliminar_servicio(self, id_servicio):
        with self.conectar() as conn:
            conn.execute("DELETE FROM servicios WHERE id = ?", (id_servicio,))