from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Conexión a la base de datos
def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Página principal: lista de alumnos
@app.route('/')
def index():
    db = get_db()
    alumnos = db.execute("SELECT * FROM alumnos").fetchall()
    return render_template('index.html', alumnos=alumnos)

# Agregar un nuevo alumno
@app.route('/nuevo_alumno', methods=['POST'])
def nuevo_alumno():
    nombre = request.form['nombre']
    cedula = request.form['cedula']
    db = get_db()
    db.execute("INSERT INTO alumnos (nombre, cedula) VALUES (?, ?)", (nombre, cedula))
    db.commit()
    return redirect('/')

# Asignar puntos a un alumno
@app.route('/asignar_puntos', methods=['POST'])
def asignar_puntos():
    alumno_id = request.form['alumno_id']
    taller = request.form['taller']
    puntos = int(request.form['puntos'])
    fecha = request.form['fecha']
    db = get_db()
    db.execute(
        "INSERT INTO talleres (alumno_id, taller, puntos, fecha) VALUES (?, ?, ?, ?)",
        (alumno_id, taller, puntos, fecha)
    )
    db.commit()
    return redirect('/')

# Mostrar puntaje total por alumno
@app.route('/puntajes')
def puntajes():
    db = get_db()
    puntajes = db.execute('''
        SELECT alumnos.nombre, SUM(talleres.puntos) AS total_puntos
        FROM alumnos
        JOIN talleres ON alumnos.id = talleres.alumno_id
        GROUP BY alumnos.id
    ''').fetchall()
    return render_template('puntajes.html', puntajes=puntajes)
@app.route('/eliminar_alumno/<int:alumno_id>', methods=['POST'])
def eliminar_alumno(alumno_id):
    db = get_db()
    # Borrar primero los puntos relacionados
    db.execute('DELETE FROM talleres WHERE alumno_id = ?', (alumno_id,))
    # Luego borrar el alumno
    db.execute('DELETE FROM alumnos WHERE id = ?', (alumno_id,))
    db.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
