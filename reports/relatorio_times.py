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
    'A.D. CENTRO OLIMPICO': 'adcentrool.jpg',
    'CFE TAUBATE / IGC / LBCP': 'taubate.jpg',
    'CLUBE DE CAMPO DE RIO CLARO - CCRC': 'rioclaro.jpg',
    'A.A. MOGI DAS CRUZES': 'mogi.jpg',
    'INSTITUTO SUPERAÇÃO':'super.png',
    'BAURU BASKET': 'bauru.jpg',
    'AABB LIMEIRA': 'aabb.jpg',
    'APAGEBASK / GUARULHOS': 'apage.png',
    'CLUBE PAINEIRAS DO MORUMBY': 'paineiras.jpg',
    'F.R. JANDIRA': 'overtime.jpg',
    'HIPICA CAMPINAS': 'hipica.jpg',
    'SESI-SP / FRANCA BASQUETE' : 'sesi_franca.png',
    'CAC / CRAVINHOS BASKETBALL' : 'cac.jpg',
    'F.R. MIRASSOL' : 'mirassol.jpg',
    'F.R. TUPÃ' : 'fbauru.jpg', 
    'SOROCABA BASQUETE': 'sorocaba.jpg',
    'SANTANA DE PARNAÍBA/AJABASK': 'ajabask.jpg',
    'BASQUETE SANTOS / FUPES' : 'santos.jpg',
    'SEMELP / PINDAMONHANGABA BASQUETE PINDA' : 'semelp.jpg',
    'SL MANDIC BASQUETE' : 'sl.jpg' ,
    'GRUPO BT/CLUBE DE CAMPO DE TATUI' : 'tatui.jpg', 
    'ARARAQUARA – ABA / FUNDESPORT' : 'aba.jpg',
    'TIME JUNDIAI-JUNBASKET' : 'jundiai.jpg', 
    'F.R. MARILIA': 'sl.jpg', 
    'MOGI BASQUETE' : 'mogi1.jpg' , 
}

# Ler o CSV garantindo que o separador está correto
df = pd.read_csv('data/partidas_normalizadas.csv', delimiter=",").dropna(subset=["Equipe 1", "Equipe 2", "Placar"])

# Função para calcular estatísticas gerais por gênero
def calcular_estatisticas_gerais_por_genero():
    # Dicionários para armazenar estatísticas por gênero
    estatisticas_masculino = defaultdict(lambda: {
        'jogos': 0, 'vitorias': 0, 'derrotas': 0, 
        'pontos_marcados': 0, 'pontos_sofridos': 0
    })
    
    estatisticas_feminino = defaultdict(lambda: {
        'jogos': 0, 'vitorias': 0, 'derrotas': 0, 
        'pontos_marcados': 0, 'pontos_sofridos': 0
    })
    
    # Processar cada partida
    for _, row in df.iterrows():
        equipe1 = row['Equipe 1']
        equipe2 = row['Equipe 2']
        placar = row['Placar']
        categoria = row['Categoria']
        
        # Determinar o gênero da categoria
        genero = "Masculino" if "Masculino" in categoria else "Feminino"
        
        # Escolher o dicionário correto com base no gênero
        estatisticas = estatisticas_masculino if genero == "Masculino" else estatisticas_feminino
        
        # Verificar se o placar está no formato esperado
        if 'X' in placar:
            try:
                placar_parts = placar.split('X')
                pontos1 = int(placar_parts[0].strip())
                pontos2 = int(placar_parts[1].strip())
                
                # Registrar jogo para ambas as equipes
                estatisticas[equipe1]['jogos'] += 1
                estatisticas[equipe2]['jogos'] += 1
                
                # Registrar pontos
                estatisticas[equipe1]['pontos_marcados'] += pontos1
                estatisticas[equipe2]['pontos_marcados'] += pontos2
                estatisticas[equipe1]['pontos_sofridos'] += pontos2
                estatisticas[equipe2]['pontos_sofridos'] += pontos1
                
                # Determinar vencedor
                if pontos1 > pontos2:
                    estatisticas[equipe1]['vitorias'] += 1
                    estatisticas[equipe2]['derrotas'] += 1
                elif pontos2 > pontos1:
                    estatisticas[equipe2]['vitorias'] += 1
                    estatisticas[equipe1]['derrotas'] += 1
            except:
                # Ignorar placares que não podem ser convertidos para números
                pass
    
    # Converter para listas de dicionários e calcular estatísticas adicionais
    resultado_masculino = []
    for equipe, stats in estatisticas_masculino.items():
        if stats['jogos'] > 0:
            aproveitamento = (stats['vitorias'] / stats['jogos']) * 100
            saldo_pontos = stats['pontos_marcados'] - stats['pontos_sofridos']
            
            resultado_masculino.append({
                'equipe': equipe,
                'jogos': stats['jogos'],
                'vitorias': stats['vitorias'],
                'derrotas': stats['derrotas'],
                'aproveitamento': aproveitamento,
                'pontos_marcados': stats['pontos_marcados'],
                'pontos_sofridos': stats['pontos_sofridos'],
                'saldo_pontos': saldo_pontos
            })
    
    resultado_feminino = []
    for equipe, stats in estatisticas_feminino.items():
        if stats['jogos'] > 0:
            aproveitamento = (stats['vitorias'] / stats['jogos']) * 100
            saldo_pontos = stats['pontos_marcados'] - stats['pontos_sofridos']
            
            resultado_feminino.append({
                'equipe': equipe,
                'jogos': stats['jogos'],
                'vitorias': stats['vitorias'],
                'derrotas': stats['derrotas'],
                'aproveitamento': aproveitamento,
                'pontos_marcados': stats['pontos_marcados'],
                'pontos_sofridos': stats['pontos_sofridos'],
                'saldo_pontos': saldo_pontos
            })
    
    # Ordenar por número de vitórias (decrescente)
    resultado_masculino.sort(key=lambda x: (x['vitorias'], x['saldo_pontos']), reverse=True)
    resultado_feminino.sort(key=lambda x: (x['vitorias'], x['saldo_pontos']), reverse=True)
    
    return resultado_masculino, resultado_feminino

# Função para criar o post de resumo geral por gênero
def criar_post_resumo_geral(estatisticas, genero):
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
    draw.text((540, 120), f"CLASSIFICAÇÃO GERAL - {genero}", font=subtitle_font, fill=(255, 215, 0), anchor="mt")  # Dourado
    
    # Determinar quantos times mostrar (máximo 15)
    num_times = min(len(estatisticas), 15)
    
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
    
    # Altura de cada linha da tabela (reduzida para caber mais times)
    row_height = 60
    
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
            logo = logo.resize((50, 50))  # Tamanho reduzido para caber mais times
            
            # Adicionar logo do time
            background.paste(logo, (110, y_pos - 25), logo if logo.mode == 'RGBA' else None)
            
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
                draw.line([(100, y_pos + 25), (980, y_pos + 25)], fill=(100, 100, 100), width=1)
                
        except Exception as e:
            print(f"Erro ao processar estatísticas para {equipe}: {e}")
    
    # Adicionar rodapé
    draw.text((540, 1020), "FPB - Federação Paulista de Basketball", font=info_font, fill=(150, 150, 150), anchor="mt")
    
    # Criar nome do arquivo
    filename = f"posts/classificacao_geral_{genero}.jpg"
    
    # Salvar a imagem
    background.save(filename)
    print(f"Post de classificação geral para {genero} criado com sucesso!")

# Calcular estatísticas gerais por gênero
estatisticas_masculino, estatisticas_feminino = calcular_estatisticas_gerais_por_genero()

# Criar posts de classificação geral por gênero
if estatisticas_masculino:
    criar_post_resumo_geral(estatisticas_masculino, "Masculino")

if estatisticas_feminino:
    criar_post_resumo_geral(estatisticas_feminino, "Feminino")

print("Posts de classificação geral por gênero gerados!")