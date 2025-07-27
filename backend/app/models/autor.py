from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from backend.app.database import Base

class Autor(Base):
    __tablename__ = "autor"

    id_autor = Column(Integer, primary_key=True, index=True)
    nome = Column(Text, nullable=False)
    nacionalidade = Column(String(20))

    # Relação muitos-para-muitos com Livro através de Escrito_por
    escrito_por_rel = relationship("Escrito_por", back_populates="autor")
    livros = relationship("Livro", secondary="escrito_por", back_populates="autores")

    def __repr__(self):
        return f"<Autor(id={self.id_autor}, nome='{self.nome}')>"