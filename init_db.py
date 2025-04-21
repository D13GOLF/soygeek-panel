import sqlite3

DATABASE = 'db/data.db'

def crear_tabla_tareas():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            cliente TEXT,
            estado TEXT DEFAULT 'pendiente',
            fecha_limite TEXT
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Base de datos y tabla 'tareas' creadas correctamente.")

if __name__ == "__main__":
    crear_tabla_tareas()
