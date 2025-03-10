import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os
import numpy as np
from collections import defaultdict

# Criar a pasta 'posts' se não existir
os.makedirs("posts", exist_ok=True)

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
    'A.D. CENTRO OLIMPICO' : 'adcentrool.jpg',
    'CFE TAUBATE / IGC / LBCP' : 'taubate.jpg',
    'CLUBE DE CAMPO DE RIO CLARO - CCRC' : 'rioclaro.jpg'
}

# Ler o CSV garantindo que o separador está correto
df = pd.read_csv('data/partidas_normalizadas.csv', delimiter=",").dropna(subset=["Equipe 1", "Equipe 2", "Placar"])

# Função para calcular estatísticas de vitórias por time, separadas por categoria
def calcular_estatisticas_por_categoria():
    # Dicionário para armazenar estatísticas por categoria
    estatisticas_por_categoria = {}
    
    # Obter todas as categorias
    categorias = df['Categoria'].unique()
    
    for categoria in categorias:
        # Filtrar partidas desta categoria
        df_categoria = df[df['Categoria'] == categoria]
        
        # Dicionários para armazenar estatísticas
        vitorias = defaultdict(int)
        derrotas = defaultdict(int)
        pontos_marcados = defaultdict(int)
        pontos_sofridos = defaultdict(int)
        jogos = defaultdict(int)
        
        # Processar cada partida
        for _, row in df_categoria.iterrows():
            equipe1 = row['Equipe 1']
            equipe2 = row['Equipe 2']
            placar = row['Placar']
            
            # Verificar se o placar está no formato esperado
            if 'X' in placar:
                try:
                    placar_parts = placar.split('X')
                    pontos1 = int(placar_parts[0].strip())
                    pontos2 = int(placar_parts[1].strip())
                    
                    # Registrar jogo para ambas as equipes
                    jogos[equipe1] += 1
                    jogos[equipe2] += 1
                    
                    # Registrar pontos
                    pontos_marcados[equipe1] += pontos1
                    pontos_marcados[equipe2] += pontos2
                    pontos_sofridos[equipe1] += pontos2
                    pontos_sofridos[equipe2] += pontos1
                    
                    # Determinar vencedor
                    if pontos1 > pontos2:
                        vitorias[equipe1] += 1
                        derrotas[equipe2] += 1
                    elif pontos2 > pontos1:
                        vitorias[equipe2] += 1
                        derrotas[equipe1] += 1
                except:
                    # Ignorar placares que não podem ser convertidos para números
                    pass
        
        # Calcular estatísticas adicionais
        estatisticas = []
        for equipe in set(list(jogos.keys())):
            if jogos[equipe] > 0:
                aproveitamento = (vitorias[equipe] / jogos[equipe]) * 100
                saldo_pontos = pontos_marcados[equipe] - pontos_sofridos[equipe]
                
                estatisticas.append({
                    'equipe': equipe,
                    'jogos': jogos[equipe],
                    'vitorias': vitorias[equipe],
                    'derrotas': derrotas[equipe],
                    'aproveitamento': aproveitamento,
                    'pontos_marcados': pontos_marcados[equipe],
                    'pontos_sofridos': pontos_sofridos[equipe],
                    'saldo_pontos': saldo_pontos
                })
        
        # Ordenar por número de vitórias (decrescente)
        estatisticas.sort(key=lambda x: (x['vitorias'], x['saldo_pontos']), reverse=True)
        
        # Armazenar estatísticas desta categoria
        estatisticas_por_categoria[categoria] = estatisticas
    
    return estatisticas_por_categoria

# Função para criar o post de resumo de vitórias por categoria
def criar_post_resumo_categoria(categoria, estatisticas):
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
        subtitle_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 36)
        team_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 24)
        stats_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 22)
        info_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 24)
    except:
        # Fallback para fonte padrão se não encontrar
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        team_font = ImageFont.load_default()
        stats_font = ImageFont.load_default()
        info_font = ImageFont.load_default()
    
    # Adicionar título
    draw.text((540, 50), "BASQUETE FPB", font=title_font, fill=(255, 255, 255), anchor="mt")
    
    # Adicionar subtítulo
    draw.text((540, 120), f"CLASSIFICAÇÃO - {categoria}", font=subtitle_font, fill=(255, 215, 0), anchor="mt")  # Dourado
    
    # Determinar quantos times mostrar (máximo 10)
    num_times = min(len(estatisticas), 10)
    
    # Altura inicial para começar a desenhar as estatísticas
    y_start = 180
    
    # Desenhar cabeçalho da tabela
    header_y = y_start + 20
    draw.text((150, header_y), "Time", font=team_font, fill=(255, 255, 255))
    draw.text((540, header_y), "J", font=team_font, fill=(255, 255, 255))
    draw.text((600, header_y), "V", font=team_font, fill=(255, 255, 255))
    draw.text((660, header_y), "D", font=team_font, fill=(255, 255, 255))
    draw.text((720, header_y), "Aprov.", font=team_font, fill=(255, 255, 255))
    draw.text((830, header_y), "Saldo", font=team_font, fill=(255, 255, 255))
    
    # Desenhar linha separadora
    draw.line([(100, header_y + 30), (980, header_y + 30)], fill=(150, 150, 150), width=2)
    
    # Altura de cada linha da tabela
    row_height = 80

    # Adicionar mais espaço antes do primeiro time
    first_team_offset = 40  # Espaço adicional antes do primeiro time
    
    # Desenhar estatísticas para cada time
    for i in range(num_times):
        stats = estatisticas[i]
        equipe = stats['equipe']
        
        # Calcular posição Y para esta linha
        y_pos = y_start + 60 + first_team_offset + i * row_height
        
        # Obter a imagem do time
        imagem_time = equipes_imagens.get(equipe, 'default.jpg')
        image_path = os.path.join('image', imagem_time)
        if not os.path.exists(image_path):
            print(f"Imagem não encontrada para {equipe}, usando default.jpg")
            image_path = os.path.join('image', 'default.jpg')
        
        try:
            # Abrir e redimensionar a imagem do time
            logo = Image.open(image_path).convert("RGBA")
            logo = logo.resize((60, 60))
            
            # Adicionar logo do time
            background.paste(logo, (110, y_pos - 30), logo if logo.mode == 'RGBA' else None)
            
            # Abreviar nome do time se for muito longo
            nome_time = equipe
            if len(nome_time) > 25:
                palavras = nome_time.split()
                nome_abreviado = []
                for palavra in palavras:
                    if len(palavra) > 3:
                        nome_abreviado.append(palavra[:3] + ".")
                    else:
                        nome_abreviado.append(palavra)
                nome_time = " ".join(nome_abreviado)
            
            # Adicionar nome do time
            draw.text((180, y_pos), nome_time, font=stats_font, fill=(255, 255, 255))
            
            # Adicionar estatísticas
            draw.text((540, y_pos), str(stats['jogos']), font=stats_font, fill=(255, 255, 255), anchor="mt")
            draw.text((600, y_pos), str(stats['vitorias']), font=stats_font, fill=(0, 255, 0), anchor="mt")  # Verde para vitórias
            draw.text((660, y_pos), str(stats['derrotas']), font=stats_font, fill=(255, 0, 0), anchor="mt")  # Vermelho para derrotas
            draw.text((720, y_pos), f"{stats['aproveitamento']:.1f}%", font=stats_font, fill=(255, 255, 255), anchor="mt")
            
            # Saldo de pontos com cor baseada no valor
            saldo_cor = (0, 255, 0) if stats['saldo_pontos'] > 0 else (255, 0, 0) if stats['saldo_pontos'] < 0 else (255, 255, 255)
            saldo_texto = f"+{stats['saldo_pontos']}" if stats['saldo_pontos'] > 0 else str(stats['saldo_pontos'])
            draw.text((830, y_pos), saldo_texto, font=stats_font, fill=saldo_cor, anchor="mt")
            
            # Desenhar linha separadora
            if i < num_times - 1:
                draw.line([(100, y_pos + 30), (980, y_pos + 30)], fill=(100, 100, 100), width=1)
                
        except Exception as e:
            print(f"Erro ao processar estatísticas para {equipe}: {e}")
    
    # Adicionar rodapé
    draw.text((540, 1020), "FPB - Federação Paulista de Basketball", font=info_font, fill=(150, 150, 150), anchor="mt")
    
    # Criar nome do arquivo
    filename = f"posts/classificacao_{categoria.replace(' ', '_')}.jpg"
    
    # Salvar a imagem
    background.save(filename)
    print(f"Post de classificação para {categoria} criado com sucesso!")

# Calcular estatísticas por categoria
estatisticas_por_categoria = calcular_estatisticas_por_categoria()

# Criar posts de classificação para cada categoria
for categoria, estatisticas in estatisticas_por_categoria.items():
    if estatisticas:  # Verificar se há estatísticas para esta categoria
        criar_post_resumo_categoria(categoria, estatisticas)

print("Posts de classificação por categoria gerados!")