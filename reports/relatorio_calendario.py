import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os
import numpy as np
from collections import defaultdict
import textwrap
from datetime import datetime

# Criar a pasta 'posts' se não existir
os.makedirs("posts/proximos_jogos", exist_ok=True)

# Mapeamento das equipes para suas imagens
equipes_imagens = {
    'CIRCULO MILITAR S.P.': 'circulo_militar.jpg',
    'C.A. PAULISTANO': 'paulistano.jpg',
    'C.A. MONTE LIBANO': 'ca_monte.jpg',
    'CLUBE CAMPINEIRO DE REGATAS E NATAÇÃO': 'capineiro_regatas.jpg',
    'CLUBE ESPERIA': 'esperia.jpg',
    'E.C. PINHEIROS': 'pinheiros.jpg',
    'SÃO PAULO F.C.': 'spfc.jpg',
    'S.E. PALMEIRAS': 'palmeiras.jpg',
    'S.C. CORINTHIANS PTA.': 'sccp.jpg',
    'T.C. PAULISTA': 'tenis_paulista.jpg',
    'INTERNACIONAL DE REGATAS': 'internacional_regatas.jpg',
    'SÃO JOSÉ BASKETBALL / ATLETA CIDADÃO': 'sjc.jpg',
    'JACAREI BASKETBALL': 'jacarei.jpg',
    'SANTO ANDRE / APABA': 'apaba.jpg',
    'AMAB / GIRAFINHAS / MAUA': 'amab.jpg',
    'DOUBLE VOTORANTIM BASKET': 'votorantim.jpg',
    'SÃO BERNARDO BASQUETE': 'sbc.jpg',
    'RM STARS BASQUETEBOL': 'RM.jpg',
    'F.R. ALPHAVILLE': 'sbtc.jpg',
    'A.D. CENTRO OLIMPICO': 'adcentrool.jpg',
    'CFE TAUBATE / IGC / LBCP': 'taubate.jpg',
    'CLUBE DE CAMPO DE RIO CLARO - CCRC': 'rioclaro.jpg',
    'A.A. MOGI DAS CRUZES': 'mogi.jpg'
}

# Ler o CSV de próximas partidas
df = pd.read_csv('data/proximas_partidas_normalizadas.csv', delimiter=",").dropna(subset=["Equipe 1", "Equipe 2"])

# Função para formatar a data
def formatar_data(data_str):
    try:
        # Converter para objeto de data
        data_obj = datetime.strptime(data_str, '%d/%m/%Y')
        # Formatar com nome do mês
        meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 
                'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
        return f"{data_obj.day} de {meses[data_obj.month-1]}"
    except:
        return data_str

# Função para criar posts de jogos por local
def criar_posts_jogos_por_local():
    # Agrupar jogos por local e data
    jogos_por_local_data = defaultdict(list)
    
    for _, row in df.iterrows():
        local = row['Local']
        data = row['Data']
        if pd.notna(local) and local.strip() != '' and pd.notna(data) and data.strip() != '':
            chave = (local, data)
            jogos_por_local_data[chave].append(row)
    
    # Criar um post para cada combinação de local e data
    for (local, data), jogos in jogos_por_local_data.items():
        criar_post_local_data(local, data, jogos)

# Função para criar um post para um local e data específicos
def criar_post_local_data(local, data, jogos):
    # Criar uma imagem de fundo
    background = Image.new('RGB', (1080, 1080), color=(0, 0, 51))  # Fundo azul escuro
    
    # Carregar o logo AA para o canto direito
    try:
        logo_aa = Image.open('image/aa.jpg').convert("RGBA")
        logo_aa = logo_aa.resize((100, 100))
        background.paste(logo_aa, (950, 30), logo_aa if logo_aa.mode == 'RGBA' else None)
    except Exception as e:
        print(f"Erro ao carregar logo AA: {e}")
    
    # Criar o objeto de desenho
    draw = ImageDraw.Draw(background)
    
    # Carregar fontes
    try:
        title_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 50)
        date_title_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 60)  # Fonte maior para a data
        subtitle_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 36)
        category_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 34)  # Fonte maior para categoria/horário
        team_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 28)
        info_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 24)
        address_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Italic.ttf', 22)
    except:
        # Fallback para fonte padrão se não encontrar
        title_font = ImageFont.load_default()
        date_title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        category_font = ImageFont.load_default()
        team_font = ImageFont.load_default()
        info_font = ImageFont.load_default()
        address_font = ImageFont.load_default()
    
    # Adicionar título
    draw.text((540, 40), "BASQUETE FPB", font=title_font, fill=(255, 255, 255), anchor="mt")
    
    # Formatar e adicionar data em destaque
    data_formatada = formatar_data(data)
    draw.text((540, 110), f"JOGOS {data_formatada}", font=date_title_font, fill=(255, 215, 0), anchor="mt")  # Dourado e maior
    
    # Altura inicial para começar a desenhar os jogos
    y_pos = 180
    
    # Desenhar cada jogo com seus logos e informações
    for i, jogo in enumerate(jogos):
        if i >= 3:  # Limitar a 3 jogos por imagem
            break
            
        equipe1 = jogo['Equipe 1']
        equipe2 = jogo['Equipe 2']
        categoria = jogo['Categoria']
        horario = jogo['Horário']
        
        # Calcular posição Y para este jogo
        jogo_y = y_pos + i * 280  # Espaçamento maior entre jogos
        
        # Obter as imagens dos times
        imagem_time1 = equipes_imagens.get(equipe1, 'default.jpg')
        image_path1 = os.path.join('image', imagem_time1)
        if not os.path.exists(image_path1):
            print(f"Imagem não encontrada para {equipe1}, usando default.jpg")
            image_path1 = os.path.join('image', 'default.jpg')
        
        imagem_time2 = equipes_imagens.get(equipe2, 'default.jpg')
        image_path2 = os.path.join('image', imagem_time2)
        if not os.path.exists(image_path2):
            print(f"Imagem não encontrada para {equipe2}, usando default.jpg")
            image_path2 = os.path.join('image', 'default.jpg')
        
        try:
            # Abrir e redimensionar as imagens dos times
            logo1 = Image.open(image_path1).convert("RGBA")
            logo1 = logo1.resize((180, 180))
            
            logo2 = Image.open(image_path2).convert("RGBA")
            logo2 = logo2.resize((180, 180))
            
            # Adicionar logos dos times
            background.paste(logo1, (250, jogo_y), logo1 if logo1.mode == 'RGBA' else None)
            background.paste(logo2, (650, jogo_y), logo2 if logo2.mode == 'RGBA' else None)
            
            # Adicionar "VS" entre os logos
            draw.text((540, jogo_y + 90), "VS", font=subtitle_font, fill=(255, 255, 255), anchor="mm")
            
            # Adicionar categoria e horário em fonte maior e mais destacada
            categoria_horario = f"{categoria} - {horario}"
            
            # Criar um retângulo semi-transparente para destacar a categoria e horário
            overlay = Image.new('RGBA', background.size, (0, 0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay)
            text_width = category_font.getbbox(categoria_horario)[2]
            overlay_draw.rectangle(
                [(540 - text_width//2 - 20, jogo_y + 190 - 10), 
                 (540 + text_width//2 + 20, jogo_y + 190 + 40)], 
                fill=(0, 0, 0, 128)
            )
            background = Image.alpha_composite(background.convert('RGBA'), overlay).convert('RGB')
            draw = ImageDraw.Draw(background)
            
            # Adicionar texto da categoria e horário
            draw.text((540, jogo_y + 190), categoria_horario, font=category_font, fill=(255, 215, 0), anchor="mt")
            
            # Adicionar linha separadora entre jogos
            if i < len(jogos) - 1 and i < 2:  # Não adicionar após o último jogo
                draw.line([(150, jogo_y + 240), (930, jogo_y + 240)], fill=(100, 100, 100), width=1)
                
        except Exception as e:
            print(f"Erro ao processar logos para {equipe1} vs {equipe2}: {e}")
    
    # Adicionar endereço do local na parte inferior
    y_pos = 900
    
    # Quebrar o endereço em múltiplas linhas se for muito longo
    endereco_linhas = textwrap.wrap(local, width=70)
    
    # Desenhar retângulo semi-transparente para o endereço
    overlay = Image.new('RGBA', background.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rectangle([(100, y_pos - 20), (980, y_pos + 30 * len(endereco_linhas))], fill=(0, 0, 0, 128))
    background = Image.alpha_composite(background.convert('RGBA'), overlay).convert('RGB')
    draw = ImageDraw.Draw(background)
    
    # Adicionar título "LOCAL"
    draw.text((540, y_pos - 40), "LOCAL", font=team_font, fill=(255, 215, 0), anchor="mt")
    
    # Adicionar endereço
    for linha in endereco_linhas:
        draw.text((540, y_pos), linha, font=address_font, fill=(255, 255, 255), anchor="mt")
        y_pos += 30
    
    # Adicionar rodapé
    draw.text((540, 1020), "FPB - Federação Paulista de Basketball", font=info_font, fill=(150, 150, 150), anchor="mt")
    
    # Criar nome do arquivo (usando parte do local para identificação)
    local_abreviado = local.split()[0].lower()
    filename = f"posts/proximos_jogos/jogos_{data.replace('/', '-')}_{local_abreviado}.jpg"
    
    # Salvar a imagem
    background.save(filename)
    print(f"Post de jogos no local '{local_abreviado}' para {data_formatada} criado com sucesso!")

# Executar a função para criar os posts
criar_posts_jogos_por_local()

print("Posts de próximos jogos por local gerados!")