from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from backend.app.database import Base

class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(Integer, primary_key=True, index=True)
    id_endereco = Column(Integer, ForeignKey("endereco.id_endereco"), nullable=True)
    nome = Column(String(50), nullable=False)
    email = Column(String(50), unique=True)
    telefone = Column(String(13))

    # Relação com Endereco
    endereco = relationship("Endereco", back_populates="usuarios")

    # Relações com Emprestimo e Reserva
    emprestimos = relationship("Emprestimo", back_populates="usuario")
    reservas = relationship("Reserva", back_populates="usuario")

    def __repr__(self):
        return f"<Usuario(id={self.id_usuario}, nome='{self.nome}', email='{self.email}')>"