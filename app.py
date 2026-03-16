from flask import Flask, render_template, request, redirect, url_for
from Conexion.conexion import obtener_conexion

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)