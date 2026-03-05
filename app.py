from flask import Flask, render_template, request, redirect, url_for
import os
from models import GestionSalud # Importamos la clase desde tu archivo models.py

app = Flask(__name__)
db = GestionSalud() # Instanciamos la gestión de base de datos

# 1. RUTA PRINCIPAL
@app.route('/')
def home():
    return render_template('index.html')

# 2. RUTA ACERCA DE
@app.route('/about')
def about():
    return render_template('about.html')

# 3. RUTA DE SERVICIOS (Muestra la lista de la DB)
@app.route('/servicios')
def servicios():
    # Obtenemos la colección (lista de diccionarios) desde SQLite
    lista_servicios = db.obtener_todos()
    return render_template('productos.html', servicios=lista_servicios)

# 4. RUTA PARA AGREGAR (Procesa el formulario POST)
@app.route('/agregar_servicio', methods=['POST'])
def agregar():
    nombre = request.form['nombre']
    especialidad = request.form['especialidad']
    costo = request.form['costo']
    
    # Llamamos al método de la clase GestionSalud para guardar en SQLite
    db.agregar_servicio(nombre, especialidad, costo)
    return redirect(url_for('servicios'))

# 5. RUTA PARA ELIMINAR (Usa el ID único del servicio)
@app.route('/eliminar/<int:id>')
def eliminar(id):
    db.eliminar_servicio(id)
    return redirect(url_for('servicios'))

# Arrancador de la aplicación
if __name__ == '__main__':
    app.run(debug=True)
