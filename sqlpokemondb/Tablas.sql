-- Creamos la tabla de Pokemones.
CREATE TABLE IF NOT EXISTS Pokemones (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    habilidad VARCHAR(50),
    ataque INT,
    defensa INT,
    velocidad INT,
    hp INT
);

-- Creamos la tabla de Entrenadores.
CREATE TABLE IF NOT EXISTS Entrenadores (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    edad INT,
    ciudad VARCHAR(50)
);

-- Creamos la tabla intermedia Entrenadores_Pokemones
CREATE TABLE IF NOT EXISTS Entrenadores_Pokemones (
    entrenador_id INT,
    pokemon_id INT,
    PRIMARY KEY (entrenador_id, pokemon_id),
    FOREIGN KEY (entrenador_id) REFERENCES Entrenadores(id),
    FOREIGN KEY (pokemon_id) REFERENCES Pokemones(id)
);

-- Creamos la tabla de batallas
CREATE TABLE IF NOT EXISTS Batallas (
    id SERIAL PRIMARY KEY,
    fecha DATE,
    entrenador1_id INT,
    entrenador2_id INT,
    pokemon1_id INT,
    pokemon2_id INT,
    resultado VARCHAR(50),
    FOREIGN KEY (entrenador1_id) REFERENCES Entrenadores(id),
    FOREIGN KEY (entrenador2_id) REFERENCES Entrenadores(id),
    FOREIGN KEY (pokemon1_id) REFERENCES Pokemones(id),
    FOREIGN KEY (pokemon2_id) REFERENCES Pokemones(id)
);
