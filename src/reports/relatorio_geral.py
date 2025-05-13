import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os
import numpy as np
from collections import defaultdict

# Criar a pasta 'posts' se não existir
os.makedirs("posts", exist_ok=True)

# Verificar se a pasta de imagens existe
if not os.path.exists('image'):
    print("Pasta 'image' não encontrada! Certifique-se de que as imagens estejam no diretório correto.")
    
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
    'A.A. MOGI DAS CRUZES': 'mogi.jpg',
    'INSTITUTO SUPERAÇÃO': 'super.png',
    'BAURU BASKET': 'bauru.jpg',
    'AABB LIMEIRA': 'aabb.jpg',
    'APAGEBASK / GUARULHOS': 'apage.png',
    'CLUBE PAINEIRAS DO MORUMBY': 'paineiras.jpg',
    'F.R. JANDIRA': 'overtime.jpg',
    'HIPICA CAMPINAS': 'hipica.jpg',
    'SESI-SP / FRANCA BASQUETE': 'sesi_franca.png',
    'CAC / CRAVINHOS BASKETBALL': 'cac.jpg',
    'F.R. MIRASSOL': 'mirassol.jpg',
    'F.R. TUPÃ': 'fbauru.jpg',
    'SOROCABA BASQUETE': 'sorocaba.jpg',
    'SANTANA DE PARNAÍBA/AJABASK': 'ajabask.jpg',
    'BASQUETE SANTOS / FUPES': 'santos.jpg',
    'SEMELP / PINDAMONHANGABA BASQUETE PINDA': 'semelp.jpg',
    'SL MANDIC BASQUETE': 'sl.jpg',
    'GRUPO BT/CLUBE DE CAMPO DE TATUI': 'tatui.jpg',
    'ARARAQUARA – ABA / FUNDESPORT': 'aba.jpg',
    'TIME JUNDIAI-JUNBASKET': 'jundiai.jpg',
    'F.R. MARILIA': 'sl.jpg',
    'MOGI BASQUETE': 'mogi1.jpg',
}

# Ler o CSV garantindo que o separador está correto
df = pd.read_csv('data/partidas_normalizadas.csv', delimiter=",").dropna(subset=["Equipe 1", "Equipe 2", "Placar"])
print(df.head())
# Filtrar as categorias e limpar os dados nulos
df.dropna(subset=['Categoria'], inplace=True)

# Função para calcular as estatísticas por categoria
def calcular_estatisticas_por_categoria():
    categorias = df['Categoria'].unique()
    estatisticas_por_categoria = {}

    for categoria in categorias:
        categoria_df = df[df['Categoria'] == categoria]
        estatisticas = {}
        
        # Calcular estatísticas por time
        times = pd.concat([categoria_df['Equipe 1'], categoria_df['Equipe 2']]).unique()
        
        for time in times:
            # Estatísticas do time
            time_df = categoria_df[(categoria_df['Equipe 1'] == time) | (categoria_df['Equipe 2'] == time)]
            
            vitorias = 0
            derrotas = 0
            jogos = 0
            pontos_pro = 0
            pontos_contra = 0
            
            for _, row in time_df.iterrows():
                jogos += 1
                # Verificar se o time venceu
                if (row['Equipe 1'] == time and int(row['Placar'].split('x')[0]) > int(row['Placar'].split('x')[1])) or \
                   (row['Equipe 2'] == time and int(row['Placar'].split('x')[1]) > int(row['Placar'].split('x')[0])):
                    vitorias += 1
                else:
                    derrotas += 1
                
                # Atualizar os pontos
                if row['Equipe 1'] == time:
                    pontos_pro += int(row['Placar'].split('x')[0])
                    pontos_contra += int(row['Placar'].split('x')[1])
                else:
                    pontos_pro += int(row['Placar'].split('x')[1])
                    pontos_contra += int(row['Placar'].split('x')[0])
            
            aproveitamento = (vitorias / jogos) * 100 if jogos > 0 else 0
            saldo_pontos = pontos_pro - pontos_contra
            
            estatisticas[time] = {
                'jogos': jogos,
                'vitorias': vitorias,
                'derrotas': derrotas,
                'aproveitamento': aproveitamento,
                'saldo_pontos': saldo_pontos
            }

        estatisticas_por_categoria[categoria] = estatisticas
    return estatisticas_por_categoria

# Função para criar o post de resumo da categoria
def criar_post_resumo_categoria(categoria, estatisticas):
    # Configurações da imagem
    largura = 1200
    altura = 900
    background = Image.new('RGB', (largura, altura), (0, 0, 0))
    draw = ImageDraw.Draw(background)
    
    # Adicionar título da categoria
    try:
        titulo_font = ImageFont.truetype("path/to/font.ttf", 40)
        stats_font = ImageFont.truetype("path/to/font.ttf", 30)
    except IOError:
        print("Fonte não encontrada, usando fonte padrão")
        titulo_font = ImageFont.load_default()
        stats_font = ImageFont.load_default()

    draw.text((10, 10), f"Classificação - {categoria}", font=titulo_font, fill=(255, 255, 255))
    
    # Adicionar cabeçalho
    draw.text((150, 50), "Equipe", font=stats_font, fill=(255, 255, 255))
    draw.text((540, 50), "Jogos", font=stats_font, fill=(255, 255, 255))
    draw.text((600, 50), "Vitórias", font=stats_font, fill=(255, 255, 255))
    draw.text((660, 50), "Derrotas", font=stats_font, fill=(255, 255, 255))
    draw.text((720, 50), "Aproveitamento", font=stats_font, fill=(255, 255, 255))
    draw.text((830, 50), "Saldo de Pontos", font=stats_font, fill=(255, 255, 255))

    # Adicionar estatísticas de cada time
    y_pos = 80
    for time, stats in estatisticas.items():
        try:
            nome_time = time
            # Adicionar logo da equipe
            logo_path = f'image/{equipes_imagens.get(time, "default_logo.png")}'  # Caminho da imagem
            if os.path.exists(logo_path):
                logo = Image.open(logo_path)
                logo.thumbnail((40, 40))  # Redimensionar logo para caber na imagem
                background.paste(logo, (100, y_pos - 10))  # Ajuste a posição do logo
            else:
                print(f"Logo não encontrado para {time}, utilizando logo padrão.")
                logo_path = 'image/default_logo.png'  # Caminho para o logo padrão
                if os.path.exists(logo_path):
                    logo = Image.open(logo_path)
                    logo.thumbnail((40, 40))  # Redimensionar logo para caber na imagem
                    background.paste(logo, (100, y_pos - 10))  # Ajuste a posição do logo
                else:
                    print(f"Logo padrão também não encontrado. Usando um espaço em branco.")
                    # Criar um logo em branco (opcional)
                    default_logo = Image.new('RGB', (40, 40), (255, 255, 255))  # Branco
                    background.paste(default_logo, (100, y_pos - 10))

            # Adicionar texto com as estatísticas
            draw.text((150, y_pos), nome_time, font=stats_font, fill=(255, 255, 255))
            draw.text((540, y_pos), str(stats['jogos']), font=stats_font, fill=(255, 255, 255))
            draw.text((600, y_pos), str(stats['vitorias']), font=stats_font, fill=(255, 255, 255))
            draw.text((660, y_pos), str(stats['derrotas']), font=stats_font, fill=(255, 255, 255))
            draw.text((720, y_pos), f"{stats['aproveitamento']:.2f}%", font=stats_font, fill=(255, 255, 255))
            draw.text((830, y_pos), str(stats['saldo_pontos']), font=stats_font, fill=(255, 255, 255))
            y_pos += 60  # Ajustar o espaçamento entre as linhas
        except Exception as e:
            print(f"Erro ao adicionar dados de {time}: {e}")

    # Salvar imagem
    output_file = f"posts/classificacao_{categoria}.png"
    background.save(output_file)
    print(f"Post criado para a categoria {categoria}: {output_file}")
