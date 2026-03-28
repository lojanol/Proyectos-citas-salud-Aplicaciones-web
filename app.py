from fpdf import FPDF
from flask import send_file

from services.producto_service import ProductoService

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


    @app.route('/productos')
    @login_required # Esto protege la ruta para que solo entren usuarios logueados
    def lista_productos():
    # 1. Llamamos al servicio para traer los datos de MySQL
     productos = ProductoService.listar_todos()
    
    # 2. Enviamos esos datos al archivo HTML para que se vean
     return render_template('productos.html', productos=productos)
    

    # --- RUTA PARA CREAR PRODUCTOS (NUEVO) ---
@app.route('/productos/agregar', methods=['POST'])
@login_required
def agregar_producto():
    # Capturamos los datos del formulario de productos.html
    nombre = request.form['nombre']
    precio = request.form['precio']
    stock = request.form['stock']
    
    # Llamamos al servicio para insertar en la base de datos
    ProductoService.insertar(nombre, precio, stock)
    
    flash("Producto guardado exitosamente")
    return redirect(url_for('lista_productos'))

# Esta es la que ya tienes:
@app.route('/productos')
@login_required 
def lista_productos():
    productos = ProductoService.listar_todos()
    return render_template('productos/productos.html', productos=productos)
    

    # ... debajo de lista_productos() ...

@app.route('/productos/reporte')
@login_required
def reporte_productos():
    # 1. Traemos los datos desde el servicio que ya configuraste
    productos = ProductoService.listar_todos() 
    
    # 2. Creamos el objeto PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    
    # Título principal
    pdf.cell(190, 10, txt="REPORTE DE INVENTARIO - SISTEMA WEB", ln=1, align='C')
    pdf.ln(10) 
    
    # Encabezados de la tabla
    pdf.set_font("Arial", 'B', 12)
    pdf.set_fill_color(200, 220, 255) # Color celeste suave para el encabezado
    pdf.cell(30, 10, "ID", 1, 0, 'C', True)
    pdf.cell(80, 10, "Nombre del Producto", 1, 0, 'C', True)
    pdf.cell(40, 10, "Precio", 1, 0, 'C', True)
    pdf.cell(40, 10, "Stock", 1, 1, 'C', True)
    
    # 3. Llenamos la tabla con los datos de MySQL
    pdf.set_font("Arial", size=11)

    for p in productos:
     pdf.cell(30, 10, str(p['id']), 1, 0, 'C')            # Antes decía 'id_producto'
     pdf.cell(80, 10, p['nombre'], 1, 0, 'C')             
     pdf.cell(40, 10, str(p['precio']), 1, 0, 'C')       
     pdf.cell(40, 10, p['Especialidad'], 1, 1, 'C')      # Antes decía 'Stock'

    # 4. Generamos y enviamos el archivo
    nombre_archivo = "reporte_productos.pdf"
    pdf.output(nombre_archivo)
    return send_file(nombre_archivo, as_attachment=True)

# LA LÍNEA 151 DE TU IMAGEN SE MANTIENE AL FINAL:


# --- RUTAS PARA COMPLETAR EL CRUD ---

@app.route('/productos/eliminar/<int:id>')
@login_required
def eliminar_producto(id):
    # Llama a la función 'eliminar' que acabas de crear en ProductoService
    ProductoService.eliminar(id)
    flash("Producto eliminado correctamente")
    return redirect(url_for('lista_productos'))

@app.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_producto(id):
    if request.method == 'POST':
        # Captura los datos del formulario de edición
        nombre = request.form['nombre']
        precio = request.form['precio']
        stock = request.form['stock']
        
        # Llama a la función 'actualizar' de tu servicio
        ProductoService.actualizar(id, nombre, precio, stock)
        flash("Producto actualizado con éxito")
        return redirect(url_for('lista_productos'))
    
    # Si es GET, busca el producto para mostrar sus datos actuales en el formulario
    producto = ProductoService.obtener_por_id(id)
    return render_template('productos/editar.html', producto=producto)
    
if __name__ == '__main__':
    app.run(debug=True)