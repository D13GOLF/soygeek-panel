# core/dashboard.py
from flask import Blueprint, render_template

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def home():
    return render_template('dashboard/index.html', title="Panel de Control")

@dashboard_bp.route('/clientes')
def clientes():
    return render_template('dashboard/clientes.html', title="Gestión de Clientes")

@dashboard_bp.route('/servicios')
def servicios():
    return render_template('dashboard/servicios.html', title="Servicios Contratados")
