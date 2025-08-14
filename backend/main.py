from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload, contains_eager
from typing import List

from backend.app.database import engine, Base, get_db
from backend.app import models
from backend.app import schemas

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao Bibliotech Analytics & Management Backend!"}


@app.get("/api/editoras/", response_model=List[schemas.editora.Editora])
def read_editoras(db: Session = Depends(get_db)):
    editoras = db.query(models.editora.Editora).all()
    return editoras

@app.post("/api/editoras/", response_model=schemas.editora.Editora)
def create_editora(editora_data: schemas.editora.EditoraCreate, db: Session = Depends(get_db)):
    db_editora = models.editora.Editora(nome=editora_data.nome)
    db.add(db_editora)
    db.commit()
    db.refresh(db_editora)
    return db_editora

@app.post("/api/enderecos/", response_model=schemas.endereco.Endereco)
def create_endereco(endereco_data: schemas.endereco.EnderecoCreate, db: Session = Depends(get_db)):
    db_endereco = models.endereco.Endereco(**endereco_data.model_dump())
    db.add(db_endereco)
    db.commit()
    db.refresh(db_endereco)
    return db_endereco


@app.get("/api/enderecos/", response_model=List[schemas.endereco.Endereco])
def read_enderecos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    enderecos = db.query(models.endereco.Endereco).offset(skip).limit(limit).all()
    return enderecos


@app.post("/api/usuarios/", response_model=schemas.usuario.Usuario)
def create_usuario(usuario_data: schemas.usuario.UsuarioCreate, db: Session = Depends(get_db)):

    endereco_data = usuario_data.endereco
    db_endereco = models.endereco.Endereco(**endereco_data.model_dump())

    #cria o objeto Usuario, sem os dados do endereço
    #O Pydantic nos ajuda a extrair apenas os dados do usuário
    usuario_dict = usuario_data.model_dump(exclude={'endereco'})
    db_usuario = models.usuario.Usuario(**usuario_dict)

    #ASSOCIA o endereço ao usuário.
    #SQLAlchemy é inteligente o suficiente para saber que isso preencherá a FK 'id_endereco'.
    db_usuario.endereco = db_endereco
    
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    
    return db_usuario


@app.get("/api/usuarios/", response_model=List[schemas.usuario.Usuario])
def read_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    usuarios = (
        db.query(models.usuario.Usuario)
        .options(joinedload(models.usuario.Usuario.endereco)) # Carrega o endereço junto para otimizar
        .offset(skip)
        .limit(limit)
        .all()
    )
    return usuarios


@app.get("/api/autores/", response_model=List[schemas.autor.Autor])
def read_autores(db: Session = Depends(get_db)):
    autores = db.query(models.autor.Autor).all()
    return autores

@app.post("/api/autores/", response_model=schemas.autor.Autor)
def create_autor(autor_data: schemas.autor.AutorCreate, db: Session = Depends(get_db)):
    db_autor = models.autor.Autor(**autor_data.model_dump())
    db.add(db_autor)
    db.commit()
    db.refresh(db_autor)
    return db_autor


@app.post("/api/livros/", response_model=schemas.livro.Livro)
def create_livro(livro_data: schemas.livro.LivroCreate, db: Session = Depends(get_db)):
    db_editora = db.query(models.editora.Editora).filter(models.editora.Editora.id_editora == livro_data.id_editora).first()
    if not db_editora:
        raise HTTPException(status_code=404, detail=f"Editora com id {livro_data.id_editora} não encontrada.")
    
    db_autores = db.query(models.autor.Autor).filter(models.autor.Autor.id_autor.in_(livro_data.autores_ids)).all()
    if not livro_data.autores_ids or len(db_autores) != len(livro_data.autores_ids):
        ids_encontrados = {autor.id_autor for autor in db_autores}
        ids_faltando = set(livro_data.autores_ids or []) - ids_encontrados
        raise HTTPException(status_code=404, detail=f"Autores com os seguintes IDs não encontrados: {list(ids_faltando)}")

    db_livro = models.livro.Livro(**livro_data.model_dump(exclude={"autores_ids"}))
    
    db_livro.autores = db_autores

    db.add(db_livro)
    db.commit()
    db.refresh(db_livro)
    
    return db_livro

@app.get("/api/livros/", response_model=List[schemas.livro.Livro])
def read_livros(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    livros = (
        db.query(models.livro.Livro)
        .options(joinedload(models.livro.Livro.editora), joinedload(models.livro.Livro.autores))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return livros

# @app.get("/api/livros/{isbn}", response_model=schemas.livro.Livro)
# def read_livro_by_isbn(isbn: str, db: Session = Depends(get_db)):
#     db_livro = (
#         db.query(models.livro.Livro)
#         .options(joinedload(models.livro.Livro.editora), joinedload(models.livro.Livro.autores))
#         .filter(models.livro.Livro.ISBN == isbn)
#         .first()
#     )
#     if db_livro is None:
#         raise HTTPException(status_code=404, detail="Livro não encontrado")
#     return db_livro


@app.post("/api/reservas/", response_model=schemas.reserva.Reserva)
def create_reserva(reserva_data: schemas.reserva.ReservaCreate, db: Session = Depends(get_db)):

    #Valida se as entidades referenciadas (livro, usuário, funcionário) existem
    db_livro = db.query(models.livro.Livro).filter(models.livro.Livro.ISBN == reserva_data.ISBN).first()
    if not db_livro:
        raise HTTPException(status_code=404, detail=f"Livro com ISBN {reserva_data.ISBN} não encontrado.")

    db_usuario = db.query(models.usuario.Usuario).filter(models.usuario.Usuario.id_usuario == reserva_data.id_usuario).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail=f"Usuário com ID {reserva_data.id_usuario} não encontrado.")

    db_funcionario = db.query(models.funcionario.Funcionario).filter(models.funcionario.Funcionario.id_funcionario == reserva_data.id_funcionario).first()
    if not db_funcionario:
        raise HTTPException(status_code=404, detail=f"Funcionário com ID {reserva_data.id_funcionario} não encontrado.")

    #Cria a instância do objeto Reserva com os dados fornecidos e calculados
    db_reserva = models.reserva.Reserva(
        ISBN=reserva_data.ISBN,
        id_usuario=reserva_data.id_usuario,
        id_funcionario=reserva_data.id_funcionario,
        data_reserva=date.today(),
        status='ATIVA'  #status inicial padrão
    )

    db.add(db_reserva)
    db.commit()
    db.refresh(db_reserva)
    
    return db_reserva


@app.get("/api/reservas/", response_model=List[schemas.reserva.Reserva])
def read_reservas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    reservas = (
        db.query(models.reserva.Reserva)
        .options(
            joinedload(models.reserva.Reserva.livro),
            joinedload(models.reserva.Reserva.usuario),
            joinedload(models.reserva.Reserva.funcionario)
        )
        .order_by(models.reserva.Reserva.data_reserva.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return reservas


from datetime import date, timedelta
from sqlalchemy.exc import IntegrityError


@app.post("/api/exemplares/", response_model=schemas.exemplar.Exemplar)
def create_exemplar(exemplar_data: schemas.exemplar.ExemplarCreate, db: Session = Depends(get_db)):
    db_livro = db.query(models.livro.Livro).filter(models.livro.Livro.ISBN == exemplar_data.ISBN).first()
    if not db_livro:
        raise HTTPException(status_code=404, detail=f"Livro com ISBN {exemplar_data.ISBN} não encontrado para criar um exemplar.")
    
    db_exemplar = models.exemplar.Exemplar(**exemplar_data.model_dump())
    db.add(db_exemplar)
    db.commit()
    db.refresh(db_exemplar)
    return db_exemplar

@app.get("/api/exemplares/", response_model=List[schemas.exemplar.Exemplar])
def read_exemplares(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    exemplares = db.query(models.exemplar.Exemplar).options(joinedload(models.exemplar.Exemplar.livro)).offset(skip).limit(limit).all()
    return exemplares


@app.post("/api/emprestimos/", response_model=schemas.emprestimo.Emprestimo)
def create_emprestimo(emprestimo_data: schemas.emprestimo.EmprestimoCreate, db: Session = Depends(get_db)):
    db_exemplar = db.query(models.exemplar.Exemplar).filter(models.exemplar.Exemplar.id_exemplar == emprestimo_data.id_exemplar).first()
    if not db_exemplar:
        raise HTTPException(status_code=404, detail="Exemplar não encontrado")

    if db_exemplar.status != 'LIVRE':
        raise HTTPException(status_code=400, detail=f"Exemplar ID {db_exemplar.id_exemplar} não está disponível. Status atual: {db_exemplar.status}")

    db_usuario = db.query(models.usuario.Usuario).filter(models.usuario.Usuario.id_usuario == emprestimo_data.id_usuario).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    db_funcionario = db.query(models.funcionario.Funcionario).filter(models.funcionario.Funcionario.id_funcionario == emprestimo_data.id_funcionario).first()
    if not db_funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")

    db_exemplar.status = 'EMPRESTADO'
    
    data_hoje = date.today()
    data_prevista = data_hoje + timedelta(days=14)

    db_emprestimo = models.emprestimo.Emprestimo(
        id_exemplar=emprestimo_data.id_exemplar,
        id_usuario=emprestimo_data.id_usuario,
        id_funcionario=emprestimo_data.id_funcionario,
        data_emprestimo=data_hoje,
        data_devolucao_prev=data_prevista,
        status='ATIVO'
    )
    
    db.add(db_emprestimo)
    db.add(db_exemplar)
    db.commit()
    db.refresh(db_emprestimo)
    return db_emprestimo

@app.get("/api/emprestimos/", response_model=List[schemas.emprestimo.Emprestimo])
def read_emprestimos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    emprestimos = db.query(models.emprestimo.Emprestimo).options(
        joinedload(models.emprestimo.Emprestimo.usuario),
        joinedload(models.emprestimo.Emprestimo.funcionario),
        joinedload(models.emprestimo.Emprestimo.exemplar).joinedload(models.exemplar.Exemplar.livro)
    ).order_by(models.emprestimo.Emprestimo.data_emprestimo.desc()).offset(skip).limit(limit).all()
    return emprestimos


@app.post("/api/pagamentos_multa/", response_model=schemas.pagamento_multa.PagamentoMulta)
def create_pagamento_multa(pagamento_data: schemas.pagamento_multa.PagamentoMultaCreate, db: Session = Depends(get_db)):
    db_emprestimo = db.query(models.emprestimo.Emprestimo).filter(models.emprestimo.Emprestimo.id_emprestimo == pagamento_data.id_emprestimo).first()
    if not db_emprestimo:
        raise HTTPException(status_code=404, detail=f"Empréstimo com ID {pagamento_data.id_emprestimo} não encontrado.")

    if db_emprestimo.status != 'ATRASADO':
        raise HTTPException(status_code=400, detail=f"O pagamento de multa só pode ser efetuado para empréstimos com status 'ATRASADO'. Status atual: '{db_emprestimo.status}'.")

    db_pagamento = models.pagamento_multa.PagamentoMulta(
        id_emprestimo=pagamento_data.id_emprestimo,
        valor_pago=pagamento_data.valor_pago,
        data_pagamento=date.today()
    )
    
    try:
        db.add(db_pagamento)
        db.commit()
        db.refresh(db_pagamento)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=f"Já existe um pagamento de multa registrado para o empréstimo ID {pagamento_data.id_emprestimo}.")
        
    return db_pagamento

@app.get("/api/pagamentos_multa/", response_model=List[schemas.pagamento_multa.PagamentoMulta])
def read_pagamentos_multa(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pagamentos = db.query(models.pagamento_multa.PagamentoMulta).options(
        joinedload(models.pagamento_multa.PagamentoMulta.emprestimo)
    ).order_by(models.pagamento_multa.PagamentoMulta.data_pagamento.desc()).offset(skip).limit(limit).all()
    return pagamentos


###### PUT E DELETE

def update_db_object(db_obj, update_data):
    """Atualiza um objeto do banco de dados com dados de um schema Pydantic."""
    for var, value in update_data.model_dump(exclude_unset=True).items():
        setattr(db_obj, var, value)
    return db_obj

@app.put("/api/autores/{autor_id}", response_model=schemas.autor.Autor)
def update_autor(autor_id: int, autor_data: schemas.autor.AutorUpdate, db: Session = Depends(get_db)):
    db_autor = db.query(models.autor.Autor).filter(models.autor.Autor.id_autor == autor_id).first()
    if not db_autor:
        raise HTTPException(status_code=404, detail="Autor não encontrado")
    
    db_autor = update_db_object(db_autor, autor_data)
    db.commit()
    db.refresh(db_autor)
    return db_autor

@app.delete("/api/autores/{autor_id}", status_code=200)
def delete_autor(autor_id: int, db: Session = Depends(get_db)):
    db_autor = db.query(models.autor.Autor).filter(models.autor.Autor.id_autor == autor_id).first()
    if not db_autor:
        raise HTTPException(status_code=404, detail="Autor não encontrado")
    
    # REGRA DE NEGÓCIO: Não deletar autor se ele tiver livros associados.
    if db_autor.livros:
        raise HTTPException(status_code=409, detail="Não é possível deletar autor, pois ele possui livros cadastrados.")
        
    db.delete(db_autor)
    db.commit()
    return {"detail": "Autor deletado com sucesso"}

@app.put("/api/editoras/{editora_id}", response_model=schemas.editora.Editora)
def update_editora(editora_id: int, editora_data: schemas.editora.EditoraUpdate, db: Session = Depends(get_db)):
    db_editora = db.query(models.editora.Editora).filter(models.editora.Editora.id_editora == editora_id).first()
    if not db_editora:
        raise HTTPException(status_code=404, detail="Editora não encontrada")

    db_editora = update_db_object(db_editora, editora_data)
    db.commit()
    db.refresh(db_editora)
    return db_editora

@app.delete("/api/editoras/{editora_id}", status_code=200)
def delete_editora(editora_id: int, db: Session = Depends(get_db)):
    db_editora = db.query(models.editora.Editora).filter(models.editora.Editora.id_editora == editora_id).first()
    if not db_editora:
        raise HTTPException(status_code=404, detail="Editora não encontrada")

    # REGRA DE NEGÓCIO: Não deletar editora se ela tiver livros associados.
    if db_editora.livros:
        raise HTTPException(status_code=409, detail="Não é possível deletar editora, pois ela possui livros cadastrados.")

    db.delete(db_editora)
    db.commit()
    return {"detail": "Editora deletada com sucesso"}

@app.put("/api/usuarios/{usuario_id}", response_model=schemas.usuario.Usuario)
def update_usuario(usuario_id: int, usuario_data: schemas.usuario.UsuarioUpdate, db: Session = Depends(get_db)):
    db_usuario = db.query(models.usuario.Usuario).filter(models.usuario.Usuario.id_usuario == usuario_id).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    db_usuario = update_db_object(db_usuario, usuario_data)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@app.delete("/api/usuarios/{usuario_id}", status_code=200)
def delete_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = db.query(models.usuario.Usuario).filter(models.usuario.Usuario.id_usuario == usuario_id).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # REGRA DE NEGÓCIO: Não deletar usuário se ele tiver histórico de empréstimos ou reservas.
    if db_usuario.emprestimos or db_usuario.reservas:
        raise HTTPException(status_code=409, detail="Não é possível deletar usuário, pois ele possui histórico de empréstimos ou reservas.")

    db.delete(db_usuario)
    db.commit()
    return {"detail": "Usuário deletado com sucesso"}

@app.put("/api/livros/{isbn}", response_model=schemas.livro.Livro)
def update_livro(isbn: str, livro_data: schemas.livro.LivroUpdate, db: Session = Depends(get_db)):
    db_livro = db.query(models.livro.Livro).filter(models.livro.Livro.ISBN == isbn).first()
    if not db_livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    db_livro = update_db_object(db_livro, livro_data)
    db.commit()
    db.refresh(db_livro)
    return db_livro

# NOTA: Não implementamos DELETE para Livro, pois ele é central para o histórico.
# A deleção é bloqueada pela FK em Exemplar, Reserva e Escrito_por.
# Uma alternativa seria um status 'INATIVO' no modelo Livro.

@app.put("/api/emprestimos/{emprestimo_id}/devolver", response_model=schemas.emprestimo.Emprestimo)
def devolver_livro(emprestimo_id: int, db: Session = Depends(get_db)):
    db_emprestimo = db.query(models.emprestimo.Emprestimo).filter(models.emprestimo.Emprestimo.id_emprestimo == emprestimo_id).first()
    if not db_emprestimo:
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado")

    if db_emprestimo.status != 'ATIVO' and db_emprestimo.status != 'ATRASADO':
        raise HTTPException(status_code=400, detail=f"Este empréstimo não pode ser devolvido. Status atual: {db_emprestimo.status}")

    # Atualiza o status do empréstimo
    db_emprestimo.data_devolucao = date.today()
    db_emprestimo.status = 'DEVOLVIDO'

    # Libera o exemplar para um novo empréstimo
    db_emprestimo.exemplar.status = 'LIVRE'
    
    db.commit()
    db.refresh(db_emprestimo)
    return db_emprestimo
