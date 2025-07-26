DELETE FROM PagamentoMulta
WHERE data_pagamento < CURRENT_DATE - INTERVAL '5 years';