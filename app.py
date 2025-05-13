# app.py
from flask import Flask, request, jsonify
from core.auth import auth_bp
from core.dashboard import dashboard_bp
from core.clientes import clientes_bp  # 👈 NUEVO: Importar el blueprint de clientes
from init_db import crear_tablas
from views import (
    clientes_por_mes,
    clima_actual,
    agregar_tarea,
    listar_tareas,
    tareas_urgentes
)
import requests

# Inicializar la aplicación Flask
from flask import Flask, request, jsonify
from core.auth import auth_bp
from core.dashboard import dashboard_bp
from core.clientes import clientes_bp  # 👈 NUEVO: Importar el blueprint de clientes
from init_db import crear_tablas
from views import (
    clientes_por_mes,
    clima_actual,
    agregar_tarea,
    listar_tareas,
    tareas_urgentes
)
import requests
import os

# Inicializar la aplicación Flask
app = Flask(__name__)
app.config.from_pyfile('config.py')  # Primero cargar el archivo config.py

# ✅ Luego setear secret_key con fallback
app.secret_key = app.config.get('SECRET_KEY', 'clave-secreta-soygeek')

# 🔗 Registrar Blueprints (rutas del panel)
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(clientes_bp)

# 📊 Rutas API personalizadas
app.add_url_rule('/api/clientes-mes', 'clientes_por_mes', clientes_por_mes)
app.add_url_rule('/api/clima', 'clima_actual', clima_actual)
app.add_url_rule('/api/tareas-urgentes', 'tareas_urgentes', tareas_urgentes)

# ✅ Endpoints de tareas
app.add_url_rule('/api/tareas', 'agregar_tarea', agregar_tarea, methods=['POST'])
app.add_url_rule('/api/tareas/listar', 'listar_tareas', listar_tareas, methods=['GET'])

# 🤖 Endpoint para interactuar con Bot-Geek desde frontend
@app.route('/api/bot', methods=['POST'])
def api_bot():
    data = request.get_json()
    mensaje = data.get('mensaje')
    user_id = data.get('user_id', 'web')

    try:
        respuesta = requests.post(
            "https://bot-geek-v1.onrender.com/api/consultar",
            json={"message": mensaje, "user_id": user_id}
        )
        data = respuesta.json()
        return jsonify({"respuesta": data.get("respuesta", "Sin respuesta 🤖")})
    except Exception as e:
        return jsonify({"respuesta": f"Error al contactar al bot: {str(e)}"}), 500

# 🧱 Crear tablas si no existen
crear_tablas()

# Solo para desarrollo local
if __name__ == '__main__':
    app.run(debug=True)

