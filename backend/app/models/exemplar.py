from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database import Base

class Exemplar(Base):
    __tablename__ = "exemplar"

    id_exemplar = Column(Integer, primary_key=True, index=True)
    ISBN = Column(String(17), ForeignKey("livro.ISBN"))
    status = Column(String(20), nullable=False) # Ex: 'LIVRE', 'RESERVADO', 'EM MANUTENCAO'
    localizacao = Column(Text)

    # Relação com Livro (um exemplar pertence a um livro)
    livro = relationship("Livro", back_populates="exemplares")

    # Relação com Emprestimo (um exemplar pode estar em muitos empréstimos)
    emprestimos = relationship("Emprestimo", back_populates="exemplar")

    def __repr__(self):
        return f"<Exemplar(id={self.id_exemplar}, ISBN='{self.ISBN}', status='{self.status}')>"