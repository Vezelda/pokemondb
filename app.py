from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

# Configuración de la conexión a la base de datos
conn = psycopg2.connect(
    host="localhost",
    database="pokemondb",
    user="pokemon",
    password="vezelda0512!"
)
cur = conn.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/consultar_entrenadores')
def consultar_entrenadores():
    cur.execute('''
        SELECT e.id, e.nombre AS entrenador, p.nombre AS pokemon
        FROM Entrenadores e
        LEFT JOIN Entrenadores_Pokemones ep ON e.id = ep.entrenador_id
        LEFT JOIN Pokemones p ON ep.pokemon_id = p.id
    ''')
    entrenadores_pokemones = cur.fetchall()
    return render_template('consultar_entrenadores.html', entrenadores_pokemones=entrenadores_pokemones)

@app.route('/consultar_batallas')
def consultar_batallas():
    cur.execute('''
        SELECT b.id, b.fecha, e1.nombre AS entrenador1, e2.nombre AS entrenador2, 
               p1.nombre AS pokemon1, p2.nombre AS pokemon2, b.resultado
        FROM Batallas b
        JOIN Entrenadores e1 ON b.entrenador1_id = e1.id
        JOIN Entrenadores e2 ON b.entrenador2_id = e2.id
        JOIN Pokemones p1 ON b.pokemon1_id = p1.id
        JOIN Pokemones p2 ON b.pokemon2_id = p2.id
    ''')
    batallas = cur.fetchall()
    return render_template('consultar_batallas.html', batallas=batallas)
@app.route('/cargar_entrenador', methods=['GET', 'POST'])
def cargar_entrenador():
    if request.method == 'POST':
        nombre_entrenador = request.form['nombre_entrenador']
        edad = request.form['edad']
        ciudad = request.form['ciudad']
        nombre_pokemon = request.form['nombre_pokemon']
        tipo = request.form['tipo']
        habilidad = request.form['habilidad']
        ataque = request.form['ataque']
        defensa = request.form['defensa']
        velocidad = request.form['velocidad']
        hp = request.form['hp']

        # Inserta el entrenador
        cur.execute('INSERTc INTO Entrenadores (nombre, edad, ciudad) VALUES (%s, %s, %s) RETURNING id', 
                    (nombre_entrenador, edad, ciudad))
        entrenador_id = cur.fetchone()[0]

        # Inserta el Pokémon
        cur.execute('INSERT INTO Pokemones (nombre, tipo, habilidad, ataque, defensa, velocidad, hp) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id',
                    (nombre_pokemon, tipo, habilidad, ataque, defensa, velocidad, hp))
        pokemon_id = cur.fetchone()[0]

        # Relaciona el entrenador con el Pokémon
        cur.execute('INSERT INTO Entrenadores_Pokemones (entrenador_id, pokemon_id) VALUES (%s, %s)', 
                    (entrenador_id, pokemon_id))

        conn.commit()
        return redirect('/consultar_entrenadores')
    else:
        return render_template('cargar_entrenador.html')

@app.route('/cargar_batalla', methods=['GET', 'POST'])
def cargar_batalla():
    if request.method == 'POST':
        fecha = request.form['fecha']
        entrenador1_id = request.form['entrenador1_id']
        entrenador2_id = request.form['entrenador2_id']
        pokemon1_id = request.form['pokemon1_id']
        pokemon2_id = request.form['pokemon2_id']
        resultado = request.form['resultado']

        cur.execute('''
            INSERT INTO Batallas (fecha, entrenador1_id, entrenador2_id, pokemon1_id, pokemon2_id, resultado)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (fecha, entrenador1_id, entrenador2_id, pokemon1_id, pokemon2_id, resultado))

        conn.commit()
        return redirect('/consultar_batallas')
    else:
        cur.execute('SELECT id, nombre FROM Entrenadores')
        entrenadores = cur.fetchall()
        cur.execute('SELECT ep.entrenador_id, p.id, p.nombre FROM Pokemones p JOIN Entrenadores_Pokemones ep ON p.id = ep.pokemon_id')
        pokemones = cur.fetchall()
        return render_template('cargar_batalla.html', entrenadores=entrenadores, pokemones=pokemones)

@app.route('/eliminar_entrenador', methods=['GET', 'POST'])
def eliminar_entrenador():
    if request.method == 'POST':
        entrenador_id = request.form['entrenador_id']

        cur.execute('DELETE FROM Batallas WHERE entrenador1_id = %s OR entrenador2_id = %s', (entrenador_id, entrenador_id))
        cur.execute('DELETE FROM Entrenadores_Pokemones WHERE entrenador_id = %s', (entrenador_id,))
        cur.execute('DELETE FROM Entrenadores WHERE id = %s', (entrenador_id,))

        conn.commit()
        return redirect('/consultar_entrenadores')
    else:
        cur.execute('''
            SELECT e.id, e.nombre, p.nombre AS pokemon
            FROM Entrenadores e
            LEFT JOIN Entrenadores_Pokemones ep ON e.id = ep.entrenador_id
            LEFT JOIN Pokemones p ON ep.pokemon_id = p.id
        ''')
        entrenadores_pokemones = cur.fetchall()
        return render_template('eliminar_entrenador.html', entrenadores_pokemones=entrenadores_pokemones)

@app.route('/modificar_entrenador', methods=['GET', 'POST'])
def modificar_entrenador():
    if request.method == 'POST':
        entrenador_id = request.form['entrenador_id']
        nuevo_pokemon_id = request.form['nuevo_pokemon_id']

        cur.execute('UPDATE Entrenadores_Pokemones SET pokemon_id = %s WHERE entrenador_id = %s', 
                    (nuevo_pokemon_id, entrenador_id))
        conn.commit()
        return redirect('/consultar_entrenadores')
    else:
        cur.execute('SELECT e.id, e.nombre, p.id AS pokemon_id, p.nombre AS pokemon_nombre FROM Entrenadores e JOIN Entrenadores_Pokemones ep ON e.id = ep.entrenador_id JOIN Pokemones p ON ep.pokemon_id = p.id')
        entrenadores_pokemones = cur.fetchall()
        cur.execute('SELECT id, nombre FROM Pokemones WHERE id NOT IN (SELECT pokemon_id FROM Entrenadores_Pokemones)')
        pokemones_disponibles = cur.fetchall()
        return render_template('modificar_entrenador.html', entrenadores_pokemones=entrenadores_pokemones, pokemones_disponibles=pokemones_disponibles)

if __name__ == '__main__':
    app.run(debug=True)
