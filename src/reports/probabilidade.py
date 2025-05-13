import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.utils import resample
from sklearn.preprocessing import LabelEncoder

# Ler o CSV
df = pd.read_csv('data/partidas_normalizadas.csv', delimiter=",")
df = df.dropna(subset=["Equipe 1", "Equipe 2", "Placar", "Data"])
df["Data"] = pd.to_datetime(df["Data"], format="%d/%m/%Y")
df["Categoria"] = df["Categoria"].str.replace(" Masculino", "", regex=False)

# Listar categorias disponíveis
categorias_disponiveis = df['Categoria'].dropna().unique()
print("Categorias disponíveis:")
for i, cat in enumerate(categorias_disponiveis, 1):
    print(f"{i}. {cat}")

# Solicitar ao usuário que escolha uma categoria
while True:
    try:
        escolha = int(input("Digite o número da categoria desejada: "))
        if 1 <= escolha <= len(categorias_disponiveis):
            categoria_escolhida = categorias_disponiveis[escolha - 1]
            break
        else:
            print("Número inválido. Tente novamente.")
    except ValueError:
        print("Entrada inválida. Digite um número.")

# Filtrar os dados pela categoria escolhida
df_categoria = df[df['Categoria'] == categoria_escolhida]

# Função para processar o placar
def processar_placar(placar):
    try:
        if isinstance(placar, str) and 'x' in placar:
            time1, time2 = placar.split('x')
            if time1.strip().isdigit() and time2.strip().isdigit():
                return int(time1.strip()), int(time2.strip())
            else:
                return None, None
        else:
            return None, None
    except:
        return None, None

# Processar placar
df_categoria[['Placar_Time1', 'Placar_Time2']] = df_categoria['Placar'].apply(lambda x: pd.Series(processar_placar(x)))

# Filtrar os dados válidos
df_realizado = df_categoria.dropna(subset=['Placar_Time1', 'Placar_Time2'])

# Criar a variável alvo
y = (df_realizado['Placar_Time1'] > df_realizado['Placar_Time2']).astype(int)

# Seleção das features
X = df_realizado[['Equipe 1', 'Equipe 2']].copy()

# Codificar os times
encoder = LabelEncoder()
X['Equipe 1'] = encoder.fit_transform(X['Equipe 1'])
X['Equipe 2'] = encoder.transform(X['Equipe 2'])

# Balancear os dados
X_balanced, y_balanced = resample(X, y, replace=True, n_samples=len(X), random_state=42)

# Dividir treino/teste
X_train, X_test, y_train, y_test = train_test_split(X_balanced, y_balanced, test_size=0.2, random_state=42)

# Treinar modelo
modelo = RandomForestClassifier(n_estimators=200, max_depth=15, random_state=42)
modelo.fit(X_train, y_train)

# Avaliação
y_pred = modelo.predict(X_test)
print("\nRelatório de classificação:")
print(classification_report(y_test, y_pred))

# Prever jogos futuros
todos_times = pd.unique(df_categoria[["Equipe 1", "Equipe 2"]].values.ravel('K'))
jogos_futuros = [(t1, t2) for t1 in todos_times for t2 in todos_times if t1 != t2]

df_futuro = pd.DataFrame(jogos_futuros, columns=["Equipe 1", "Equipe 2"])
df_futuro['Equipe 1'] = encoder.transform(df_futuro['Equipe 1'])
df_futuro['Equipe 2'] = encoder.transform(df_futuro['Equipe 2'])
X_futuro = df_futuro[['Equipe 1', 'Equipe 2']]

if X_futuro.shape[0] > 0:
    df_futuro["Probabilidade_Vitoria_Time1"] = modelo.predict_proba(X_futuro)[:, 1]
    df_futuro['Equipe 1'] = encoder.inverse_transform(df_futuro['Equipe 1'])
    df_futuro['Equipe 2'] = encoder.inverse_transform(df_futuro['Equipe 2'])

    print("\nPrevisão de vitórias para jogos futuros:")
    print(df_futuro[['Equipe 1', 'Equipe 2', 'Probabilidade_Vitoria_Time1']])

    nome_arquivo = f"data/probabilidade_vitoria_jogos_futuros_{categoria_escolhida.lower().replace(' ', '_')}.xlsx"
    df_futuro.to_excel(nome_arquivo, index=False)
    print(f"\nPlanilha salva com sucesso como: {nome_arquivo}")
else:
    print("Não há dados válidos para prever os jogos futuros.")
