from pathlib import Path

import pandas as pd
from sklearn.preprocessing import StandardScaler


ROOT_DIR = Path(__file__).resolve().parent
INPUT_FILE = ROOT_DIR / "data" / "Online Retail.xlsx"
OUTPUT_DIR = ROOT_DIR / "dados_processados"

FEATURE_COLUMNS = [
    "TotalQuantity",
    "TotalSpent",
    "Frequency",
    "AvgTicket",
    "UniqueProducts",
    "AvgUnitPrice",
    "Recency",
]


def most_frequent_value(series: pd.Series):
    mode = series.mode(dropna=True)
    if mode.empty:
        return pd.NA
    return mode.iloc[0]


def load_dataset() -> pd.DataFrame:
    return pd.read_excel(INPUT_FILE)


def clean_transactions(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()

    cleaned["InvoiceNo"] = cleaned["InvoiceNo"].astype(str)
    cleaned["CustomerID"] = pd.to_numeric(cleaned["CustomerID"], errors="coerce")
    cleaned["Quantity"] = pd.to_numeric(cleaned["Quantity"], errors="coerce")
    cleaned["UnitPrice"] = pd.to_numeric(cleaned["UnitPrice"], errors="coerce")
    cleaned["InvoiceDate"] = pd.to_datetime(cleaned["InvoiceDate"], errors="coerce")

    cleaned = cleaned.dropna(
        subset=["InvoiceNo", "StockCode", "Quantity", "UnitPrice", "InvoiceDate", "CustomerID"]
    )

    valid_purchase = (
        ~cleaned["InvoiceNo"].str.upper().str.startswith("C")
        & (cleaned["Quantity"] > 0)
        & (cleaned["UnitPrice"] > 0)
    )
    cleaned = cleaned.loc[valid_purchase].copy()

    cleaned["CustomerID"] = cleaned["CustomerID"].astype(int)
    cleaned["TotalPrice"] = cleaned["Quantity"] * cleaned["UnitPrice"]

    return cleaned


def build_customer_features(cleaned: pd.DataFrame) -> pd.DataFrame:
    snapshot_date = cleaned["InvoiceDate"].max() + pd.Timedelta(days=1)

    grouped = cleaned.groupby("CustomerID")
    customer_features = grouped.agg(
        TotalQuantity=("Quantity", "sum"),
        TotalSpent=("TotalPrice", "sum"),
        Frequency=("InvoiceNo", "nunique"),
        UniqueProducts=("StockCode", "nunique"),
        AvgUnitPrice=("UnitPrice", "mean"),
        LastPurchase=("InvoiceDate", "max"),
        Country=("Country", most_frequent_value),
    ).reset_index()

    customer_features["AvgTicket"] = (
        customer_features["TotalSpent"] / customer_features["Frequency"]
    )
    customer_features["Recency"] = (
        snapshot_date - customer_features["LastPurchase"]
    ).dt.days

    ordered_columns = ["CustomerID", "Country"] + FEATURE_COLUMNS + ["LastPurchase"]
    return customer_features[ordered_columns].sort_values("CustomerID").reset_index(drop=True)


def standardize_features(customer_features: pd.DataFrame) -> pd.DataFrame:
    scaler = StandardScaler()
    standardized_values = scaler.fit_transform(customer_features[FEATURE_COLUMNS])

    standardized = pd.DataFrame(
        standardized_values,
        columns=[f"{column}_std" for column in FEATURE_COLUMNS],
        index=customer_features.index,
    )

    return pd.concat(
        [customer_features[["CustomerID", "Country"]], standardized],
        axis=1,
    )


def write_summary(raw: pd.DataFrame, cleaned: pd.DataFrame, features: pd.DataFrame) -> None:
    removed_rows = len(raw) - len(cleaned)
    summary = f"""# Resumo da Preparacao dos Dados

## Dataset de entrada

- Arquivo: `online+retail/Online Retail.xlsx`
- Registros originais: {len(raw):,}
- Colunas originais: {len(raw.columns)}

## Limpeza aplicada

- Remocao de registros sem identificacao de cliente ou campos essenciais.
- Remocao de faturas canceladas, identificadas por `InvoiceNo` iniciado com `C`.
- Remocao de registros com `Quantity <= 0`.
- Remocao de registros com `UnitPrice <= 0`.
- Criacao da coluna `TotalPrice = Quantity * UnitPrice`.

## Resultado da limpeza

- Registros validos apos limpeza: {len(cleaned):,}
- Registros removidos: {removed_rows:,}
- Clientes analisados: {features["CustomerID"].nunique():,}
- Periodo considerado: {cleaned["InvoiceDate"].min()} ate {cleaned["InvoiceDate"].max()}

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
"""
    (OUTPUT_DIR / "resumo_preparacao.md").write_text(summary, encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    raw = load_dataset()
    cleaned = clean_transactions(raw)
    customer_features = build_customer_features(cleaned)
    standardized = standardize_features(customer_features)

    cleaned.to_csv(OUTPUT_DIR / "transacoes_limpas.csv", index=False)
    customer_features.to_csv(OUTPUT_DIR / "features_clientes.csv", index=False)
    standardized.to_csv(OUTPUT_DIR / "features_clientes_padronizadas.csv", index=False)
    write_summary(raw, cleaned, customer_features)

    print("Preparacao concluida.")
    print(f"Registros originais: {len(raw):,}")
    print(f"Registros validos: {len(cleaned):,}")
    print(f"Clientes analisados: {customer_features['CustomerID'].nunique():,}")
    print(f"Arquivos salvos em: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
