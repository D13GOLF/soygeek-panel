# core/clientes.py
from flask import Blueprint, request, redirect, url_for, render_template, flash
from core.clientes_db import agregar_cliente_db, editar_cliente_db, eliminar_cliente_db, obtener_clientes_db

clientes_bp = Blueprint("clientes_bp", __name__)

@clientes_bp.route("/clientes", methods=["GET"])
def clientes():
    clientes = obtener_clientes_db()
    return render_template("clientes.html", title="Gestión de Clientes", clientes=clientes)

@clientes_bp.route("/clientes/agregar", methods=["POST"])
def agregar_cliente():
    data = request.form
    resultado = agregar_cliente_db(data)
    flash(resultado["mensaje"], "success" if resultado["ok"] else "danger")
    return redirect(url_for("clientes_bp.clientes"))

@clientes_bp.route("/clientes/editar/<int:id>", methods=["POST"])
def editar_cliente(id):
    data = request.form
    resultado = editar_cliente_db(id, data)
    flash(resultado["mensaje"], "success" if resultado["ok"] else "danger")
    return redirect(url_for("clientes_bp.clientes"))

@clientes_bp.route("/clientes/eliminar/<int:id>", methods=["POST"])
def eliminar_cliente(id):
    resultado = eliminar_cliente_db(id)
    flash(resultado["mensaje"], "success" if resultado["ok"] else "danger")
    return redirect(url_for("clientes_bp.clientes"))
