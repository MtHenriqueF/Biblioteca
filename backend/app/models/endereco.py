from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.app.database import Base

class Endereco(Base):
    __tablename__ = "endereco"

    id_endereco = Column(Integer, primary_key=True, index=True)
    nome_bairro = Column(String(255), nullable=False)
    nome_rua = Column(String(255), nullable=False)

    # Relações com Usuario e Funcionario
    usuarios = relationship("Usuario", back_populates="endereco")
    funcionarios = relationship("Funcionario", back_populates="endereco")

    def __repr__(self):
        return f"<Endereco(id={self.id_endereco}, bairro='{self.nome_bairro}', rua='{self.nome_rua}')>"