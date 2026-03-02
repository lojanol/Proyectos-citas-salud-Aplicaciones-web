from flask import Flask, render_template
import os

app = Flask(__name__)

# 1. RUTA PRINCIPAL (Soluciona el problema de la página en blanco)
@app.route('/')
def home():
    return render_template('index.html')

# 2. Ruta para la página Acerca de
@app.route('/about')
def about():
    return render_template('about.html')

# 3. Ruta para la página de Servicios/Productos
@app.route('/servicios')
def servicios():
    return render_template('productos.html')

# 4. CONFIGURACIÓN DE ARRANQUE (Asegúrate de incluir esto al final)
if __name__ == '__main__':
    # Render asigna un puerto dinámico mediante la variable de entorno 'PORT'
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)