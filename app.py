# app.py
from flask import Flask, request, jsonify
from core.auth import auth_bp
from core.dashboard import dashboard_bp
from init_db import crear_tablas
from views import clientes_por_mes  # ✅ Importamos la nueva vista API
import requests

# Inicializar Flask app
app = Flask(__name__)
app.secret_key = 'clave-secreta-soygeek'
app.config.from_pyfile('config.py')

# Registrar Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)

# Registrar rutas API personalizadas
app.add_url_rule('/api/clientes-mes', 'clientes_por_mes', clientes_por_mes)

# Crear las tablas si no existen
crear_tablas()

# Endpoint para interactuar con el bot (usado por la consola del panel)
@app.route('/api/bot', methods=['POST'])
def api_bot():
    data = request.get_json()
    mensaje = data.get('mensaje')

    try:
        respuesta = requests.post(
            "https://bot-geek-v1.onrender.com/api/consultar",  # Cambia si usas otra URL
            json={"message": mensaje}
        )
        data = respuesta.json()
        return jsonify({"respuesta": data.get("respuesta", "Sin respuesta 🤖")})
    except Exception as e:
        return jsonify({"respuesta": f"Error al contactar al bot: {str(e)}"})

# Solo se usa si ejecutas localmente con python app.py
if __name__ == '__main__':
    app.run(debug=True)
