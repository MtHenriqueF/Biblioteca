from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import engine, Base, get_db
from backend.app.models import editora

# Cria todas as tabelas (apenas se elas não existirem)
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao Bibliotech Analytics & Management Backend!"}

# Endpoint para listar editoras
@app.get("/api/editoras/")
def read_editoras(db: Session = Depends(get_db)):
    editoras = db.query(editora.Editora).all()
    return editoras

# Endpoint para adicionar uma editora
@app.post("/api/editoras/")
def create_editora(nome: str, db: Session = Depends(get_db)):
    db_editora = editora.Editora(nome=nome)
    db.add(db_editora)
    db.commit()
    db.refresh(db_editora)
    return db_editora