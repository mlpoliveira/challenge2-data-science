# %%
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd

url = 'https://raw.githubusercontent.com/mlpoliveira/challenge2-data-science/main/TelecomX_Data.json'

# Carregando os dados corretamente
df = pd.read_json(url)
# %%
# Visualizando as primeiras linhas
df.head()
# 1. Verificar o formato dos dados
print("Formato do dataset:")
print(df.shape)

# 2. Informações gerais sobre as colunas
print("\nInformações sobre as colunas:")
df.info()

# 3. Verificar valores únicos na variável target
print("\nDistribuição de Churn:")
print(df['Churn'].value_counts())

# 4. Verificar se há valores nulos
print("\nValores nulos por coluna:")
print(df.isnull().sum())

# 5. Estatísticas descritivas das variáveis numéricas
print("\nEstatísticas descritivas:")
df.describe()
# %%
