import requests
import csv
import os
from bs4 import BeautifulSoup

# Lista de URLs para os campeonatos
urls = [
    ("SUB-12 Masculino", "https://www.fpb.com.br/estatisticas/campeonato-sub-12-masculino-da-gsp/863"),
    ("SUB-13 Masculino", "https://www.fpb.com.br/estatisticas/campeonato-sub-13-masculino-da-gsp/864"),
    ("SUB-14 Masculino", "https://www.fpb.com.br/estatisticas/campeonato-sub-14-masculino-da-gsp/865"),
    ("SUB-15 Masculino", "https://www.fpb.com.br/estatisticas/campeonato-sub-15-masculino-da-gsp/866"),
    ("SUB-16 Masculino", "https://www.fpb.com.br/estatisticas/campeonato-estadual-sub-16-masculino/867"),
    ("SUB-18 Masculino", "https://www.fpb.com.br/estatisticas/campeonato-estadual-sub-18-masculino/868"),
    ("SUB-20 Masculino", "https://www.fpb.com.br/estatisticas/campeonato-estadual-sub-20-masculino/869"),
    ("SUB-13 Feminino", "https://www.fpb.com.br/estatisticas/campeonato-estadual-sub-13-feminino/870"),
    ("SUB-14 Feminino", "https://www.fpb.com.br/estatisticas/campeonato-estadual-sub-14-feminino/871"),
    ("SUB-15 Feminino", "https://www.fpb.com.br/estatisticas/campeonato-estadual-sub-15-feminino/872"),
    ("SUB-16 Feminino", "https://www.fpb.com.br/estatisticas/campeonato-estadual-sub-16-feminino/873"),
    ("SUB-18 Feminino", "https://www.fpb.com.br/estatisticas/campeonato-estadual-sub-18-feminino/874"),
    ("SUB-20 Feminino", "https://www.fpb.com.br/estatisticas/campeonato-estadual-sub-20-feminino/875")
]

# Função para extrair as estatísticas e salvar em CSV
def extrair_e_salvar_estatisticas(nome_campeonato, url):
    # Fazer a requisição HTTP
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Tentar encontrar a tabela de estatísticas
    tabela = soup.find('table', {'class': 'unstriped data__table'})
    
    # Verificar se a tabela existe
    if tabela:
        # Extrair os dados das linhas da tabela
        rows = tabela.find_all('tr')
        estatisticas = []
        
        for row in rows[1:]:  # Ignorar o cabeçalho
            cols = row.find_all('td')
            if len(cols) > 1:
                atleta = cols[0].get_text(strip=True)
                equipe = cols[1].get_text(strip=True)
                pontos = cols[2].get_text(strip=True)
                jogos = cols[3].get_text(strip=True)
                medias = cols[4].get_text(strip=True)
                estatisticas.append([atleta, equipe, pontos, jogos, medias])
        
        # Criar pasta "data" se não existir
        if not os.path.exists("data"):
            os.makedirs("data")
        
        # Definir o nome do arquivo CSV
        file_name = f"data/{nome_campeonato}.csv"
        
        # Salvar as estatísticas em um arquivo CSV
        with open(file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Atleta", "Equipe", "PTS", "Jogos", "Médias"])  # Cabeçalho
            writer.writerows(estatisticas)
        
        print(f"Estatísticas do {nome_campeonato} salvas com sucesso em {file_name}")
    else:
        print(f"Não há estatísticas disponíveis para o campeonato {nome_campeonato} em {url}")

# Loop para percorrer os links e salvar os dados
for nome_campeonato, url in urls:
    print(f"Extraindo e salvando estatísticas de: {nome_campeonato}")
    extrair_e_salvar_estatisticas(nome_campeonato, url)
