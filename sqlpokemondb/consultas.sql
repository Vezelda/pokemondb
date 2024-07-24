-- Ver todos los entrenadores y sus pokemones
SELECT e.id, e.nombre AS entrenador, p.nombre AS pokemon
FROM Entrenadores e
LEFT JOIN Entrenadores_Pokemones ep ON e.id = ep.entrenador_id
LEFT JOIN Pokemones p ON ep.pokemon_id = p.id;

-- Ver todas las batallas
SELECT b.id, b.fecha, e1.nombre AS entrenador1, e2.nombre AS entrenador2, p1.nombre AS pokemon1, p2.nombre AS pokemon2, b.resultado
FROM Batallas b
JOIN Entrenadores e1 ON b.entrenador1_id = e1.id
JOIN Entrenadores e2 ON b.entrenador2_id = e2.id
JOIN Pokemones p1 ON b.pokemon1_id = p1.id
JOIN Pokemones p2 ON b.pokemon2_id = p2.id;

-- Ver Pokemones no asignados a ningun entrenador
SELECT id, nombre 
FROM Pokemones 
WHERE id NOT IN (SELECT pokemon_id FROM Entrenadores_Pokemones);

-- Actualizar en pOKEMON DE UN ENTRENADOR
UPDATE Entrenadores_Pokemones
SET pokemon_id = 1
WHERE entrenador_id = 1;

-- Eliminar un entrenador y todas sus referencias
-- Eliminar referencias en la tabla Batallas
DELETE FROM Batallas WHERE entrenador1_id = 21 OR entrenador2_id = 1;

-- Eliminar referencias en la tabla intermedia Entrenadores_Pokemones
DELETE FROM Entrenadores_Pokemones WHERE entrenador_id = 21;

-- Finalmente, eliminar el entrenador
DELETE FROM Entrenadores WHERE id = 21;
