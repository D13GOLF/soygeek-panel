# core/dashboard.py
from flask import Blueprint, render_template
import sqlite3
import os

dashboard_bp = Blueprint('dashboard', __name__)

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db', 'data.db')

@dashboard_bp.route('/')
def home():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row

        clientes_count = conn.execute("SELECT COUNT(*) FROM clientes").fetchone()[0]
        tareas_pendientes = conn.execute("SELECT COUNT(*) FROM tareas WHERE estado = 'pendiente'").fetchone()[0]
        tareas_completadas = conn.execute("SELECT COUNT(*) FROM tareas WHERE estado = 'completada'").fetchone()[0]
        tareas_vencidas = conn.execute("SELECT COUNT(*) FROM tareas WHERE fecha_vencimiento < date('now') AND estado != 'completada'").fetchone()[0]
        hostings_por_vencer = conn.execute("SELECT COUNT(*) FROM clientes WHERE hosting_vencimiento < date('now', '+7 days')").fetchone()[0]

        estado_bot = "Activo ✅"  # Aquí podrías hacer ping a tu bot más adelante

    return render_template('dashboard.html',
                           title="Panel de Control",
                           clientes_count=clientes_count,
                           tareas_pendientes=tareas_pendientes,
                           tareas_completadas=tareas_completadas,
                           tareas_vencidas=tareas_vencidas,
                           hostings_por_vencer=hostings_por_vencer,
                           estado_bot=estado_bot)

@dashboard_bp.route('/clientes')
def clientes():
    return render_template('dashboard/clientes.html', title="Gestión de Clientes")

@dashboard_bp.route('/servicios')
def servicios():
    return render_template('dashboard/servicios.html', title="Hostings Contratados")

@dashboard_bp.route('/tareas')
def tareas():
    return render_template('dashboard/tareas.html', title="Gestión de Tareas")

@dashboard_bp.route('/bot')
def bot():
    return render_template('dashboard/bot.html', title="Panel del Bot Geek")
