import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os

# Criar a pasta 'resumo_times' se não existir
os.makedirs("resumo_times", exist_ok=True)
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
    'CLUBE PAINEIRAS DO MORUMBY': 'paineiras.png',
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
    'F.R. MIRASSOL,': 'mr.jpg', 
}
# Ler o CSV
df = pd.read_csv('data/partidas_normalizadas.csv', delimiter=",")
df = df.dropna(subset=["Equipe 1", "Equipe 2", "Placar", "Data"])
df["Data"] = pd.to_datetime(df["Data"], format="%d/%m/%Y")
df["Categoria"] = df["Categoria"].str.replace(" Masculino", "", regex=False)

# Obter times únicos
todos_times = pd.unique(df[["Equipe 1", "Equipe 2"]].values.ravel('K'))

# Configurações visuais
logo_size = (90, 90)
altura_total = 1920
largura_total = 1080
y_start = 150
espaco_por_jogo = 85

# Fontes
try:
    title_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 48)
    placar_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 36)
    categoria_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 28)
except:
    title_font = placar_font = categoria_font = ImageFont.load_default()

# Gerar o resumo de jogos por categoria para cada time
for time in todos_times:
    df_time = df[(df["Equipe 1"] == time) | (df["Equipe 2"] == time)].sort_values(by="Data")
    
    if df_time.empty:
        continue
    
    categorias = df_time["Categoria"].unique()

    for categoria in categorias:
        df_categoria = df_time[df_time["Categoria"] == categoria]

        background = Image.new('RGB', (largura_total, altura_total), color=(10, 10, 40))
        draw = ImageDraw.Draw(background)

        draw.text((largura_total // 2, 40), f"CATEGORIA: {categoria.upper()}", font=categoria_font, fill=(173, 216, 230), anchor="mt")

        for i, (_, row) in enumerate(df_categoria.iterrows()):
            if i >= 20:
                break
            y_pos = y_start + i * espaco_por_jogo

            equipe1 = row["Equipe 1"]
            equipe2 = row["Equipe 2"]
            placar_raw = str(row["Placar"]).strip()

            try:
                placar1, placar2 = map(int, placar_raw.replace("x", "-").split("-"))
            except ValueError:
                continue  # pula se o placar estiver mal formatado

            if equipe1 == time:
                adversario = equipe2
                placar_time, placar_rival = placar1, placar2
            else:
                adversario = equipe1
                placar_time, placar_rival = placar2, placar1

            # Cores do placar
            cor_time = (255, 215, 0) if placar_time > placar_rival else (255, 0, 0)
            cor_rival = (255, 215, 0) if placar_rival > placar_time else (255, 0, 0)

            # Logos
            logo_time = Image.open(os.path.join("image", equipes_imagens.get(time, "default.jpg"))).resize(logo_size)
            logo_rival = Image.open(os.path.join("image", equipes_imagens.get(adversario, "default.jpg"))).resize(logo_size)

            background.paste(logo_time, (150, y_pos))
            background.paste(logo_rival, (840, y_pos))

            # Placar centralizado
            placar_time_str = str(placar_time)
            placar_rival_str = str(placar_rival)
            x_str = "x"

            time_width = draw.textlength(placar_time_str, font=placar_font)
            x_width = draw.textlength(x_str, font=placar_font)
            rival_width = draw.textlength(placar_rival_str, font=placar_font)

            total_width = time_width + x_width + rival_width
            center_x = largura_total // 2
            y_text = y_pos + logo_size[1] // 2

            start_x = center_x - (total_width // 2)

            draw.text((start_x, y_text), placar_time_str, font=placar_font, fill=cor_time)
            draw.text((start_x + time_width, y_text), x_str, font=placar_font, fill=(255, 255, 255))
            draw.text((start_x + time_width + x_width, y_text), placar_rival_str, font=placar_font, fill=cor_rival)

        nome_arquivo = f"{time.lower().replace(' ', '_').replace('/', '').replace('.', '').replace('-', '')}_{categoria.lower().replace(' ', '_')}"
        filepath = f"resumo_times/{nome_arquivo}.jpg"
        background.save(filepath)
        print(f"Resumo do time '{time}' para a categoria '{categoria}' salvo como: {filepath}")
