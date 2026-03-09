from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import json
import csv

app = Flask(__name__)

# --- 1. CONFIGURACIÓN DE SQLALCHEMY (Punto 2.3) ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clinica.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- 2. MODELO DE DATOS (Punto 2.4) ---
class Servicio(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Clave primaria
    nombre = db.Column(db.String(100), nullable=False)
    especialidad = db.Column(db.String(100), nullable=False)
    costo = db.Column(db.Float, nullable=False)

# Crear la base de datos automáticamente
with app.app_context():
    db.create_all()

# --- 3. RUTAS DE NAVEGACIÓN ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/servicios')
def servicios():
    # Lee todos los registros usando el ORM
    lista_servicios = Servicio.query.all()
    return render_template('productos.html', servicios=lista_servicios)

# --- 4. RUTA DE PERSISTENCIA MÚLTIPLE (Punto 2.2) ---
@app.route('/agregar_servicio', methods=['POST'])
def agregar():
    nombre = request.form['nombre']
    especialidad = request.form['especialidad']
    costo = request.form['costo']
    
    # A. Guardar en SQLite con SQLAlchemy
    nuevo = Servicio(nombre=nombre, especialidad=especialidad, costo=float(costo))
    db.session.add(nuevo)
    db.session.commit()

    # Preparar datos para archivos planos
    datos_dict = {"nombre": nombre, "especialidad": especialidad, "costo": costo}

    # B. Persistencia en TXT (Modo append)
    with open("data/datos.txt", "a") as f:
        f.write(f"{nombre}, {especialidad}, {costo}\n")

    # C. Persistencia en JSON
    lista_json = []
    if os.path.exists("data/datos.json") and os.path.getsize("data/datos.json") > 0:
        with open("data/datos.json", "r") as f:
            lista_json = json.load(f)
    lista_json.append(datos_dict)
    with open("data/datos.json", "w") as f:
        json.dump(lista_json, f, indent=4)

    # D. Persistencia en CSV
    with open("data/datos.csv", "a", newline='') as f:
        escritor = csv.DictWriter(f, fieldnames=["nombre", "especialidad", "costo"])
        if f.tell() == 0: 
            escritor.writeheader()
        escritor.writerow(datos_dict)

    return redirect(url_for('servicios'))

# --- 5. RUTA PARA LEER ARCHIVOS (Punto 2.2) ---
@app.route('/datos_archivos')
def datos_archivos():
    servicios_archivo = []
    if os.path.exists("data/datos.json"):
        with open("data/datos.json", "r") as f:
            servicios_archivo = json.load(f)
    return render_template('datos.html', servicios=servicios_archivo)

# --- 6. EJECUCIÓN DEL SERVIDOR ---
if __name__ == '__main__':
    app.run(debug=True)