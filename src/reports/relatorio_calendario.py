import pandas as pd

# Caminho de entrada e saída
input_csv = 'data/proxima_partidas_normalizadas.csv'
output_excel = 'data/calendario_por_categoria.xlsx'

# Carregar os dados do CSV
df = pd.read_csv(input_csv)

# Garantir que a coluna 'Data' seja interpretada corretamente (se ainda não estiver formatada)
df['Data'] = pd.to_datetime(df['Data'], dayfirst=True, errors='coerce')

# Criar o Excel com abas separadas por categoria
with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
    for categoria, grupo in df.groupby('Categoria'):
        nome_aba = categoria[:31]  # Limite de 31 caracteres no nome da aba do Excel
        grupo.sort_values(by='Data').to_excel(writer, sheet_name=nome_aba, index=False)

print(f"Calendário salvo em: {output_excel}")
