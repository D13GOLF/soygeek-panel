# views.py
import os
import sqlite3
import requests
from flask import jsonify, request
from datetime import datetime

# Ruta segura a la base de datos
DB_PATH = os.path.join(os.path.dirname(__file__), 'db', 'data.db')


# 📊 Clientes registrados por mes (gráfico de barras)
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

    for fila in reversed(resultados):  # Mostrar desde el mes más antiguo al más nuevo
        meses.append(fila["mes"])
        cantidades.append(fila["total"])

    return jsonify({"meses": meses, "cantidades": cantidades})


# 🌤️ Clima actual desde OpenWeatherMap (usado en dashboard visual)
def clima_actual():
    ciudad = request.args.get("ciudad", "El Monte,CL")
    api_key = os.getenv("OPENWEATHER_API_KEY")

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}&units=metric&lang=es"
        res = requests.get(url)
        res.raise_for_status()
        return jsonify(res.json())
    except Exception as e:
        return jsonify({"error": f"No se pudo obtener el clima: {str(e)}"}), 500
