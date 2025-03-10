from collections import defaultdict
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os
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
df = pd.read_csv('data/proximas_partidas_normalizadas.csv', delimiter=",")

# Função para formatar a data
def formatar_data(data_str):
    try:
        data_obj = datetime.strptime(data_str, '%d/%m/%Y')
        meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 
                'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
        return f"{data_obj.day} de {meses[data_obj.month-1]}"
    except:
        return data_str

# Função para abreviar nomes longos de equipes
def abreviar_nome(nome, max_len=25):
    if len(nome) > max_len:
        palavras = nome.split()
        abreviado = []
        for palavra in palavras:
            if len(palavra) > 3:
                abreviado.append(palavra[:3] + ".")
            else:
                abreviado.append(palavra)
        return " ".join(abreviado)
    return nome

# Função para ajustar a fonte do nome do time para que não ultrapasse a largura
def ajustar_tamanho_texto(draw, texto, font, largura_maxima):
    largura_texto, _ = draw.textbbox((0, 0), texto, font=font)[2:4]
    if largura_texto > largura_maxima:
        # Reduzir a fonte até o texto caber na largura máxima
        while largura_texto > largura_maxima:
            font = ImageFont.truetype(font.path, font.size - 1)  # Diminuir tamanho da fonte
            largura_texto, _ = draw.textbbox((0, 0), texto, font=font)[2:4]
    return font

# Função para criar posts de jogos por local
def criar_posts_jogos_por_local():
    jogos_por_local_data = defaultdict(list)
    
    for _, row in df.iterrows():
        local = row['Local']
        data = row['Data']
        if pd.notna(local) and local.strip() != '' and pd.notna(data) and data.strip() != '':
            chave = (local, data)
            jogos_por_local_data[chave].append(row)
    
    for (local, data), jogos in jogos_por_local_data.items():
        criar_post_local_data(local, data, jogos)

def criar_post_local_data(local, data, jogos): 
    background = Image.new('RGB', (1080, 1080), color=(0, 0, 51))
    
    try:
        logo_aa = Image.open('image/aa.jpg').convert("RGBA")
        logo_aa = logo_aa.resize((120, 120))  # Aumentando o logo
        background.paste(logo_aa, (950, 20), logo_aa if logo_aa.mode == 'RGBA' else None)
    except Exception as e:
        print(f"Erro ao carregar logo AA: {e}")

    draw = ImageDraw.Draw(background)

    try:
        title_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 50)
        date_title_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 60)
        team_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 42)
        category_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 38)
        address_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Italic.ttf', 36)
    except:
        title_font = ImageFont.load_default()
        date_title_font = ImageFont.load_default()
        team_font = ImageFont.load_default()
        category_font = ImageFont.load_default()
        address_font = ImageFont.load_default()

    # Título
    draw.text((540, 40), "BASQUETE FPB", font=title_font, fill=(255, 255, 255), anchor="mt")

    # Data em destaque com fundo
    data_formatada = formatar_data(data)
    data_text = f"JOGOS {data_formatada.upper()}"

    # Criar retângulo para a data
    text_bbox = draw.textbbox((0, 0), data_text, font=date_title_font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Desenhar retângulo para a data
    overlay = Image.new('RGBA', background.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rectangle(
        [(540 - text_width//2 - 20, 120 - 10), 
         (540 + text_width//2 + 20, 120 + text_height + 10)], 
        fill=(0, 0, 128, 180)
    )
    background = Image.alpha_composite(background.convert('RGBA'), overlay).convert('RGB')
    draw = ImageDraw.Draw(background)

    # Texto da data
    draw.text((540, 120), data_text, font=date_title_font, fill=(255, 215, 0), anchor="mt")

    # Agrupar jogos por confronto (times únicos)
    times_vistos = set()

    # Jogos
    y_offset = 230
    for i, jogo in enumerate(jogos):
        if i >= 8:  # Limitar a 8 jogos por imagem
            break

        equipe1 = jogo['Equipe 1']
        equipe2 = jogo['Equipe 2']

        # Verificar se este par de times já foi mostrado
        par_times = frozenset([equipe1, equipe2])
        if par_times in times_vistos:
            continue

        times_vistos.add(par_times)

        equipe1_abrev = abreviar_nome(equipe1)
        equipe2_abrev = abreviar_nome(equipe2)
        categoria = jogo['Categoria']
        horario = jogo['Horário']

        # Fundo para cada jogo
        overlay = Image.new('RGBA', background.size, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.rectangle(
            [(100, y_offset - 10), (980, y_offset + 90)], 
            fill=(0, 0, 0, 128)
        )
        background = Image.alpha_composite(background.convert('RGBA'), overlay).convert('RGB')
        draw = ImageDraw.Draw(background)

        # Tentar carregar logos dos times
        try:
            # Time 1
            imagem_time1 = equipes_imagens.get(equipe1, 'default.jpg')
            image_path1 = os.path.join('image', imagem_time1)
            if os.path.exists(image_path1):
                logo1 = Image.open(image_path1).convert("RGBA")
                logo1 = logo1.resize((80, 80))  # Ajustando tamanho
                background.paste(logo1, (120, y_offset), logo1 if logo1.mode == 'RGBA' else None)
        except:
            pass

        try:
            # Time 2
            imagem_time2 = equipes_imagens.get(equipe2, 'default.jpg')
            image_path2 = os.path.join('image', imagem_time2)
            if os.path.exists(image_path2):
                logo2 = Image.open(image_path2).convert("RGBA")
                logo2 = logo2.resize((80, 80))  # Ajustando tamanho
                background.paste(logo2, (890, y_offset), logo2 if logo2.mode == 'RGBA' else None)
        except:
            pass

        # Ajustar tamanho do nome do time
        team_font_adjusted = ajustar_tamanho_texto(draw, f"{equipe1_abrev} x {equipe2_abrev}", team_font, 800)

        # Texto do confronto
        texto_jogo = f"{equipe1_abrev} x {equipe2_abrev}"
        draw.text((540, y_offset + 20), texto_jogo, font=team_font_adjusted, fill=(255, 255, 255), anchor="mt")

        # Exibir categorias e horários abaixo
        texto_categoria = f"{categoria} - {horario}"
        cat_font_adjusted = ajustar_tamanho_texto(draw, texto_categoria, category_font, 800)
        draw.text((540, y_offset + 65), texto_categoria, font=cat_font_adjusted, fill=(255, 215, 0), anchor="mt")

        y_offset += 110

    # Local com fundo
    endereco_linhas = textwrap.wrap(local, width=50)

    # Retângulo para o local
    overlay = Image.new('RGBA', background.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rectangle(
        [(100, 900 - 10), (980, 900 + 40 * len(endereco_linhas) + 10)], 
        fill=(0, 0, 128, 180)
    )
    background = Image.alpha_composite(background.convert('RGBA'), overlay).convert('RGB')
    draw = ImageDraw.Draw(background)

    # Título "LOCAL"
    draw.text((540, 860), "LOCAL", font=team_font, fill=(255, 215, 0), anchor="mt")

    # Texto do local
    for i, linha in enumerate(endereco_linhas):
        draw.text((540, 900 + i * 40), linha, font=address_font, fill=(255, 255, 255), anchor="mt")

    # Rodapé
    draw.text((540, 1030), "FPB - Federação Paulista de Basketball", font=category_font, fill=(150, 150, 150), anchor="mt")

    # Salvar imagem
    local_abreviado = local.split()[0].lower()
    nome_arquivo = f"posts/proximos_jogos/jogos_{data.replace('/', '-')}_{local_abreviado}.jpg"
    background.save(nome_arquivo)

    print(f"Post de jogos no local '{local_abreviado}' para {formatar_data(data)} criado com sucesso!")

criar_posts_jogos_por_local()
