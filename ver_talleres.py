import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

resultados = c.execute('SELECT * FROM talleres').fetchall()

for fila in resultados:
    print(fila)

conn.close()
