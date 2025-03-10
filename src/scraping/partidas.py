from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
import time
import csv
import os

# Função para iniciar o WebDriver e acessar a página
def start_browser():
    # Inicializa o WebDriver com o Firefox
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")  # Roda sem abrir a janela do navegador
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
    return driver

def get_category_from_url(url):
    try:
        # Extract the category from the URL
        if "sub-" in url.lower():
            # Find the position of "sub-" in the URL
            sub_pos = url.lower().find("sub-")
            # Extract the number after "sub-"
            category_number = ""
            pos = sub_pos + 4  # Start after "sub-"
            while pos < len(url) and url[pos].isdigit():
                category_number += url[pos]
                pos += 1
            
            # Determine gender
            if "masculino" in url.lower():
                gender = "Masculino"
            elif "feminino" in url.lower():
                gender = "Feminino"
            else:
                gender = "Masculino"  # Default to Masculino
            
            category = f"SUB {category_number} {gender}"
            print(f"Categoria extraída do URL: {category}")
            return category
        else:
            print("Padrão 'sub-' não encontrado no URL")
            return "Categoria não encontrada"
    except Exception as e:
        print(f"Erro ao extrair categoria do URL: {e}")
        return "Categoria não encontrada"


# Função para obter os dados da página de partidas
def get_match_data(url):
    driver = start_browser()
    driver.get(url)
    
    # Esperar até que o conteúdo da página esteja carregado
    wait = WebDriverWait(driver, 20)
    
    # Obter a categoria do campeonato diretamente do URL
    category = get_category_from_url(url)
    
    match_data = []
    
    try:
        # Esperar pelo link "Partidas Realizadas"
        matches_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Partidas Realizadas')]")))
        print("Botão 'Partidas Realizadas' encontrado e clicado.")
        matches_button.click()
        
        # Esperar para garantir que a lista de partidas seja carregada
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'unstriped.matches--table')))
        print("Lista de partidas carregada.")
        
        # Encontrar a lista de partidas
        match_section = driver.find_elements(By.CLASS_NAME, 'unstriped.matches--table')
        
        # Verificar quantas partidas foram encontradas
        print(f"Partidas encontradas: {len(match_section)}")
        
        for section in match_section:
            try:
                # Data
                date = section.find_element(By.XPATH, ".//preceding-sibling::h3").text.strip()
                
                # Horário
                match_time = section.find_element(By.XPATH, ".//td[@width='35%']").text.strip().replace('Horário: ', '')
                
                # Equipes
                teams = section.find_elements(By.CLASS_NAME, 'team-name')
                team1 = teams[0].text.strip() if len(teams) > 0 else 'N/A'
                team2 = teams[1].text.strip() if len(teams) > 1 else 'N/A'
                
                # Placar - Ajustar para garantir a coleta correta
                try:
                    score = section.find_element(By.XPATH, ".//span[normalize-space(text())]").text.strip()
                except:
                    score = 'X'  # Caso não encontre o placar
                
                # Adicionar os dados coletados na lista, incluindo a categoria
                match_data.append([date, match_time, team1, team2, score, category])
                print(f"Partida adicionada: {team1} vs {team2}, Placar: {score}")
            except Exception as e:
                print(f"Erro ao extrair dados de uma partida: {e}")

    except Exception as e:
        print(f"Erro ao acessar ou processar a página: {e}")
    
    finally:
        driver.quit()
    
    return match_data

def save_to_csv(data, filename):
    # Check if file exists to determine if we need to write headers
    file_exists = os.path.isfile(filename)
    
    # Open in append mode
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write header only if file doesn't exist yet
        if not file_exists:
            writer.writerow(["Data", "Horário", "Equipe 1", "Equipe 2", "Placar", "Categoria"])
        
        # Write the match data
        writer.writerows(data)
        print(f"Dados adicionados ao arquivo {filename}")

# URLs de campeonatos
urls = [
    'https://www.fpb.com.br/campeonatos/campeonato-sub-12-masculino-da-gsp/863',
    'https://www.fpb.com.br/campeonatos/campeonato-sub-13-masculino-da-gsp/864',
    'https://www.fpb.com.br/campeonatos/campeonato-sub-14-masculino-da-gsp/865',
    'https://www.fpb.com.br/campeonatos/campeonato-sub-15-masculino-da-gsp/866',
    'https://www.fpb.com.br/campeonatos/campeonato-estadual-sub-16-masculino/867',
    'https://www.fpb.com.br/campeonatos/campeonato-estadual-sub-18-masculino/868',
    'https://www.fpb.com.br/campeonatos/campeonato-estadual-sub-20-masculino/869',
    'https://www.fpb.com.br/campeonatos/campeonato-estadual-sub-13-feminino/870',
    'https://www.fpb.com.br/campeonatos/campeonato-estadual-sub-14-feminino/871',
    'https://www.fpb.com.br/campeonatos/campeonato-estadual-sub-15-feminino/872',
    'https://www.fpb.com.br/campeonatos/campeonato-estadual-sub-16-feminino/873',
    'https://www.fpb.com.br/campeonatos/campeonato-estadual-sub-18-feminino/874',
    'https://www.fpb.com.br/campeonatos/campeonato-estadual-sub-20-feminino/875',
]

# Garantir que o diretório 'data' exista
os.makedirs('data', exist_ok=True)

for url in urls:
    data = get_match_data(url)
    save_to_csv(data, 'data/partidas.csv')
    print(f'Dados salvos para {url}')