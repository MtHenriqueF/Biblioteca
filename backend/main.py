from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
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