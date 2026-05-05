# PCA e MDS no Dataset Online Retail

## Explicação Teórica do PCA

A Análise de Componentes Principais, ou PCA, é uma técnica estatística utilizada para reduzir a dimensionalidade de um conjunto de dados numéricos. A ideia principal do PCA é transformar um conjunto de variáveis possivelmente correlacionadas em um novo conjunto de variáveis chamadas componentes principais.

Esses componentes são combinações lineares das variáveis originais. O primeiro componente principal concentra a maior parte possível da variabilidade dos dados; o segundo componente explica a maior parte da variabilidade restante, sendo independente do primeiro; e assim sucessivamente.

No contexto da análise exploratória, o PCA permite representar dados multidimensionais em duas ou três dimensões, facilitando a visualização de padrões, agrupamentos, tendências e possíveis outliers. Além disso, o PCA ajuda a identificar quais variáveis mais contribuem para a separação dos registros, permitindo compreender melhor a estrutura do dataset.

Como o PCA é sensível à escala das variáveis, é necessário padronizar os dados antes da aplicação. Isso evita que variáveis com valores maiores, como faturamento total, dominem variáveis menores, como quantidade média de produtos.

## Explicação Teórica do MDS

O MDS, ou Escalonamento Multidimensional, é uma técnica de redução de dimensionalidade baseada nas distâncias ou dissimilaridades entre os registros. Diferente do PCA, que busca maximizar a variância explicada por combinações lineares das variáveis, o MDS tenta posicionar os registros em um espaço de menor dimensão preservando, tanto quanto possível, as distâncias observadas no espaço original.

Na prática, se dois registros são parecidos no conjunto original de variáveis, eles devem aparecer próximos no gráfico gerado pelo MDS. Se forem muito diferentes, devem aparecer distantes. Por isso, o MDS é bastante útil para visualizar proximidades, agrupamentos e outliers.

No caso deste trabalho, o MDS será utilizado para observar se clientes ou compras com comportamentos semelhantes aparecem próximos no gráfico bidimensional. Isso pode ajudar a identificar perfis de consumo, clientes com alto valor de compra, registros atípicos ou grupos com padrões semelhantes de compra.

## Descrição do Dataset Utilizado

O dataset escolhido foi o **Online Retail**, disponível no repositório da **UCI Machine Learning Repository**. Ele contém transações realizadas entre **01/12/2010 e 09/12/2011** por uma loja online registrada no Reino Unido. Segundo a descrição da UCI, a empresa comercializa principalmente presentes e produtos para diversas ocasiões, e muitos de seus clientes são atacadistas.

Esse dataset é adequado ao tema do projeto, relacionado a um **atelier**, porque representa um cenário de vendas de produtos criativos, personalizados ou de presente, semelhante ao funcionamento comercial de um atelier que vende peças, encomendas ou produtos artesanais para diferentes clientes.

O dataset possui **541.909 registros** e contém variáveis relacionadas às transações, produtos, clientes e países. As principais colunas são:

- `InvoiceNo`: número da fatura ou transação.
- `StockCode`: código do produto.
- `Description`: descrição do produto.
- `Quantity`: quantidade comprada.
- `InvoiceDate`: data e hora da compra.
- `UnitPrice`: preço unitário do produto.
- `CustomerID`: identificação do cliente.
- `Country`: país do cliente.

Fonte: UCI Machine Learning Repository - Online Retail: https://archive.ics.uci.edu/dataset/352/online+retail

## Seleção e Justificativa das Features Analisadas

Como o PCA e o MDS trabalham melhor com variáveis numéricas, foi necessário transformar o dataset original em um conjunto de features quantitativas. O dataset original possui poucas variáveis numéricas diretas, como `Quantity` e `UnitPrice`, então foram criadas novas variáveis a partir das transações.

A análise será feita considerando cada cliente como um registro. Assim, em vez de analisar cada linha de compra individualmente, os dados serão agrupados por `CustomerID`. Essa escolha permite estudar padrões de comportamento dos clientes do atelier.

As features selecionadas foram:

- `TotalQuantity`: quantidade total de itens comprados pelo cliente.
- `TotalSpent`: valor total gasto pelo cliente, calculado por `Quantity * UnitPrice`.
- `Frequency`: número de compras ou faturas realizadas pelo cliente.
- `AvgTicket`: valor médio gasto por compra.
- `UniqueProducts`: quantidade de produtos diferentes comprados.
- `AvgUnitPrice`: preço médio dos produtos comprados.
- `Recency`: tempo desde a última compra do cliente.

Essas variáveis foram escolhidas porque representam diferentes aspectos do comportamento de compra:

- Volume de consumo: representado por `TotalQuantity`.
- Valor financeiro: representado por `TotalSpent` e `AvgTicket`.
- Frequência de relacionamento com a loja: representada por `Frequency`.
- Variedade de interesse: representada por `UniqueProducts`.
- Perfil de preço dos produtos comprados: representado por `AvgUnitPrice`.
- Atualidade do cliente: representada por `Recency`.

No contexto de um atelier, essas features podem ajudar a diferenciar clientes ocasionais, clientes recorrentes, clientes de alto valor, clientes que compram muitos itens pequenos e clientes que compram produtos mais caros ou personalizados.

## Preparação e Padronização dos Dados

Antes da aplicação do PCA e do MDS, o dataset precisa passar por uma etapa de preparação. Essa etapa é importante porque os dados originais possuem registros de vendas, possíveis cancelamentos, valores ausentes e variáveis em escalas diferentes.

As principais etapas de preparação são:

1. Remoção de registros sem `CustomerID`, pois a análise será feita por cliente.
2. Remoção ou tratamento de compras canceladas. No dataset, faturas cujo `InvoiceNo` começa com a letra `C` indicam cancelamentos. Também podem existir quantidades negativas associadas a devoluções.
3. Remoção de registros com `Quantity <= 0` ou `UnitPrice <= 0`, pois esses valores não representam compras válidas para a análise de comportamento.
4. Criação da variável `TotalPrice`, calculada como:

```text
TotalPrice = Quantity * UnitPrice
```

5. Agrupamento dos dados por cliente, criando as features numéricas selecionadas.
6. Tratamento de outliers, pois alguns clientes atacadistas podem ter valores muito acima dos demais. Esses casos podem ser mantidos para análise exploratória, mas devem ser observados com atenção nos gráficos.
7. Padronização das variáveis numéricas usando uma técnica como o `StandardScaler`, que transforma os dados para média 0 e desvio padrão 1.

A padronização é essencial porque as variáveis possuem escalas muito diferentes. Por exemplo, `TotalSpent` pode assumir valores muito altos, enquanto `AvgUnitPrice` pode ter valores menores. Sem padronização, as variáveis de maior escala teriam influência exagerada no PCA e no MDS.

Com os dados preparados e padronizados, torna-se possível aplicar PCA e MDS de forma mais adequada, permitindo visualizar os clientes em duas dimensões e investigar padrões relevantes para o contexto do atelier.