from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.app.database import Base

class Editora(Base):
    __tablename__ = "editora"

    id_editora = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)

    # Relação com Livro (uma editora pode ter muitos livros)
    livros = relationship("Livro", back_populates="editora")

    def __repr__(self):
        return f"<Editora(id={self.id_editora}, nome='{self.nome}')>"