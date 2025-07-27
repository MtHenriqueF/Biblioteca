from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database import Base

class Funcionario(Base):
    __tablename__ = "funcionario"

    id_funcionario = Column(Integer, primary_key=True, index=True)
    id_endereco = Column(Integer, ForeignKey("endereco.id_endereco"), nullable=True)
    email = Column(String(35), unique=True)
    nome = Column(String(50))
    cargo = Column(String(20))

    # Relação com Endereco
    endereco = relationship("Endereco", back_populates="funcionarios")

    # Relações com Emprestimo e Reserva
    emprestimos = relationship("Emprestimo", back_populates="funcionario")
    reservas = relationship("Reserva", back_populates="funcionario")

    def __repr__(self):
        return f"<Funcionario(id={self.id_funcionario}, nome='{self.nome}', cargo='{self.cargo}')>"