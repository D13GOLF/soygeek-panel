# app.py
from flask import Flask
from core.auth import auth_bp
from core.dashboard import dashboard_bp
from init_db import crear_tablas
from views import clientes_por_mes  # ✅ Importamos la nueva vista API

# Inicializar Flask app
app = Flask(__name__)
app.secret_key = 'clave-secreta-soygeek'
app.config.from_pyfile('config.py')

# Registrar Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)

# Registrar rutas API directamente
app.add_url_rule('/api/clientes-mes', 'clientes_por_mes', clientes_por_mes)

# Crear las tablas si no existen
crear_tablas()

# Solo se usa si ejecutas localmente con python app.py
if __name__ == '__main__':
    app.run(debug=True)
