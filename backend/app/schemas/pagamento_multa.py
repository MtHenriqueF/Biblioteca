from pydantic import BaseModel
from typing import Optional
from datetime import date
from decimal import Decimal
from backend.app.schemas import emprestimo as schemas_emprestimo

class PagamentoMultaBase(BaseModel):
    id_emprestimo: Optional[int] = None
    valor_pago: Optional[Decimal] = None 
    data_pagamento: Optional[date] = None

class PagamentoMultaCreate(PagamentoMultaBase):
    pass

class PagamentoMulta(PagamentoMultaBase):
    id_pagamento: int
    emprestimo: Optional[schemas_emprestimo.Emprestimo] = None

    class Config:
        from_attributes = True