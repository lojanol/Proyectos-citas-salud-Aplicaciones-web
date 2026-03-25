from flask import Flask, render_template, request, redirect, url_for, flash
from Conexion.conexion import obtener_conexion
from models import Usuario  # <--- Esto conecta con tu archivo models.py
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

app.secret_key = 'tu_clave_secreta_aqui' # Necesario para sesiones

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    db = obtener_conexion()
    if db:
     cursor = db.cursor(dictionary=True)
     cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (user_id,))
     user_data = cursor.fetchone()
     cursor.close()
     db.close()
    if user_data:
     return Usuario(user_data['id_usuario'], user_data['nombre'], user_data['email'], user_data['password'])
     return None


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/servicios')
def servicios():
    db = obtener_conexion()
    if db:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM servicios")
        lista = cursor.fetchall()
        cursor.close()
        db.close()
        return render_template('servicios.html', servicios=lista)
    return "Error de conexión"

@app.route('/agregar', methods=['POST'])
def agregar():
    nombre = request.form['nombre']
    costo = request.form['costo']
    especialidad = request.form['especialidad'] # Captura del formulario
    
    db = obtener_conexion()
    if db:
        cursor = db.cursor()
        # Asegúrate que en MySQL la columna sea 'Especialidad'
        sql = "INSERT INTO servicios (nombre, precio, Especialidad) VALUES (%s, %s, %s)"
        cursor.execute(sql, (nombre, costo, especialidad))
        db.commit()
        cursor.close()
        db.close()
    return redirect(url_for('servicios'))

@app.route('/editar/<int:id>')
def editar(id):
    db = obtener_conexion()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM servicios WHERE id = %s", (id,))
    res = cursor.fetchone()
    cursor.close()
    db.close()
    return render_template('editar.html', servicio=res)

@app.route('/actualizar/<int:id>', methods=['POST'])
def actualizar(id):
    nombre = request.form['nombre']
    costo = request.form['costo']
    especialidad = request.form['especialidad']
    
    db = obtener_conexion()
    cursor = db.cursor()
    sql = "UPDATE servicios SET nombre=%s, precio=%s, Especialidad=%s WHERE id=%s"
    cursor.execute(sql, (nombre, costo, especialidad, id))
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('servicios'))

@app.route('/eliminar/<int:id>')
def eliminar(id):
    db = obtener_conexion()
    cursor = db.cursor()
    cursor.execute("DELETE FROM servicios WHERE id = %s", (id,))
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('servicios'))

  # Proyecto de Liliana  

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        # Encriptamos la clave antes de guardarla
        pass_hash = generate_password_hash(request.form['password'])
        
        db = obtener_conexion()
        if db:
            cursor = db.cursor()
            cursor.execute("INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)", 
                           (nombre, email, pass_hash))
            db.commit()
            cursor.close()
            db.close()
            return redirect(url_for('login'))
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = obtener_conexion()
        if db:
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            user = cursor.fetchone()
            cursor.close()
            db.close()
            if user and check_password_hash(user['password'], password):
                user_obj = Usuario(user['id_usuario'], user['nombre'], user['email'] ,user['password'])
                login_user(user_obj)
                return redirect(url_for('index'))
            else:
                return "Usuario o contraseña incorrectos"
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)