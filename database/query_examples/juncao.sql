SELECT L.titulo, A.nome AS nome_autor, E.nome AS nome_editora
FROM Livro AS L
JOIN Escrito_por AS EP ON L.ISBN = EP.ISBN
JOIN Autor AS A ON EP.id_autor = A.id_autor
JOIN Editora AS E ON L.id_editora = E.id_editora;