# core/dashboard.py
from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3
import os
from datetime import datetime
from collections import Counter

dashboard_bp = Blueprint('dashboard', __name__)
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db', 'data.db')

def obtener_clientes_por_mes():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT fecha_registro FROM clientes WHERE fecha_registro IS NOT NULL")
            fechas = [row['fecha_registro'] for row in cur.fetchall()]
            conteo = Counter()

            for fecha in fechas:
                dt = datetime.strptime(fecha, "%Y-%m-%d")
                clave = dt.strftime("%b %Y")
                conteo[clave] += 1

            meses = list(conteo.keys())
            clientes_mes = list(conteo.values())
            return meses, clientes_mes
    except Exception as e:
        print(f"Error al contar clientes por mes: {e}")
        return [], []

def obtener_clientes_por_servicio():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT tipo_servicio, COUNT(*) as total FROM clientes GROUP BY tipo_servicio")
            resultados = cur.fetchall()

            servicios = [row['tipo_servicio'] for row in resultados]
            cantidad = [row['total'] for row in resultados]
            return servicios, cantidad
    except Exception as e:
        print(f"Error al contar clientes por servicio: {e}")
        return [], []

@dashboard_bp.route('/')
def home():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row

        clientes_count = conn.execute("SELECT COUNT(*) FROM clientes").fetchone()[0]
        tareas_pendientes = conn.execute("SELECT COUNT(*) FROM tareas WHERE estado = 'pendiente'").fetchone()[0]
        tareas_completadas = conn.execute("SELECT COUNT(*) FROM tareas WHERE estado = 'completada'").fetchone()[0]
        tareas_vencidas = conn.execute("SELECT COUNT(*) FROM tareas WHERE fecha_vencimiento < date('now') AND estado != 'completada'").fetchone()[0]
        hostings_por_vencer = conn.execute("SELECT COUNT(*) FROM clientes WHERE hosting_vencimiento < date('now', '+7 days')").fetchone()[0]

        estado_bot = "Activo ✅"

        meses, clientes_mes = obtener_clientes_por_mes()
        servicios, servicios_cantidad = obtener_clientes_por_servicio()

        tareas_completadas_mes = conn.execute("""
            SELECT strftime('%Y-%m', fecha_vencimiento) AS mes, COUNT(*) as total
            FROM tareas
            WHERE estado = 'completada'
            GROUP BY mes
            ORDER BY mes ASC
            LIMIT 6
        """).fetchall()

        meses_tareas = [row['mes'] for row in tareas_completadas_mes]
        cantidades_tareas = [row['total'] for row in tareas_completadas_mes]

    return render_template(
        'dashboard.html',
        title="Panel de Control",
        clientes_count=clientes_count,
        tareas_pendientes=tareas_pendientes,
        tareas_completadas=tareas_completadas,
        tareas_vencidas=tareas_vencidas,
        hostings_por_vencer=hostings_por_vencer,
        estado_bot=estado_bot,
        meses=meses,
        clientes_mes=clientes_mes,
        meses_tareas=meses_tareas,
        cantidades_tareas=cantidades_tareas,
        servicios=servicios,
        servicios_cantidad=servicios_cantidad
    )
# === SERVICIOS ===
@dashboard_bp.route('/servicios')
def servicios():
    return render_template('servicios.html', title="Servicios de Hosting")

# === TAREAS ===
@dashboard_bp.route('/tareas')
def tareas():
    return render_template('tareas.html', title="Gestión de Tareas")

# === CLIENTES ===
@dashboard_bp.route('/clientes')
def clientes():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        clientes = conn.execute("SELECT * FROM clientes").fetchall()
    return render_template('clientes.html', title="Gestión de Clientes", clientes=clientes)
