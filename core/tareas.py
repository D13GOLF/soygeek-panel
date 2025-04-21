from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime
import sqlite3

tareas_bp = Blueprint('tareas', __name__)

DATABASE = 'db/data.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@tareas_bp.route('/tareas')
def tareas():
    conn = get_db_connection()
    tareas = conn.execute('SELECT * FROM tareas ORDER BY fecha_limite ASC').fetchall()
    conn.close()
    return render_template('tareas.html', tareas=tareas)

@tareas_bp.route('/tareas/nueva', methods=['POST'])
def nueva_tarea():
    titulo = request.form['titulo']
    descripcion = request.form['descripcion']
    cliente = request.form['cliente']
    fecha_limite = request.form['fecha_limite']

    conn = get_db_connection()
    conn.execute(
        'INSERT INTO tareas (titulo, descripcion, cliente, estado, fecha_limite) VALUES (?, ?, ?, ?, ?)',
        (titulo, descripcion, cliente, 'pendiente', fecha_limite)
    )
    conn.commit()
    conn.close()
    return redirect(url_for('tareas.tareas'))

@tareas_bp.route('/tareas/completar/<int:id>')
def completar_tarea(id):
    conn = get_db_connection()
    conn.execute('UPDATE tareas SET estado = "completada" WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('tareas.tareas'))

@tareas_bp.route('/tareas/eliminar/<int:id>')
def eliminar_tarea(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tareas WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('tareas.tareas'))
