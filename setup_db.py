import sqlite3

# Conexión
conn = sqlite3.connect('database.db')

# Tabla alumnos
conn.execute('''
CREATE TABLE IF NOT EXISTS alumnos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    cedula TEXT NOT NULL
)
''')

# Tabla talleres
conn.execute('''
CREATE TABLE IF NOT EXISTS talleres (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alumno_id INTEGER,
    taller TEXT,
    puntos INTEGER,
    fecha TEXT,
    FOREIGN KEY (alumno_id) REFERENCES alumnos(id)
)
''')
# Tabla de talleres independientes
conn.execute('''
CREATE TABLE IF NOT EXISTS talleres_disponibles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    fecha TEXT
)
''')


# Guardar y cerrar
conn.commit()
conn.close()
