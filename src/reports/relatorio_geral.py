import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os

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

# Ler o CSV e garantir que as categorias que podem ser "nan" sejam tratadas
df = pd.read_csv('data/partidas_normalizadas.csv', delimiter=",").dropna(subset=["Equipe 1", "Equipe 2", "Placar"])

# Não remover as linhas com "nan" na categoria, mas substituir por um valor padrão (se necessário)
df['Categoria'].fillna('Categoria Desconhecida', inplace=True)

# Função para calcular as estatísticas gerais do campeonato, divididas por categoria
def calcular_estatisticas_por_categoria():
    estatisticas_por_categoria = {}

    # Separar os times por categoria
    categorias = df['Categoria'].unique()

    for categoria in categorias:
        estatisticas = {}
        
        # Filtrar partidas para a categoria
        df_categoria = df[df['Categoria'] == categoria]
        
        # Calcular estatísticas por time
        times = pd.concat([df_categoria['Equipe 1'], df_categoria['Equipe 2']]).unique()
        
        for time in times:
            # Estatísticas do time
            time_df = df_categoria[(df_categoria['Equipe 1'] == time) | (df_categoria['Equipe 2'] == time)]
            
            vitorias = 0
            derrotas = 0
            jogos = 0
            pontos_pro = 0
            pontos_contra = 0
            
            for _, row in time_df.iterrows():
                jogos += 1
                if (row['Equipe 1'] == time and int(row['Placar'].split('x')[0]) > int(row['Placar'].split('x')[1])) or \
                   (row['Equipe 2'] == time and int(row['Placar'].split('x')[1]) > int(row['Placar'].split('x')[0])):
                    vitorias += 1
                else:
                    derrotas += 1
                
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

        # Ordenar os times por vitórias e saldo de pontos
        estatisticas_ordenadas = sorted(estatisticas.items(), key=lambda x: (-x[1]['vitorias'], -x[1]['saldo_pontos']))
        
        # Adicionar à lista de estatísticas por categoria
        estatisticas_por_categoria[categoria] = estatisticas_ordenadas[:20]  # Limitar a 20 times por categoria
    
    return estatisticas_por_categoria

# Função para criar o post de classificação por categoria
def criar_post_classificacao_categoria(estatisticas_por_categoria):
    for categoria, estatisticas in estatisticas_por_categoria.items():
        largura = 1200
        altura = 900
        background = Image.new('RGB', (largura, altura), (0, 0, 51))  # Fundo azul
        draw = ImageDraw.Draw(background)
        
        try:
            team_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)
        except IOError:
            print("Fonte não encontrada, usando fonte padrão")
            team_font = ImageFont.load_default()

        # Adicionar título centralizado
        draw.text((largura // 2, 50), f"CLASSIFICAÇÃO - {categoria}", font=team_font, fill=(255, 255, 255), anchor="mt")

        # Determinar quantos times mostrar (máximo 20)
        num_times = len(estatisticas)
        
        # Altura inicial para começar a desenhar as estatísticas
        y_start = 120
        
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
        row_height = 50
        
        # Adicionar mais espaço antes do primeiro time
        first_team_offset = 40  # Espaço adicional antes do primeiro time
        
        # Desenhar estatísticas para cada time
        for i, (time, stats) in enumerate(estatisticas):
            # Calcular posição Y para esta linha
            y_pos = y_start + 60 + first_team_offset + i * row_height
            
            # Obter a imagem do time
            imagem_time = equipes_imagens.get(time, 'default.jpg')
            image_path = os.path.join('image', imagem_time)
            if not os.path.exists(image_path):
                print(f"Imagem não encontrada para {time}, usando default.jpg")
                image_path = os.path.join('image', 'default.jpg')
            
            try:
                # Abrir e redimensionar a imagem do time
                logo = Image.open(image_path).convert("RGBA")
                logo = logo.resize((30, 30))  # Tamanho muito reduzido
                
                # Adicionar logo do time
                background.paste(logo, (110, y_pos - 15), logo if logo.mode == 'RGBA' else None)
                
                # Abreviar nome do time se for muito longo
                nome_time = time
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
                draw.text((180, y_pos), nome_time, font=team_font, fill=(255, 255, 255))
                
                # Adicionar estatísticas
                draw.text((540, y_pos), str(stats['jogos']), font=team_font, fill=(255, 255, 255), anchor="mt")
                draw.text((600, y_pos), str(stats['vitorias']), font=team_font, fill=(0, 255, 0), anchor="mt")  # Verde para vitórias
                draw.text((660, y_pos), str(stats['derrotas']), font=team_font, fill=(255, 0, 0), anchor="mt")  # Vermelho para derrotas
                draw.text((720, y_pos), f"{stats['aproveitamento']:.1f}%", font=team_font, fill=(255, 255, 255), anchor="mt")
                
                # Saldo de pontos com cor baseada no valor
                saldo_cor = (0, 255, 0) if stats['saldo_pontos'] > 0 else (255, 0, 0) if stats['saldo_pontos'] < 0 else (255, 255, 255)
                saldo_texto = f"+{stats['saldo_pontos']}" if stats['saldo_pontos'] > 0 else str(stats['saldo_pontos'])
                draw.text((830, y_pos), saldo_texto, font=team_font, fill=saldo_cor, anchor="mt")
                
                # Desenhar linha separadora
                if i < num_times - 1:
                    draw.line([(100, y_pos + 25), (980, y_pos + 25)], fill=(100, 100, 100), width=1)
                    
            except Exception as e:
                print(f"Erro ao processar estatísticas para {time}: {e}")
        
        # Adicionar rodapé
        draw.text((540, 1020), "FPB - Federação Paulista de Basketball", font=team_font, fill=(150, 150, 150), anchor="mt")
        
        # Criar nome do arquivo
        filename = f"posts/classificacao_{categoria}.jpg"
        
        # Salvar a imagem
        background.save(filename)
        print(f"Post de classificação para a categoria {categoria} criado com sucesso!")

# Calcular as estatísticas por categoria
estatisticas_por_categoria = calcular_estatisticas_por_categoria()

# Criar os posts de classificação por categoria
criar_post_classificacao_categoria(estatisticas_por_categoria)
