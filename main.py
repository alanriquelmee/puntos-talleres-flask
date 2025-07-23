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
@app.route('/talleres_disponibles', methods=['GET', 'POST'])
def talleres_disponibles():
    db = get_db()

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        fecha = request.form['fecha']
        db.execute("INSERT INTO talleres_disponibles (nombre, descripcion, fecha) VALUES (?, ?, ?)",
                   (nombre, descripcion, fecha))
        db.commit()
        return redirect('/talleres_disponibles')

    talleres = db.execute("SELECT * FROM talleres_disponibles ORDER BY fecha DESC").fetchall()
    return render_template('talleres_disponibles.html', talleres=talleres)


import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
