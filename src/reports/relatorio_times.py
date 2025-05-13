import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os

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
}
# Ler o CSV
df = pd.read_csv('data/partidas_normalizadas.csv', delimiter=",")
df = df.dropna(subset=["Equipe 1", "Equipe 2", "Placar", "Data"])

# Converter coluna de data para datetime
df["Data"] = pd.to_datetime(df["Data"], format="%d/%m/%Y")

# Remover "Masculino" da coluna Categoria
df["Categoria"] = df["Categoria"].str.replace(" Masculino", "", regex=False)

# Criar posts para cada combinação única de data e categoria
for (data, categoria), df_filtrado in df.groupby(["Data", "Categoria"]):
    partidas = df_filtrado.reset_index(drop=True)
    total_partidas = len(partidas)
    
    # Dividir em páginas se houver mais de 6 jogos
    num_paginas = (total_partidas - 1) // 6 + 1

    for pagina in range(num_paginas):
        background = Image.new('RGB', (1080, 1080), color=(0, 0, 51))
        draw = ImageDraw.Draw(background)

        try:
            title_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 50)
            info_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 24)
        except:
            title_font = ImageFont.load_default()
            info_font = ImageFont.load_default()

        draw.text((540, 30), f"CATEGORIA: {categoria.upper()}", font=info_font, fill=(173, 216, 230), anchor="mt")
        draw.text((540, 80), "BASQUETE FPB", font=title_font, fill=(255, 255, 255), anchor="mt")
        draw.text((540, 150), f"Jogos - {data.strftime('%d/%m/%Y')}", font=title_font, fill=(255, 215, 0), anchor="mt")

        y_start = 210
        y_spacing = 135  # espaçamento vertical entre partidas
        logo_size = (140, 140)

        # Definir quais partidas entram nesta página
        inicio = pagina * 6
        fim = min(inicio + 6, total_partidas)

        for i in range(inicio, fim):
            row = partidas.iloc[i]
            y_pos = y_start + (i - inicio) * y_spacing

            equipe1, equipe2, placar = row["Equipe 1"], row["Equipe 2"], row["Placar"]
            placar = str(placar).strip()

            img1 = Image.open(os.path.join('image', equipes_imagens.get(equipe1, 'default.jpg'))).resize(logo_size)
            img2 = Image.open(os.path.join('image', equipes_imagens.get(equipe2, 'default.jpg'))).resize(logo_size)

            background.paste(img1, (220, y_pos))
            background.paste(img2, (720, y_pos))

            draw.text((540, y_pos + logo_size[1] // 2), placar, font=title_font, fill=(255, 215, 0), anchor="mm")

        # Nome do arquivo com índice da página se necessário
        categoria_slug = categoria.replace(" ", "_").lower()
        pagina_str = f"_p{pagina+1}" if num_paginas > 1 else ""
        filename = f"posts/Jogos_{data.strftime('%d-%m-%Y')}_{categoria_slug}{pagina_str}.jpg"
        background.save(filename)
        print(f"Post {filename} criado com sucesso!")