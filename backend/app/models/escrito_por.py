from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database import Base

class Escrito_por(Base):
    __tablename__ = "escrito_por"

    id_escritura = Column(Integer, primary_key=True, index=True)
    ISBN = Column(String(17), ForeignKey("livro.ISBN"), nullable=False)
    id_autor = Column(Integer, ForeignKey("autor.id_autor"), nullable=False)

    # Relações com Livro e Autor
    livro = relationship("Livro", back_populates="escrito_por_rel")
    autor = relationship("Autor", back_populates="escrito_por_rel")

    def __repr__(self):
        return f"<Escrito_por(id={self.id_escritura}, ISBN='{self.ISBN}', id_autor={self.id_autor})>"