from sqlalchemy import Column, Integer, DECIMAL, Date, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database import Base

class PagamentoMulta(Base):
    __tablename__ = "pagamento_multa"

    id_pagamento = Column(Integer, primary_key=True, index=True)
    id_emprestimo = Column(Integer, ForeignKey("emprestimo.id_emprestimo"), unique=True)
    valor_pago = Column(DECIMAL(10, 2))
    data_pagamento = Column(Date)

    # Relação com Emprestimo (um pagamento de multa pertence a um empréstimo)
    emprestimo = relationship("Emprestimo", back_populates="pagamento_multa")

    def __repr__(self):
        return f"<PagamentoMulta(id={self.id_pagamento}, emprestimo_id={self.id_emprestimo}, valor={self.valor_pago})>"