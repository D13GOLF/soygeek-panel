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

        # Tabla tareas básica sin repetir si ya existe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descripcion TEXT,
                cliente_id INTEGER,
                fecha_vencimiento DATE,
                FOREIGN KEY (cliente_id) REFERENCES clientes (id)
            )
        ''')

        # Verificar si la columna 'estado' existe
        cursor.execute("PRAGMA table_info(tareas)")
        columnas = [col[1] for col in cursor.fetchall()]
        if 'estado' not in columnas:
            cursor.execute("ALTER TABLE tareas ADD COLUMN estado TEXT DEFAULT 'pendiente'")
            print("✅ Columna 'estado' agregada a la tabla 'tareas'.")

        print("✅ Tablas creadas o ya existentes.")

if __name__ == "__main__":
    crear_tablas()
