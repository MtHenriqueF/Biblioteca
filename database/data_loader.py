from faker import Faker
import psycopg2
import random
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

fake = Faker('pt_BR')

load_dotenv(dotenv_path='backend/.env') # Ajuste o caminho se necessário
DATABASE_URL = os.getenv("DATABASE_URL")

# Configuração do PostgreSQL
# conn = psycopg2.connect(
#     dbname="biblioteca",
#     user="Sirimarco",
#     password="1234",
#     host="localhost"
# )

conn = psycopg2.connect(DATABASE_URL)

cursor = conn.cursor()

# Configurações
NUM_EDITORAS = 10
NUM_AUTORES = 20
NUM_LIVROS = 50
NUM_ENDERECOS = 30
NUM_USUARIOS = 40
NUM_FUNCIONARIOS = 8
NUM_EXEMPLARES = 100
NUM_RESERVAS = 30
NUM_EMPRESTIMOS = 60
NUM_PAGAMENTOS = 20

generos = ['Romance', 'Ficção Científica', 'Fantasia', 'Mistério', 'Suspense',
           'Biografia', 'História', 'Poesia', 'Autoajuda', 'Infantil']

status_exemplar = ['LIVRE', 'RESERVADO', 'EM MANUTENCAO']
status_emprestimo = ['ATIVO', 'DEVOLVIDO', 'ATRASADO']
status_reserva = ['ATIVA', 'CANCELADA', 'CONCLUIDA']

try:
    # 1. Popular Editora
    print("Populando Editora...")
    cursor.execute("SELECT id_editora FROM Editora")
    editoras_ids = []
    for _ in range(NUM_EDITORAS):
        cursor.execute("INSERT INTO Editora (nome) VALUES (%s) RETURNING id_editora",
                      (fake.company() + " Editora",))
        editoras_ids.append(cursor.fetchone()[0])


    # 2. Popular Autor
    print("Populando Autor...")
    nacionalidades = ['Brasileira', 'Americana', 'Britânica', 'Francesa', 'Japonesa']
    autores_ids = []
    for _ in range(NUM_AUTORES):
        cursor.execute("INSERT INTO Autor (nome, nacionalidade) VALUES (%s, %s) RETURNING id_autor",
                      (fake.name(), random.choice(nacionalidades)))
        autores_ids.append(cursor.fetchone()[0])


    # 3. Popular Livro
    print("Populando Livro...")
    livros_isbn = []
    for _ in range(NUM_LIVROS):
        isbn = fake.isbn13()
        try:
            cursor.execute("""
                INSERT INTO Livro (ISBN, id_editora, data_publicacao, edicao, genero, titulo)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    isbn,
                    random.choice(editoras_ids),
                    fake.date_between(start_date='-30y', end_date='today'),
                    random.randint(1, 10),
                    random.choice(generos),
                    fake.sentence(nb_words=4)
                ))
            livros_isbn.append(isbn)
        except psycopg2.IntegrityError:
            conn.rollback()
            continue

    # 4. Popular Escrito_por
    print("Populando Escrito_por...")
    for isbn in livros_isbn:
        num_autores = random.randint(1, min(4, len(autores_ids)))
        autores_para_livro = random.sample(autores_ids, num_autores)
        for autor_id in autores_para_livro:
            cursor.execute("""
                INSERT INTO Escrito_por (ISBN, id_autor)
                VALUES (%s, %s)
                """, (isbn, autor_id))

    # 5. Popular Endereco
    print("Populando Endereco...")
    enderecos_ids = []
    for _ in range(NUM_ENDERECOS):
        cursor.execute("""
            INSERT INTO Endereco (nome_bairro, nome_rua)
            VALUES (%s, %s) RETURNING id_endereco
            """,
            (fake.bairro(), fake.street_name()))
        enderecos_ids.append(cursor.fetchone()[0])


    # 6. Popular Usuario
    print("Populando Usuario...")
    usuarios_ids = []
    for _ in range(NUM_USUARIOS):
        cursor.execute("""
            INSERT INTO Usuario (id_endereco, nome, email, telefone)
            VALUES (%s, %s, %s, %s) RETURNING id_usuario
            """,
            (
                random.choice(enderecos_ids),
                fake.name(),
                fake.email(),
                fake.phone_number()[:13]
            ))
        usuarios_ids.append(cursor.fetchone()[0])


    # 7. Popular Funcionario
    print("Populando Funcionario...")
    cargos = ['Bibliotecário', 'Assistente', 'Gerente', 'Atendente']
    funcionarios_ids = []
    for _ in range(NUM_FUNCIONARIOS):
        cursor.execute("""
            INSERT INTO Funcionario (id_endereco, email, nome, cargo)
            VALUES (%s, %s, %s, %s) RETURNING id_funcionario
            """,
            (
                random.choice(enderecos_ids),
                fake.email(),
                fake.name(),
                random.choice(cargos)
            ))
        funcionarios_ids.append(cursor.fetchone()[0])


    # 8. Popular Exemplar
    print("Populando Exemplar...")
    exemplares_ids = []
    for _ in range(NUM_EXEMPLARES):
        cursor.execute("""
            INSERT INTO Exemplar (ISBN, status, localizacao)
            VALUES (%s, %s, %s) RETURNING id_exemplar
            """,
            (
                random.choice(livros_isbn),
                random.choice(status_exemplar),
                f"Prateleira {random.randint(1, 50)}, Seção {random.choice(['A', 'B', 'C'])}"
            ))
        exemplares_ids.append(cursor.fetchone()[0])


    #9. Popular Reserva
    print("Populando Reserva...")
    for _ in range(NUM_RESERVAS):
        try:
            data_reserva = fake.date_between(start_date='-1y', end_date='today')
            cursor.execute("""
                INSERT INTO Reserva (ISBN, id_usuario, id_funcionario, data_reserva, status) 
                VALUES (%s, %s, %s, %s, %s)
                """, 
                (
                    random.choice(livros_isbn),
                    random.choice(usuarios_ids),
                    random.choice(funcionarios_ids),
                    data_reserva,
                    random.choice(status_reserva)
                ))
        except psycopg2.IntegrityError:
            conn.rollback()
            continue

    # 10. Popular Emprestimo
    print("Populando Emprestimo...")
    exemplares_disponiveis = list(exemplares_ids)
    random.shuffle(exemplares_disponiveis) 
    emprestimos_atrasados_ids = []

    for i in range(min(NUM_EMPRESTIMOS, len(exemplares_disponiveis))):
        exemplar_id = exemplares_disponiveis.pop() # Pega e remove um exemplar da lista de disponíveis

        data_emprestimo = fake.date_between(start_date='-1y', end_date='today')
        data_devolucao_prev = data_emprestimo + timedelta(days=14)
        data_devolucao = None
        status = 'ATIVO'

        if random.random() > 0.3: # 70% de chance de já ter sido devolvido
            data_devolucao = fake.date_between(start_date=data_emprestimo, end_date=data_devolucao_prev + timedelta(days=10))
            status = 'DEVOLVIDO'
            if data_devolucao > data_devolucao_prev:
                status = 'ATRASADO'

        cursor.execute("""
            INSERT INTO Emprestimo (
                id_exemplar, id_usuario, id_funcionario,
                data_emprestimo, data_devolucao_prev, data_devolucao, status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id_emprestimo
            """,
            (
                exemplar_id,
                random.choice(usuarios_ids),
                random.choice(funcionarios_ids),
                data_emprestimo,
                data_devolucao_prev,
                data_devolucao,
                status
            ))
        
        if status == 'ATRASADO':
            emprestimos_atrasados_ids.append(cursor.fetchone()[0])


    # 11. Popular PagamentoMulta
    print("Populando PagamentoMulta...")
    num_pagamentos = min(NUM_PAGAMENTOS, len(emprestimos_atrasados_ids))
    random.shuffle(emprestimos_atrasados_ids)

    for i in range(num_pagamentos):
        emprestimo_id = emprestimos_atrasados_ids[i]
        valor_pago = round(random.uniform(5.0, 50.0), 2)
        data_pagamento = fake.date_between(start_date='-1y', end_date='today')

        cursor.execute("""
            INSERT INTO PagamentoMulta (id_emprestimo, valor_pago, data_pagamento)
            VALUES (%s, %s, %s)
            """,
            (emprestimo_id, valor_pago, data_pagamento))

    print("Banco de dados populado com sucesso!")

    # --- Trecho para garantir a existência do livro de teste ---

    target_isbn = '978-0-345-39180-3'

    cursor.execute("SELECT COUNT(*) FROM Livro WHERE ISBN = %s", (target_isbn,))
    count = cursor.fetchone()[0]

    if count == 0:
        print(f"Livro com ISBN {target_isbn} não encontrado. Inserindo registro de teste...")
        try:
            id_editora_valido = editoras_ids[0]
            dados_livro_teste = (
                target_isbn,
                id_editora_valido,
                '1977-04-12',
                1,
                'Ficção Científica',
                'O Guia do Mochileiro das Galáxias'
            )

            cursor.execute("""
                INSERT INTO Livro (ISBN, id_editora, data_publicacao, edicao, genero, titulo)
                VALUES (%s, %s, %s, %s, %s, %s)
                """, dados_livro_teste)
            
        except IndexError:
            print("ERRO: Não foi possível inserir o livro de teste porque nenhuma editora foi criada.")
        except Exception as e:
            print(f"Ocorreu um erro ao inserir o livro de teste: {e}")

    else:
        print(f"Livro com ISBN {target_isbn} já existe no banco. Nenhuma ação necessária.")

    # --- Fim do trecho para garantir a existência do livro de teste ---

    conn.commit()

except Exception as e:
    print(f"Erro: {e}")
    conn.rollback()

finally:
    if conn:
        cursor.close()
        conn.close()