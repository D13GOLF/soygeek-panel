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
                tipo_servicio TEXT,
                hosting_vencimiento TEXT,
                fecha_registro TEXT DEFAULT (date('now'))
                tipo_servicio TEXT DEFAULT 'General' -- 🚀 Nuevo campo agregado
            )
        ''')

        # 📅 Verificar si las columnas existen (por si actualizas una DB ya creada)
        cursor.execute("PRAGMA table_info(clientes)")
        columnas_clientes = [col[1] for col in cursor.fetchall()]
        if 'fecha_registro' not in columnas_clientes:
            cursor.execute("ALTER TABLE clientes ADD COLUMN fecha_registro TEXT DEFAULT (date('now'))")
            print("✅ Columna 'fecha_registro' agregada a la tabla 'clientes'.")

        if 'tipo_servicio' not in columnas_clientes:
            cursor.execute("ALTER TABLE clientes ADD COLUMN tipo_servicio TEXT DEFAULT 'General'")
            print("✅ Columna 'tipo_servicio' agregada a la tabla 'clientes'.")

        # 📝 Tabla de categorías de tareas (NUEVA)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                color TEXT DEFAULT '#3b82f6' -- Color Futurista por defecto (Azul eléctrico)
                    
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
            cursor.execute("INSERT INTO categorias (nombre, color) VALUES ('Sin Categorizar', '#64748b')")  # Gris futurista
            print("✅ Categoría 'Sin Categorizar' creada.")

        print("✅ Base de datos lista con Clientes, Categorías y Tareas actualizadas.")

if __name__ == "__main__":
    crear_tablas()
