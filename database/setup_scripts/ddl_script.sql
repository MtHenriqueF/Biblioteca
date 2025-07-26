CREATE TABLE Editora (
	id_editora SERIAL PRIMARY KEY,
	nome VARCHAR(255) NOT NULL
);

CREATE TABLE Autor (
	id_autor SERIAL PRIMARY KEY,
	nome TEXT NOT NULL,
	nacionalidade VARCHAR(20)
);

CREATE TABLE Livro (
	ISBN VARCHAR(17) PRIMARY KEY, -- Ex: 978-1-00-268144-2
	id_editora INTEGER NOT NULL,
	data_publicacao DATE NOT NULL,
	edicao INTEGER,
	genero VARCHAR(50),
	titulo TEXT NOT NULL,
	FOREIGN KEY (id_editora) REFERENCES Editora(id_editora)
		ON DELETE NO ACTION
		ON UPDATE CASCADE
);

CREATE TABLE Escrito_por (
	id_escritura SERIAL PRIMARY KEY,
	ISBN VARCHAR(17) NOT NULL,
	id_autor INTEGER NOT NULL,
	FOREIGN KEY (ISBN) REFERENCES Livro(ISBN)
		ON DELETE NO ACTION
		ON UPDATE CASCADE,
	FOREIGN KEY (id_autor) REFERENCES Autor(id_autor)
		ON DELETE NO ACTION
		ON UPDATE CASCADE,
	UNIQUE (ISBN, id_autor)
);

CREATE TABLE Endereco (
	id_endereco SERIAL PRIMARY KEY,
	nome_bairro VARCHAR(255) NOT NULL,
	nome_rua VARCHAR(255) NOT NULL
);

CREATE TABLE Usuario (
	id_usuario SERIAL PRIMARY KEY,
	id_endereco INTEGER,
	nome VARCHAR(50) NOT NULL,
	email VARCHAR(50),
	telefone VARCHAR(13),
	FOREIGN KEY (id_endereco) REFERENCES Endereco(id_endereco)
		ON DELETE SET NULL
		ON UPDATE CASCADE,
	UNIQUE (email)
);

CREATE TABLE Funcionario (
	id_funcionario SERIAL PRIMARY KEY,
	id_endereco INTEGER,
	email VARCHAR(35),
	nome VARCHAR(50),
	cargo VARCHAR(20),
	FOREIGN KEY (id_endereco) REFERENCES Endereco(id_endereco)
		ON DELETE SET NULL
		ON UPDATE CASCADE,
	UNIQUE (email)
);

CREATE TABLE Exemplar (
	id_exemplar SERIAL PRIMARY KEY,
	ISBN VARCHAR(17),
	status VARCHAR(20) NOT NULL, -- Ex: 'EMPRESTADO', 'LIVRE'
	localizacao TEXT,
	FOREIGN KEY (ISBN) REFERENCES Livro(ISBN)
		ON DELETE NO ACTION
		ON UPDATE CASCADE
);



CREATE TABLE Reserva (
	id_reserva SERIAL PRIMARY KEY,
	ISBN VARCHAR(17) NOT NULL,
	id_usuario INTEGER NOT NULL,
	id_funcionario INTEGER NOT NULL,
	data_reserva DATE,
	status VARCHAR(20),

	FOREIGN KEY (ISBN) REFERENCES Livro(ISBN)
		ON DELETE NO ACTION
		ON UPDATE CASCADE,
	FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
		ON DELETE NO ACTION
		ON UPDATE CASCADE,
	FOREIGN KEY (id_funcionario) REFERENCES Funcionario(id_funcionario)
		ON DELETE NO ACTION
		ON UPDATE CASCADE,

	CONSTRAINT uk_reserva_tripla UNIQUE (id_funcionario, id_usuario, ISBN)
);



CREATE TABLE Emprestimo (
	id_emprestimo SERIAL PRIMARY KEY,
	id_exemplar INTEGER NOT NULL,
	id_usuario INTEGER NOT NULL,
	id_funcionario INTEGER NOT NULL,
	data_emprestimo DATE NOT NULL,
	data_devolucao_prev DATE,
  	data_devolucao DATE, 
	status VARCHAR(20) NOT NULL, -- Ex: 'ATIVO', 'DEVOLVIDO', 'ATRASADO'
	
	FOREIGN KEY (id_exemplar) REFERENCES Exemplar(id_exemplar)
		ON DELETE NO ACTION
		ON UPDATE CASCADE,
	FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
		ON DELETE NO ACTION
		ON UPDATE CASCADE,
	FOREIGN KEY (id_funcionario) REFERENCES Funcionario(id_funcionario)
		ON DELETE NO ACTION
		ON UPDATE CASCADE,

	CONSTRAINT uk_emprestimo_tripla UNIQUE (id_funcionario, id_usuario, id_exemplar)

);


CREATE TABLE PagamentoMulta (
	id_pagamento SERIAL PRIMARY KEY,
	id_emprestimo INTEGER UNIQUE,
	valor_pago DECIMAL(10, 2),
	data_pagamento DATE,
	FOREIGN KEY (id_emprestimo) REFERENCES Emprestimo(id_emprestimo)
		ON DELETE NO ACTION
		ON UPDATE CASCADE
);