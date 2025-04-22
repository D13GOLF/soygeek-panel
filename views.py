# views.py
import sqlite3
from flask import jsonify
from datetime import datetime
import os

# Ruta segura a la base de datos
DB_PATH = os.path.join(os.path.dirname(__file__), 'db', 'data.db')

def clientes_por_mes():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Asegúrate de que la tabla tenga la columna fecha_registro
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
