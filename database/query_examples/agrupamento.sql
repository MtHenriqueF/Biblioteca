SELECT genero,
COUNT(ISBN) AS total_livros
FROM Livro
GROUP BY genero;