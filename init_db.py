import sqlite3
import os

# Ruta segura para Render o local
DB_PATH = os.path.join(os.path.dirname(__file__), 'db', 'data.db')

def crear_tablas():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # 🧍 Tabla de clientes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                correo TEXT NOT NULL,
                telefono TEXT,
                hosting_vencimiento TEXT
            )
        ''')

        # 📅 Agregar columna de fecha_registro si no existe
        cursor.execute("PRAGMA table_info(clientes)")
        columnas_clientes = [col[1] for col in cursor.fetchall()]
        if 'fecha_registro' not in columnas_clientes:
            cursor.execute("ALTER TABLE clientes ADD COLUMN fecha_registro TEXT DEFAULT (date('now'))")
            print("✅ Columna 'fecha_registro' agregada a la tabla 'clientes'.")

        # ✅ Tabla de tareas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descripcion TEXT,
                cliente_id INTEGER,
                fecha_vencimiento DATE,
                estado TEXT DEFAULT 'pendiente',
                fecha_creacion TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (cliente_id) REFERENCES clientes (id)
            )
        ''')

        print("✅ Tablas creadas o actualizadas correctamente.")

if __name__ == "__main__":
    crear_tablas()
