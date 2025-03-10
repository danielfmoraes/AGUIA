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


# Função para obter os dados da página de próximas partidas
def get_upcoming_matches(url):
    driver = start_browser()
    driver.get(url)
    
    # Esperar até que o conteúdo da página esteja carregado
    wait = WebDriverWait(driver, 20)
    
    # Obter a categoria do campeonato diretamente do URL
    category = get_category_from_url(url)
    
    match_data = []
    
    try:
        # Esperar pelo link "Próximas Partidas"
        matches_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Próximas Partidas')]")))
        print("Botão 'Próximas Partidas' encontrado e clicado.")
        matches_button.click()
        
        # Esperar para garantir que a lista de partidas seja carregada
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'unstriped.matches--table')))
        print("Lista de próximas partidas carregada.")
        
        # Encontrar a lista de partidas
        match_section = driver.find_elements(By.CLASS_NAME, 'unstriped.matches--table')
        
        # Verificar quantas partidas foram encontradas
        print(f"Próximas partidas encontradas: {len(match_section)}")
        
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
                
                # Local da partida - método melhorado
                try:
                    # Tentar encontrar todos os elementos td e procurar pelo que contém informações de local
                    td_elements = section.find_elements(By.TAG_NAME, "td")
                    local = 'Local não informado'
                    
                    for td in td_elements:
                        td_text = td.text.strip()
                        # Verificar se o texto parece ser um endereço ou contém ícone de localização
                        if any(keyword in td_text.lower() for keyword in ['ginásio', 'quadra', 'centro', 'rua', 'avenida', 'av.', 'r.']) or td.find_elements(By.CLASS_NAME, "fa-map-marker-alt"):
                            local = td_text
                            # Remover o número de telefone se estiver presente
                            if "Telefone:" in local:
                                local = local.split("Telefone:")[0].strip()
                            break
                except Exception as e:
                    print(f"Erro ao extrair local: {e}")
                    local = 'Local não informado'
                
                # Adicionar os dados coletados na lista, incluindo a categoria
                match_data.append([date, match_time, team1, team2, local, category])
                print(f"Próxima partida adicionada: {team1} vs {team2}, Local: {local}")
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
            writer.writerow(["Data", "Horário", "Equipe 1", "Equipe 2", "Local", "Categoria"])
        
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

# Remover arquivo existente para evitar duplicações
if os.path.exists('data/proximas_partidas.csv'):
    os.remove('data/proximas_partidas.csv')
    print("Arquivo anterior de próximas partidas removido.")

for url in urls:
    data = get_upcoming_matches(url)
    save_to_csv(data, 'data/proximas_partidas.csv')
    print(f'Dados de próximas partidas salvos para {url}')