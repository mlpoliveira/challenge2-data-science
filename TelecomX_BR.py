{
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "4foVEKhrlqcH"
      },
      "source": [
        "#📌 Extração"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "1. Verificação Inicial dos Dados\n",
        "\n",
        "1.1 Carregar os Dados"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 1,
      "metadata": {
        "id": "1--uPM88l7JH"
      },
      "outputs": [],
      "source": [
        "import pandas as pd\n",
        "import warnings\n",
        "warnings.filterwarnings(\"ignore\", category=FutureWarning)\n",
        "\n",
        "url = 'https://raw.githubusercontent.com/mlpoliveira/challenge2-data-science/main/TelecomX_Data.json'\n",
        "df = pd.read_json(url)\n",
        "\n",
        "# Backup dos dados brutos\n",
        "df.to_csv('dados_brutos.csv', index=False)"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "#🔧 Transformação"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 2,
      "metadata": {
        "id": "bsm-WTLjmHvt"
      },
      "outputs": [],
      "source": [
        "# Copiando o DataFrame original para não mexer diretamente nele\n",
        "df_original = df.copy()"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "1. Expandir Colunas Aninhadas (JSON)\n",
        "\n",
        "As colunas customer, phone, internet e account contêm dicionários que precisam ser normalizados."
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 3,
      "metadata": {},
      "outputs": [],
      "source": [
        "# Normalizar as colunas aninhadas\n",
        "customer_df = pd.json_normalize(df['customer'])\n",
        "phone_df = pd.json_normalize(df['phone'])\n",
        "internet_df = pd.json_normalize(df['internet'])\n",
        "account_df = pd.json_normalize(df['account'])\n",
        "\n",
        "# Combinar tudo em um único DataFrame\n",
        "df_final = pd.concat([\n",
        "    df[['customerID', 'Churn']],  # Manter colunas principais\n",
        "    customer_df,\n",
        "    phone_df,\n",
        "    internet_df,\n",
        "    account_df\n",
        "], axis=1)"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "2. Conversão de Tipos de Dados"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 4,
      "metadata": {},
      "outputs": [],
      "source": [
        "# Converter SeniorCitizen para categórico (Sim/Não)\n",
        "df_final['SeniorCitizen'] = df_final['SeniorCitizen'].map({0: 'No', 1: 'Yes'})\n",
        "\n",
        "# Converter Charges.Total para numérico\n",
        "df_final['Charges.Total'] = pd.to_numeric(df_final['Charges.Total'], errors='coerce')"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "3. Tratamento de Valores Ausentes\n",
        "\n",
        "Padronizar valores em colunas de serviços"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 5,
      "metadata": {},
      "outputs": [],
      "source": [
        "services = ['OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies']\n",
        "\n",
        "for col in services:\n",
        "    df_final[col] = df_final[col].replace({'No internet service': 'No'})"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "4. Criação de Novas Variáveis (Feature Engineering)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 6,
      "metadata": {},
      "outputs": [],
      "source": [
        "# Categorizar tenure (Tempo como Cliente)\n",
        "def categorize_tenure(tenure):\n",
        "    if tenure <= 12:\n",
        "        return '0-1 ano'\n",
        "    elif tenure <= 24:\n",
        "        return '1-2 anos'\n",
        "    elif tenure <= 36:\n",
        "        return '2-3 anos'\n",
        "    else:\n",
        "        return '+3 anos'\n",
        "\n",
        "df_final['tenure_group'] = df_final['tenure'].apply(categorize_tenure)\n",
        "\n",
        "# Calcular Valor Médio Mensal\n",
        "df_final['AvgMonthlyCharge'] = df_final['Charges.Total'] / df_final['tenure']\n",
        "\n",
        "# Tratar divisão por zero e valores ausentes\n",
        "df_final['AvgMonthlyCharge'] = df_final['AvgMonthlyCharge'].fillna(0)"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "6XnTC2NTmMRL"
      },
      "source": [
        "#📊 Carga e análise"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 7,
      "metadata": {
        "id": "1jgUnLqTmPdd"
      },
      "outputs": [],
      "source": [
        "# Salvar dados transformados\n",
        "df_final.to_csv('dados_transformados.csv', index=False)\n",
        "\n",
        "# Salvar dados limpos\n",
        "df_final.to_csv('dados_limpos.csv', index=False)"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "5. Validação Final da Transformação"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 8,
      "metadata": {},
      "outputs": [],
      "source": [
        "# Verificar estrutura final\n",
        "def check_final_data(df):\n",
        "    print(\"\\nInformações do DataFrame:\")\n",
        "    print(df.info())\n",
        "    \n",
        "    print(\"\\nValores ausentes por coluna:\")\n",
        "    print(df.isnull().sum())\n",
        "    \n",
        "    print(\"\\nDistribuição de Churn:\")\n",
        "    print(df['Churn'].value_counts(normalize=True) * 100)\n",
        "    \n",
        "    print(\"\\nAmostra dos dados transformados:\")\n",
        "    return df.sample(5)\n",
        "\n",
        "check_final_data(df_final)"
      ]
    }
  ],
  "metadata": {
    "kernelspec": {
      "display_name": "Python 3",
      "language": "python",
      "name": "python3"
    },
    "language_info": {
      "codemirror_mode": {
        "name": "ipython",
        "version": 3
      },
      "file_extension": ".py",
      "mimetype": "text/x-python",
      "name": "python",
      "nbconvert_exporter": "python",
      "pygments_lexer": "ipython3",
      "version": "3.8.5"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 4
}