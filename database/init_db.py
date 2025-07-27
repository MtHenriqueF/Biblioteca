import psycopg2
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='backend/.env')
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL não configurada no .env")

DDL_SCRIPT_PATH = "database/setup_scripts/ddl_script.sql"
# DDL_SCRIPT_PATH = "database/setup_scripts/drop_script"


def init_db():
    conn = None
    cursor = None
    try:

        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        with open(DDL_SCRIPT_PATH, 'r') as f:
            sql_script = f.read()

        cursor.execute(sql_script)
        conn.commit()
        print(f"Banco de dados inicializado com sucesso usando {DDL_SCRIPT_PATH}!")

    except psycopg2.Error as e:
        print(f"Erro ao conectar ou inicializar o banco de dados: {e}")
        if conn:
            conn.rollback() # Reverte qualquer transação em caso de erro
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    print("Tentando inicializar o banco de dados no Render...")
    init_db()