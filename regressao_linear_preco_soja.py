import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from scipy import stats
import scipy.stats as stats
import statsmodels.api as sm

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
pd.set_option('display.precision', 2)

df = pd.read_excel('dataset.xlsx')

print("\nInformações do dataset:")
print(df.info())

print("\nValores nulos por coluna:")
print(df.isnull().sum())

df.drop_duplicates(inplace=True)

df.dropna(inplace=True)

z_scores = np.abs(stats.zscore(df.select_dtypes(include=[np.number])))
df = df[(z_scores < 3).all(axis=1)]

print("\nEstatísticas descritivas:")
print(df.describe().T)

# Matriz de correlação
plt.figure(figsize=(10, 8))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Matriz de Correlação")
plt.xticks(rotation=90)
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()

# Histogramas
df.hist(bins=30, figsize=(12, 10), color='skyblue', edgecolor='black')
plt.suptitle("Distribuição das Variáveis")
plt.tight_layout()
plt.show()

scaler = StandardScaler()
variavel_alvo = 'bean_settle'
variaveis_preditoras = ['Oil', 'USD', 'US_Production', 'Brazil_Production']

# Normalizar os dados
X = scaler.fit_transform(df[variaveis_preditoras])
y = df[variavel_alvo].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

modelo = LinearRegression()
modelo.fit(X_train, y_train)

y_pred = modelo.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print("\n" + "="*50)
print("Resultados da Regressão Linear".center(50))
print("="*50)
print(f"Variável Alvo: {variavel_alvo}")
print(f"Variáveis Preditoras: {', '.join(variaveis_preditoras)}")
print(f"Coeficientes: {modelo.coef_}")
print(f"Intercepto: {modelo.intercept_:.2f}")
print(f"R²: {r2:.4f}")
print(f"RMSE: {rmse:.2f}")

residuos = y_test - y_pred

plt.figure(figsize=(10, 6))
sns.histplot(residuos, kde=True, color='purple')
plt.title('Distribuição dos Resíduos')
plt.xlabel('Erro')
plt.show()

plt.figure(figsize=(10, 6))
sns.scatterplot(x=y_test, y=y_pred, alpha=0.7, color='blue')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')  # Linha de referência
plt.xlabel('Valor Real')
plt.ylabel('Valor Predito')
plt.title('Valor Real vs Valor Predito')
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
sns.scatterplot(x=y_test, y=residuos, alpha=0.7, color='green')
plt.axhline(0, color='red', linestyle='--')
plt.xlabel('Valor Real')
plt.ylabel('Resíduo')
plt.title('Resíduos vs Valor Real')
plt.grid(True)
plt.show()

sm.qqplot(residuos, line='45', fit=True)
plt.title("QQ-Plot dos Resíduos")
plt.grid(True)
plt.show()
