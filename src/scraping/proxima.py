from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import os

def start_browser():
    options = Options()
    options.headless = True
    options.binary_location = "/usr/bin/brave-browser"  # Ajuste conforme o seu sistema
    service = Service("/usr/local/bin/chromedriver")     # Ajuste conforme o seu sistema
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def get_category_from_url(url):
    try:
        if "sub-" in url.lower():
            sub_pos = url.lower().find("sub-")
            category_number = ""
            pos = sub_pos + 4
            while pos < len(url) and url[pos].isdigit():
                category_number += url[pos]
                pos += 1

            gender = "Masculino" if "masculino" in url.lower() else "Feminino" if "feminino" in url.lower() else "Masculino"
            category = f"SUB {category_number} {gender}"
            print(f"Categoria extraída do URL: {category}")
            return category
        else:
            print("Padrão 'sub-' não encontrado no URL")
            return "Categoria não encontrada"
    except Exception as e:
        print(f"Erro ao extrair categoria do URL: {e}")
        return "Categoria não encontrada"

def get_upcoming_matches(url):
    driver = start_browser()
    driver.get(url)
    wait = WebDriverWait(driver, 20)
    category = get_category_from_url(url)
    match_data = []

    try:
        matches_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Próximas Partidas')]")))
        print("Botão 'Próximas Partidas' encontrado e clicado.")
        matches_button.click()

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'unstriped.matches--table')))
        print("Lista de próximas partidas carregada.")

        match_sections = driver.find_elements(By.CLASS_NAME, 'unstriped.matches--table')
        print(f"Próximas partidas encontradas: {len(match_sections)}")

        for section in match_sections:
            try:
                date = section.find_element(By.XPATH, ".//preceding-sibling::h3").text.strip()
                match_time = section.find_element(By.XPATH, ".//td[@width='35%']").text.strip().replace('Horário: ', '')
                teams = section.find_elements(By.CLASS_NAME, 'team-name')
                team1 = teams[0].text.strip() if len(teams) > 0 else 'N/A'
                team2 = teams[1].text.strip() if len(teams) > 1 else 'N/A'

                # Local
                try:
                    td_elements = section.find_elements(By.TAG_NAME, "td")
                    local = 'Local não informado'
                    for td in td_elements:
                        td_text = td.text.strip().lower()
                        if any(k in td_text for k in ['ginásio', 'quadra', 'centro', 'rua', 'avenida', 'av.', 'r.']):
                            local = td.text.strip()
                            if "Telefone:" in local:
                                local = local.split("Telefone:")[0].strip()
                            break
                except:
                    local = 'Local não informado'

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
    file_exists = os.path.isfile(filename)
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Data", "Horário", "Equipe 1", "Equipe 2", "Local", "Categoria"])
        writer.writerows(data)
        print(f"Dados adicionados ao arquivo {filename}")

# URLs
urls = [
    'https://www.fpb.com.br/campeonatos/campeonato-sub-12-masculino-da-gsp/863',
    'https://www.fpb.com.br/campeonatos/campeonato-sub-13-masculino-da-gsp/864',
    'https://www.fpb.com.br/campeonatos/campeonato-sub-14-masculino-da-gsp/865',
    'https://www.fpb.com.br/campeonatos/campeonato-sub-15-masculino-da-gsp/866',
    'https://www.fpb.com.br/campeonatos/campeonato-estadual-sub-16-masculino/867',
    # Adicione outros URLs conforme necessário
]

# Garantir diretório
os.makedirs('data', exist_ok=True)

# Apagar arquivo anterior
csv_path = 'data/proximas_partidas.csv'
if os.path.exists(csv_path):
    os.remove(csv_path)
    print("Arquivo anterior de próximas partidas removido.")

# Coletar dados
for url in urls:
    data = get_upcoming_matches(url)
    save_to_csv(data, csv_path)
    print(f'Dados salvos para {url}')
