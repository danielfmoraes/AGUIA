import pandas as pd
import re
import os
from difflib import get_close_matches

def normalize_upcoming_matches(input_file, output_file):
    print(f"Normalizando arquivo de próximas partidas: {input_file}")
    
    # Lista de nomes corretos de equipes
    nomes_corretos = [
        'CIRCULO MILITAR S.P.',
        'C.A. PAULISTANO',
        'C.A. MONTE LIBANO',
        'CLUBE CAMPINEIRO DE REGATAS E NATAÇÃO',
        'CLUBE ESPERIA',
        'E.C. PINHEIROS',
        'SÃO PAULO F.C.',
        'S.E. PALMEIRAS',
        'S.C. CORINTHIANS PTA.',
        'T.C. PAULISTA',
        'INTERNACIONAL DE REGATAS',
        'SÃO JOSÉ BASKETBALL / ATLETA CIDADÃO',
        'JACAREI BASKETBALL',
        'SANTO ANDRE / APABA',
        'AMAB / GIRAFINHAS / MAUA',
        'DOUBLE VOTORANTIM BASKET',
        'SÃO BERNARDO BASQUETE',
        'RM STARS BASQUETEBOL',
        'F.R. ALPHAVILLE',
        'CFE TAUBATE / IGC / LBCP',
        'A.D. CENTRO OLIMPICO',
        'CLUBE DE CAMPO DE RIO CLARO - CCRC',
        'A.A. MOGI DAS CRUZES',
        'INSTITUTO SUPERAÇÃO',
        'BAURU BASKET',
        'AABB LIMEIRA',
        'APAGEBASK / GUARULHOS',
        'CLUBE PAINEIRAS DO MORUMBY',
        'F.R. JANDIRA',
        'HIPICA CAMPINAS',
        'SESI-SP / FRANCA BASQUETE',
        'CAC / CRAVINHOS BASKETBALL',
        'F.R. MIRASSOL',
        'F.R. TUPÃ',
        'SOROCABA BASQUETE',
        'SANTANA DE PARNAÍBA/AJABASK',
        'BASQUETE SANTOS / FUPES',
        'SEMELP / PINDAMONHANGABA BASQUETE PINDA',
        'SL MANDIC BASQUETE',
        'GRUPO BT/CLUBE DE CAMPO DE TATUI',
        'ARARAQUARA – ABA / FUNDESPORT',
        'TIME JUNDIAI-JUNBASKET',
        'F.R. MARILIA',
        'MOGI BASQUETE',
                                                                                                                                                                  # Adicionado novo time encontrado
    ]
    
    # Mapeamento de variações de nomes para nomes corretos
    mapeamento_nomes = {
        'CIRCULO MILITAR': 'CIRCULO MILITAR S.P.',
        'PAULISTANO': 'C.A. PAULISTANO',
        'MONTE LIBANO': 'C.A. MONTE LIBANO',
        'CLUBE CAMPINEIRO': 'CLUBE CAMPINEIRO DE REGATAS E NATAÇÃO',
        'REGATAS E NATAÇÃO': 'CLUBE CAMPINEIRO DE REGATAS E NATAÇÃO',
        'ESPERIA': 'CLUBE ESPERIA',
        'PINHEIROS': 'E.C. PINHEIROS',
        'SÃO PAULO': 'SÃO PAULO F.C.',
        'PALMEIRAS': 'S.E. PALMEIRAS',
        'CORINTHIANS': 'S.C. CORINTHIANS PTA.',
        'TENIS CLUBE PAULISTA': 'T.C. PAULISTA',
        'INTERNACIONAL': 'INTERNACIONAL DE REGATAS',
        'SÃO JOSÉ': 'SÃO JOSÉ BASKETBALL / ATLETA CIDADÃO',
        'ATLETA CIDADÃO': 'SÃO JOSÉ BASKETBALL / ATLETA CIDADÃO',
        'JACAREI': 'JACAREI BASKETBALL',
        'SANTO ANDRE': 'SANTO ANDRE / APABA',
        'APABA': 'SANTO ANDRE / APABA',
        'AMAB': 'AMAB / GIRAFINHAS / MAUA',
        'GIRAFINHAS': 'AMAB / GIRAFINHAS / MAUA',
        'MAUA': 'AMAB / GIRAFINHAS / MAUA',
        'VOTORANTIM': 'DOUBLE VOTORANTIM BASKET',
        'SÃO BERNARDO': 'SÃO BERNARDO BASQUETE',
        'RM STARS': 'RM STARS BASQUETEBOL',
        'ALPHAVILLE': 'F.R. ALPHAVILLE',
        'CENTRO OLIMPICO': 'A.D. CENTRO OLIMPICO',
        'TAUBATE': 'CFE TAUBATE / IGC / LBCP',
        'RIO CLARO': 'CLUBE DE CAMPO DE RIO CLARO - CCRC',
        'MOGI DAS CRUZES': 'A.A. MOGI DAS CRUZES',
        'INSTITUTO SUPERAÇÃO' : 'INSTIT.SUPERAÇÃO - FORM.PELO ESPORTE',
        'BAURU BASKET' : 'ASSOCIACAO BAURU BASKETBALL TEAM',
        'AABB LIMEIRA': 'ASSOC.ATLETICA BANCO DO BRASIL',
        'APAGEBASK / GUARULHOS': 'APAGEBASK / GUARULHOS',
        'CLUBE PAINEIRAS DO MORUMBY': 'CLUBE PAINEIRAS DO MORUMBY',
        'F.R. JANDIRA': 'LIGA PAULISTA/OVERTIME',
        'HIPICA CAMPINAS': 'SOCIEDADE HIPICA DE CAMPINAS',
        'SESI-SP / FRANCA BASQUETE': 'SESI-SP/FRANCA BASQUETEBOL CLUBE',
        'CAC / CRAVINHOS BASKETBALL': 'CLUBE ATLETICO CRAVINHOS',
        'F.R. MIRASSOL':'F.R. SÃO JOSÉ DO RIO PRETO',
        'F.R. TUPÃ':'FEDERACAO REGIONAL DE BAURU',
        'SOROCABA BASQUETE' : 'ASSOCIAÇÃO CLASSIC SPORTS',
        'SANTANA DE PARNAÍBA/AJABASK' : 'ASSOC.JAGUAR BASKETBALL',
        'BASQUETE SANTOS / FUPES' : 'INSTITUTO OSVALDO DE ROSIS',
        'SEMELP / PINDAMONHANGABA BASQUETE PINDA': 'SEMELP PINDAMONHANGABA',
        'SL MANDIC BASQUETE' : 'SL MANDIC BASQUETE' ,
        'GRUPO BT/CLUBE DE CAMPO DE TATUI' : 'ASSOC.DOS AMIGOS DO BASQ.TATUI',
        'ARARAQUARA – ABA / FUNDESPORT' : 'ABA FUNDESPORT ARARAQUARA',
        'TIME JUNDIAI-JUNBASKET': 'TIME JUNDIAI',
        'F.R. MARILIA':"FEDERACAO REGIONAL DE BAURU" ,
        'MOGI BASQUETE':'ASSOC. DESPORT.MOGI DAS CRUZES' ,

    }
    
    # Função para normalizar o nome da equipe
    def normalizar_nome_equipe(nome):
        if pd.isna(nome) or nome == '':
            return nome
            
        nome = nome.strip().upper()
        
        # Verificar se o nome já está na lista de nomes corretos
        if nome in nomes_corretos:
            return nome
            
        # Verificar se o nome está no mapeamento
        for variacao, correto in mapeamento_nomes.items():
            if variacao in nome:
                return correto
                
        # Tentar encontrar o nome mais próximo usando difflib
        matches = get_close_matches(nome, nomes_corretos, n=1, cutoff=0.6)
        if matches:
            print(f"Nome ajustado: '{nome}' -> '{matches[0]}'")
            return matches[0]
            
        # Se não encontrar correspondência, perguntar ao usuário
        print(f"\nNome de equipe não reconhecido: '{nome}'")
        print("Opções disponíveis:")
        for i, nome_correto in enumerate(nomes_corretos, 1):
            print(f"{i}. {nome_correto}")
        print(f"{len(nomes_corretos) + 1}. Manter como está")
        print(f"{len(nomes_corretos) + 2}. Adicionar como novo nome correto")
        
        try:
            escolha = int(input("Escolha uma opção (número): "))
            if 1 <= escolha <= len(nomes_corretos):
                return nomes_corretos[escolha - 1]
            elif escolha == len(nomes_corretos) + 1:
                return nome
            elif escolha == len(nomes_corretos) + 2:
                nomes_corretos.append(nome)
                print(f"'{nome}' adicionado à lista de nomes corretos.")
                return nome
            else:
                print("Opção inválida. Mantendo o nome original.")
                return nome
        except ValueError:
            print("Entrada inválida. Mantendo o nome original.")
            return nome
    
    # Verificar se o arquivo existe
    if not os.path.exists(input_file):
        print(f"Erro: Arquivo {input_file} não encontrado.")
        return
    
    try:
        # Ler o CSV
        df = pd.read_csv(input_file)
        
        # Verificar e criar colunas necessárias se não existirem
        colunas_necessarias = ["Data", "Horário", "Equipe 1", "Equipe 2", "Local", "Categoria"]
        for coluna in colunas_necessarias:
            if coluna not in df.columns:
                df[coluna] = ""
                print(f"Coluna '{coluna}' não encontrada. Criada coluna vazia.")
        
        # Remover linhas com dados essenciais faltantes
        df_original_len = len(df)
        df = df.dropna(subset=["Equipe 1", "Equipe 2", "Categoria"])
        linhas_removidas = df_original_len - len(df)
        if linhas_removidas > 0:
            print(f"Removidas {linhas_removidas} linhas com dados essenciais faltantes.")
        
        # Normalizar nomes das equipes
        df["Equipe 1"] = df["Equipe 1"].apply(normalizar_nome_equipe)
        df["Equipe 2"] = df["Equipe 2"].apply(normalizar_nome_equipe)
        
        # Normalizar categorias
        def normalizar_categoria(categoria):
            if pd.isna(categoria) or categoria == '':
                return categoria
                
            categoria = str(categoria).strip().upper()
            
            # Padronizar formato "SUB XX [Masculino/Feminino]"
            if "SUB" in categoria:
                # Extrair o número da categoria
                match = re.search(r'SUB\s*(\d+)', categoria)
                if match:
                    numero = match.group(1)
                    
                    # Determinar o gênero
                    if "FEM" in categoria:
                        return f"SUB {numero} Feminino"
                    else:
                        return f"SUB {numero} Masculino"
            
            return categoria
        
        df["Categoria"] = df["Categoria"].apply(normalizar_categoria)
        
        # Normalizar datas
        def normalizar_data(data):
            if pd.isna(data) or data == '':
                return data
                
            data = str(data).strip()
            
            # Verificar se está no formato DD/MM/YYYY
            if re.match(r'^\d{2}/\d{2}/\d{4}$', data):
                return data
            
            # Tentar converter outros formatos
            try:
                data_obj = pd.to_datetime(data)
                return data_obj.strftime('%d/%m/%Y')
            except:
                return data
        
        df["Data"] = df["Data"].apply(normalizar_data)
        
        # Salvar o CSV normalizado
        df.to_csv(output_file, index=False)
        print(f"CSV de próximas partidas normalizado salvo em: {output_file}")
        print(f"Total de linhas processadas: {len(df)}")
        
    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")

# Exemplo de uso
if __name__ == "__main__":
    input_file = "data/proximas_partidas.csv"
    output_file = "data/proximas_partidas_normalizadas.csv"
    normalize_upcoming_matches(input_file, output_file)