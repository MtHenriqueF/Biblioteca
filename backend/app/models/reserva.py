from sqlalchemy import Column, Integer, String, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from backend.app.database import Base

class Reserva(Base):
    __tablename__ = "reserva"

    id_reserva = Column(Integer, primary_key=True, index=True)
    ISBN = Column(String(17), ForeignKey("livro.ISBN"), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    id_funcionario = Column(Integer, ForeignKey("funcionario.id_funcionario"), nullable=False)
    data_reserva = Column(Date)
    status = Column(String(20)) # Ex: 'ATIVA', 'CANCELADA', 'CONCLUIDA'

    # Relacionamentos
    livro = relationship("Livro", back_populates="reservas")
    usuario = relationship("Usuario", back_populates="reservas")
    funcionario = relationship("Funcionario", back_populates="reservas")

    # Restrição UNIQUE do DDL: CONSTRAINT uk_reserva_tripla UNIQUE (id_funcionario, id_usuario, ISBN)
    __table_args__ = (UniqueConstraint('id_funcionario', 'id_usuario', 'ISBN', name='uk_reserva_tripla'),)

    def __repr__(self):
        return f"<Reserva(id={self.id_reserva}, ISBN='{self.ISBN}', user_id={self.id_usuario})>"