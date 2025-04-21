import sqlite3
import os

# Ruta segura para Render o local
DB_PATH = os.path.join(os.path.dirname(__file__), 'db', 'data.db')

def crear_tablas():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # Tabla clientes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                correo TEXT NOT NULL,
                telefono TEXT,
                hosting_vencimiento TEXT
            )
        ''')

        # Tabla tareas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descripcion TEXT,
                cliente_id INTEGER,
                completada INTEGER DEFAULT 0,
                FOREIGN KEY (cliente_id) REFERENCES clientes (id)
            )
        ''')

        print("✅ Tablas creadas o ya existentes.")

# Solo se ejecuta si este archivo es llamado desde otro
if __name__ == "__main__":
    crear_tablas()
