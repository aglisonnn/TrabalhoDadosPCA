# Resumo da Preparacao dos Dados

## Dataset de entrada

- Arquivo: `online+retail/Online Retail.xlsx`
- Registros originais: 541,909
- Colunas originais: 8

## Limpeza aplicada

- Remocao de registros sem identificacao de cliente ou campos essenciais.
- Remocao de faturas canceladas, identificadas por `InvoiceNo` iniciado com `C`.
- Remocao de registros com `Quantity <= 0`.
- Remocao de registros com `UnitPrice <= 0`.
- Criacao da coluna `TotalPrice = Quantity * UnitPrice`.

## Resultado da limpeza

- Registros validos apos limpeza: 397,884
- Registros removidos: 144,025
- Clientes analisados: 4,338
- Periodo considerado: 2010-12-01 08:26:00 ate 2011-12-09 12:50:00

## Features criadas por cliente

- `TotalQuantity`: quantidade total de itens comprados.
- `TotalSpent`: valor total gasto.
- `Frequency`: quantidade de faturas distintas.
- `AvgTicket`: valor medio gasto por fatura.
- `UniqueProducts`: quantidade de produtos diferentes comprados.
- `AvgUnitPrice`: preco medio dos produtos comprados.
- `Recency`: quantidade de dias desde a ultima compra.

## Arquivos gerados

- `dados_processados/transacoes_limpas.csv`
- `dados_processados/features_clientes.csv`
- `dados_processados/features_clientes_padronizadas.csv`
