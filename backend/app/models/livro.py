from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database import Base

class Livro(Base):
    __tablename__ = "livro"

    ISBN = Column(String(17), primary_key=True, index=True)
    id_editora = Column(Integer, ForeignKey("editora.id_editora"), nullable=False)
    data_publicacao = Column(Date, nullable=False)
    edicao = Column(Integer)
    genero = Column(String(50))
    titulo = Column(Text, nullable=False)

    # Relação com Editora (um livro pertence a uma editora)
    editora = relationship("Editora", back_populates="livros")

    # Relação muitos-para-muitos com Autor através de Escrito_por
    escrito_por_rel = relationship("Escrito_por", back_populates="livro")
    autores = relationship("Autor", secondary="escrito_por", back_populates="livros")

    # Relação com Exemplar (um livro pode ter muitos exemplares)
    exemplares = relationship("Exemplar", back_populates="livro")

    # Relação com Reserva (um livro pode ter muitas reservas)
    reservas = relationship("Reserva", back_populates="livro")

    def __repr__(self):
        return f"<Livro(ISBN='{self.ISBN}', titulo='{self.titulo}')>"