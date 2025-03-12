import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os
import numpy as np

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

# Função para criar o post com os dois times
def create_match_post(rows, categoria):
    # Pegar a data da primeira partida para o título
    data_jogo = rows[0]['Data'] if rows else "Data não disponível"
    
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
        category_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 40)
        date_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 36)
        score_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 36)
        info_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 24)
    except:
        # Fallback para fonte padrão se não encontrar
        title_font = ImageFont.load_default()
        category_font = ImageFont.load_default()
        date_font = ImageFont.load_default()
        score_font = ImageFont.load_default()
        info_font = ImageFont.load_default()
    
    # Adicionar título
    draw.text((540, 50), "BASQUETE FPB", font=title_font, fill=(255, 255, 255), anchor="mt")
    
    # Adicionar categoria e data
    draw.text((540, 120), f"{categoria} - {data_jogo}", font=category_font, fill=(255, 215, 0), anchor="mt")  # Dourado
    
    # Calcular quantas partidas podemos mostrar (máximo 4)
    num_partidas = min(len(rows), 4)
    
    # Altura inicial para começar a desenhar as partidas
    y_start = 200
    
    # Altura de cada bloco de partida
    partida_height = 200
    
    for i in range(num_partidas):
        row = rows[i]
        
        # Calcular posição Y para esta partida
        y_pos = y_start + i * partida_height
        
        # Obter as imagens dos times
        equipe1 = row['Equipe 1']
        equipe2 = row['Equipe 2']
        
        # Obter a imagem do time 1
        imagem_time1 = equipes_imagens.get(equipe1, 'default.jpg')
        image_path1 = os.path.join('image', imagem_time1)
        if not os.path.exists(image_path1):
            print(f"Imagem não encontrada para {equipe1}, usando default.jpg")
            image_path1 = os.path.join('image', 'default.jpg')
        
        # Obter a imagem do time 2
        imagem_time2 = equipes_imagens.get(equipe2, 'default.jpg')
        image_path2 = os.path.join('image', imagem_time2)
        if not os.path.exists(image_path2):
            print(f"Imagem não encontrada para {equipe2}, usando default.jpg")
            image_path2 = os.path.join('image', 'default.jpg')
        
        try:
            # Abrir e redimensionar as imagens dos times
            logo1 = Image.open(image_path1).convert("RGBA")
            logo1 = logo1.resize((200, 200))
            
            logo2 = Image.open(image_path2).convert("RGBA")
            logo2 = logo2.resize((200, 200))
            
            # Adicionar logos dos times
            background.paste(logo1, (200, y_pos), logo1 if logo1.mode == 'RGBA' else None)
            background.paste(logo2, (680, y_pos), logo2 if logo2.mode == 'RGBA' else None)
            
            # Extrair placar
            placar = row['Placar']
            if 'X' in placar:
                placar_parts = placar.split('X')
                placar1 = placar_parts[0].strip()
                placar2 = placar_parts[1].strip()
            else:
                placar1 = "?"
                placar2 = "?"
            
            # Adicionar placar entre os logos
            placar_text = f"{placar1} X {placar2}"
            placar_width = score_font.getbbox(placar_text)[2]
            
            # Desenhar um círculo ou retângulo arredondado para o placar
            circle_center = (540, y_pos + 100)
            circle_radius = max(placar_width // 2 + 20, 60)  # Garantir um tamanho mínimo
            
            # Desenhar um círculo com fundo semi-transparente
            overlay = Image.new('RGBA', background.size, (0, 0, 0, 0))
            draw_overlay = ImageDraw.Draw(overlay)
            draw_overlay.ellipse(
                (circle_center[0] - circle_radius, circle_center[1] - circle_radius,
                 circle_center[0] + circle_radius, circle_center[1] + circle_radius),
                fill=(0, 0, 0, 128)
            )
            background = Image.alpha_composite(background.convert('RGBA'), overlay).convert('RGB')
            draw = ImageDraw.Draw(background)
            
            # Adicionar o placar no centro
            draw.text((540, y_pos + 100), placar_text, font=score_font, fill=(255, 215, 0), anchor="mm")
            
        except Exception as e:
            print(f"Erro ao processar partida {equipe1} vs {equipe2}: {e}")
    
    # Adicionar rodapé
    draw.text((540, 1020), "FPB - Federação Paulista de Basketball", font=info_font, fill=(150, 150, 150), anchor="mt")
    
    # Criar nome do arquivo
    filename = f"posts/categoria_{categoria.replace(' ', '_')}_{data_jogo.replace('/', '-')}.jpg"
    
    # Salvar a imagem
    background.save(filename)
    print(f"Post da categoria {categoria} criado com sucesso!")

# Agrupar partidas por categoria
categorias = df['Categoria'].unique()

for categoria in categorias:
    # Filtrar partidas desta categoria
    partidas_categoria = df[df['Categoria'] == categoria].to_dict('records')
    
    # Criar post para esta categoria
    if partidas_categoria:
        create_match_post(partidas_categoria, categoria)

print("Todos os posts foram gerados!")