import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db', 'data.db')

def obtener_clientes():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        return cursor.execute("SELECT * FROM clientes").fetchall()

def agregar_cliente(nombre, correo, telefono, tipo_servicio, hosting_vencimiento):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO clientes (nombre, correo, telefono, tipo_servicio, hosting_vencimiento)
            VALUES (?, ?, ?, ?, ?)
        """, (nombre, correo, telefono, tipo_servicio, hosting_vencimiento))
        conn.commit()

def actualizar_cliente(id, nombre, correo, telefono, tipo_servicio, hosting_vencimiento):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE clientes
            SET nombre = ?, correo = ?, telefono = ?, tipo_servicio = ?, hosting_vencimiento = ?
            WHERE id = ?
        """, (nombre, correo, telefono, tipo_servicio, hosting_vencimiento, id))
        conn.commit()

def eliminar_cliente(id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clientes WHERE id = ?", (id,))
        conn.commit()
