from flask import Flask, render_template

app = Flask(__name__)

# Ruta para la página de inicio (index.html)
@app.route('/')
def home():
    return render_template('index.html')

# Ruta para la página Acerca de (about.html)
@app.route('/about')
def about():
    return render_template('about.html')

# Ruta para la página de Servicios/Productos (productos.html)
@app.route('/servicios')
def servicios():
    return render_template('productos.html')

if __name__ == '__main__':
    # Esto es importante para que funcione localmente, 
    # pero Render usará gunicorn para la producción.
    app.run(debug=True)