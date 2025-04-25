# views.py
import os
import sqlite3
import requests
from flask import jsonify, request
from datetime import datetime

# Ruta segura a la base de datos
DB_PATH = os.path.join(os.path.dirname(__file__), 'db', 'data.db')

# 📊 Clientes registrados por mes
def clientes_por_mes():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                strftime('%Y-%m', fecha_registro) as mes,
                COUNT(*) as total
            FROM clientes
            GROUP BY mes
            ORDER BY mes DESC
            LIMIT 6
        """)
        resultados = cursor.fetchall()

    meses = []
    cantidades = []

    for fila in reversed(resultados):  # Mostrar desde el más antiguo
        meses.append(fila["mes"])
        cantidades.append(fila["total"])

    return jsonify({"meses": meses, "cantidades": cantidades})

# 🌤️ API Clima desde OpenWeatherMap
def clima_actual():
    ciudad = request.args.get("ciudad", "El Monte,CL")
    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        return jsonify({"error": "API key no configurada"}), 500

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}&units=metric&lang=es"
        res = requests.get(url)
        res.raise_for_status()
        return jsonify(res.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"No se pudo obtener el clima: {str(e)}"}), 500

# ✅ Guardar tarea desde consola o interfaz
def agregar_tarea():
    data = request.get_json()
    titulo = data.get("titulo")
    descripcion = data.get("descripcion", "")
    fecha_vencimiento = data.get("fecha_vencimiento", None)

    if not titulo:
        return jsonify({"error": "El campo 'titulo' es obligatorio."}), 400

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tareas (titulo, descripcion, fecha_vencimiento)
            VALUES (?, ?, ?)
        """, (titulo, descripcion, fecha_vencimiento))
        conn.commit()

    return jsonify({"mensaje": "✅ Tarea guardada correctamente."}), 201

# 📋 Listar todas las tareas (útil para futuras notificaciones o widgets)
def listar_tareas():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tareas ORDER BY fecha_creacion DESC")
        tareas = [dict(row) for row in cursor.fetchall()]
    return jsonify(tareas)
    
# 🔔 Tareas urgentes para mostrar en el dashboard
def tareas_urgentes():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, titulo, fecha_vencimiento, estado
            FROM tareas
            WHERE estado = 'pendiente'
            ORDER BY fecha_vencimiento ASC
            LIMIT 3
        """)
        tareas = [dict(row) for row in cursor.fetchall()]
    return jsonify(tareas)

