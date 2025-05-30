# init_db.py
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
                tipo_servicio TEXT DEFAULT 'General',
                hosting_vencimiento TEXT,
                fecha_registro TEXT DEFAULT (date('now'))
            )
        ''')

        # 📝 Tabla de categorías de tareas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                color TEXT DEFAULT '#3b82f6'
            )
        ''')

        # 🧩 Tabla de tareas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descripcion TEXT,
                cliente_id INTEGER,
                fecha_vencimiento DATE,
                estado TEXT DEFAULT 'pendiente',
                fecha_creacion TEXT DEFAULT (datetime('now')),
                categoria_id INTEGER,
                FOREIGN KEY (cliente_id) REFERENCES clientes (id),
                FOREIGN KEY (categoria_id) REFERENCES categorias (id)
            )
        ''')

        # ✅ Crear categoría "Sin Categorizar" si no existe
        cursor.execute("SELECT COUNT(*) FROM categorias WHERE nombre = 'Sin Categorizar'")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO categorias (nombre, color) VALUES ('Sin Categorizar', '#64748b')")
            print("✅ Categoría 'Sin Categorizar' creada.")

        # 🧠 Tabla de logs del Bot
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs_bot (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                origen TEXT,
                usuario TEXT,
                mensaje TEXT,
                fecha_hora TEXT DEFAULT (datetime('now'))
            )
        ''')
        print("✅ Tabla 'logs_bot' verificada/creada para registrar actividades del Bot.")

    print("✅ Base de datos lista y actualizada para el futuro, Principe Sayayin 🚀")

if __name__ == "__main__":
    crear_tablas()
