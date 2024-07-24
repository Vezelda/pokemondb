INSERT INTO Pokemones (nombre, tipo, habilidad, ataque, defensa, velocidad, hp)
SELECT 'Absol', 'Oscuro', 'Shadowball', 55, 40, 90, 35
WHERE NOT EXISTS (SELECT 1 FROM Pokemones WHERE nombre = 'Absol');

INSERT INTO Pokemones (nombre, tipo, habilidad, ataque, defensa, velocidad, hp)
SELECT 'Greninja', 'Agua', 'Shuriken de Agua', 52, 43, 65, 39
WHERE NOT EXISTS (SELECT 1 FROM Pokemones WHERE nombre = 'Greninja');

INSERT INTO Entrenadores (nombre, edad, ciudad)
SELECT 'Joel', 10, 'Asuncion'
WHERE NOT EXISTS (SELECT 1 FROM Entrenadores WHERE nombre = 'Joel');

INSERT INTO Entrenadores (nombre, edad, ciudad)
SELECT 'Abril', 15, 'Luque'
WHERE NOT EXISTS (SELECT 1 FROM Entrenadores WHERE nombre = 'Abril');

INSERT INTO Entrenadores_Pokemones (entrenador_id, pokemon_id)
SELECT e.id, p.id
FROM Entrenadores e, Pokemones p
WHERE e.nombre = 'Joel' AND p.nombre = 'Absol'
AND NOT EXISTS (
    SELECT 1 FROM Entrenadores_Pokemones ep
    WHERE ep.entrenador_id = e.id AND ep.pokemon_id = p.id
);

INSERT INTO Entrenadores_Pokemones (entrenador_id, pokemon_id)
SELECT e.id, p.id
FROM Entrenadores e, Pokemones p
WHERE e.nombre = 'Abril' AND p.nombre = 'Greninja'
AND NOT EXISTS (
    SELECT 1 FROM Entrenadores_Pokemones ep
    WHERE ep.entrenador_id = e.id AND ep.pokemon_id = p.id
);


INSERT INTO Batallas (fecha, entrenador1_id, entrenador2_id, pokemon1_id, pokemon2_id, resultado)
SELECT '2024-07-01',
       (SELECT id FROM Entrenadores WHERE nombre = 'Joel' LIMIT 1),
       (SELECT id FROM Entrenadores WHERE nombre = 'Abril' LIMIT 1),
       (SELECT id FROM Pokemones WHERE nombre = 'Absol' LIMIT 1),
       (SELECT id FROM Pokemones WHERE nombre = 'Greninja' LIMIT 1),
       'Victoria para Joel'
WHERE NOT EXISTS (
    SELECT 1 FROM Batallas
    WHERE fecha = '2024-07-01' AND
          entrenador1_id = (SELECT id FROM Entrenadores WHERE nombre = 'Joel' LIMIT 1) AND
          entrenador2_id = (SELECT id FROM Entrenadores WHERE nombre = 'Abril' LIMIT 1) AND
          pokemon1_id = (SELECT id FROM Pokemones WHERE nombre = 'Absol' LIMIT 1) AND
          pokemon2_id = (SELECT id FROM Pokemones WHERE nombre = 'Greninja' LIMIT 1)
);
