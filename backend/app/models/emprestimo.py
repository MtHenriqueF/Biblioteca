from sqlalchemy import Column, Integer, String, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from backend.app.database import Base

class Emprestimo(Base):
    __tablename__ = "emprestimo"

    id_emprestimo = Column(Integer, primary_key=True, index=True)
    id_exemplar = Column(Integer, ForeignKey("exemplar.id_exemplar"), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    id_funcionario = Column(Integer, ForeignKey("funcionario.id_funcionario"), nullable=False)
    data_emprestimo = Column(Date, nullable=False)
    data_devolucao_prev = Column(Date)
    data_devolucao = Column(Date)
    status = Column(String(20), nullable=False) # Ex: 'ATIVO', 'DEVOLVIDO', 'ATRASADO'

    # Relacionamentos
    exemplar = relationship("Exemplar", back_populates="emprestimos")
    usuario = relationship("Usuario", back_populates="emprestimos")
    funcionario = relationship("Funcionario", back_populates="emprestimos")
    pagamento_multa = relationship("PagamentoMulta", back_populates="emprestimo", uselist=False) # uselist=False para 1:1

    # Restrição UNIQUE do DDL: CONSTRAINT uk_emprestimo_tripla UNIQUE (id_funcionario, id_usuario, id_exemplar)
    __table_args__ = (UniqueConstraint('id_funcionario', 'id_usuario', 'id_exemplar', name='uk_emprestimo_tripla'),)

    def __repr__(self):
        return f"<Emprestimo(id={self.id_emprestimo}, exemplar_id={self.id_exemplar}, user_id={self.id_usuario})>"