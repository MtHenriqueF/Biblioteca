UPDATE Livro
SET 
    id_editora = 99999 --Essa editora nao existe.
WHERE 
    ISBN = '978-0-345-39180-3';