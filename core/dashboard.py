# core/dashboard.py
from flask import Blueprint, render_template
import sqlite3
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)

def get_db_connection():
    conn = sqlite3.connect('db/data.db')
    conn.row_factory = sqlite3.Row
    return conn

@dashboard_bp.route('/')
def home():
    conn = get_db_connection()

    total_clientes = conn.execute('SELECT COUNT(*) FROM clientes').fetchone()[0]
    tareas_completadas = conn.execute("SELECT COUNT(*) FROM tareas WHERE estado = 'completada'").fetchone()[0]
    tareas_pendientes = conn.execute("SELECT COUNT(*) FROM tareas WHERE estado = 'pendiente'").fetchone()[0]
    tareas_vencidas = conn.execute("SELECT COUNT(*) FROM tareas WHERE estado = 'pendiente' AND fecha_vencimiento < ?", (datetime.now().date(),)).fetchone()[0]

    # Si aún no tienes la columna fecha_vencimiento_hosting, este valor será 0
    try:
        hostings_por_vencer = conn.execute("SELECT COUNT(*) FROM clientes WHERE fecha_vencimiento_hosting < ?", (datetime.now().date(),)).fetchone()[0]
    except:
        hostings_por_vencer = 0

    conn.close()

    return render_template('dashboard.html',
        title="Panel de Control SoyGeek",
        total_clientes=total_clientes,
        tareas_completadas=tareas_completadas,
        tareas_pendientes=tareas_pendientes,
        tareas_vencidas=tareas_vencidas,
        hostings_por_vencer=hostings_por_vencer
    )

@dashboard_bp.route('/clientes')
def clientes():
    return render_template('dashboard/clientes.html', title="Gestión de Clientes")

@dashboard_bp.route('/servicios')
def servicios():
    return render_template('dashboard/servicios.html', title="Servicios Contratados")
