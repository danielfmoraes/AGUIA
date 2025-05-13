import pandas as pd
import re
import os
from difflib import get_close_matches

def corrigir_placar(placar):
    placar = str(placar).strip()
    if re.match(r"^\d{1,3}x\d{1,3}$", placar):
        return placar
    numeros = re.findall(r'\d+', placar)
    if len(numeros) == 2:
        return f"{numeros[0]}x{numeros[1]}"
    return placar

def normalizar_nome_equipe(nome, nomes_corretos, mapeamento_nomes):
    if pd.isna(nome) or nome == '':
        return nome
    nome = nome.strip().upper()
    if nome in nomes_corretos:
        return nome
    for variacao, correto in mapeamento_nomes.items():
        if variacao in nome:
            return correto
    matches = get_close_matches(nome, nomes_corretos, n=1, cutoff=0.6)
    if matches:
        print(f"Nome ajustado: '{nome}' -> '{matches[0]}'")
        return matches[0]
    return nome

def normalize_csv(input_file, output_file):
    print(f"Normalizando arquivo CSV: {input_file}")
    
    if not os.path.exists(input_file):
        print(f"Erro: Arquivo {input_file} não encontrado.")
        return

    try:
        df = pd.read_csv(input_file)

        # Remover linhas vazias e com "Local não informado"
        df = df.dropna(subset=["Data", "Horário", "Equipe 1", "Equipe 2"], how="all")
        df = df[df["Local"].str.strip().str.upper() != "LOCAL NÃO INFORMADO"]

        # Lista de nomes corretos de equipes
        nomes_corretos = [
            'CIRCULO MILITAR S.P.', 'C.A. PAULISTANO', 'C.A. MONTE LIBANO',
            'CLUBE CAMPINEIRO DE REGATAS E NATAÇÃO', 'CLUBE ESPERIA', 'E.C. PINHEIROS',
            'SÃO PAULO F.C.', 'S.E. PALMEIRAS', 'S.C. CORINTHIANS PTA.', 'T.C. PAULISTA',
            'INTERNACIONAL DE REGATAS', 'SÃO JOSÉ BASKETBALL / ATLETA CIDADÃO',
            'JACAREI BASKETBALL', 'SANTO ANDRE / APABA', 'AMAB / GIRAFINHAS / MAUA',
            'DOUBLE VOTORANTIM BASKET', 'SÃO BERNARDO BASQUETE', 'RM STARS BASQUETEBOL',
            'F.R. ALPHAVILLE', 'CFE TAUBATE / IGC / LBCP', 'A.D. CENTRO OLIMPICO',
            'CLUBE DE CAMPO DE RIO CLARO - CCRC', 'A.A. MOGI DAS CRUZES', 'INSTITUTO SUPERAÇÃO',
            'BAURU BASKET', 'AABB LIMEIRA', 'APAGEBASK / GUARULHOS', 'CLUBE PAINEIRAS DO MORUMBY',
            'F.R. JANDIRA', 'HIPICA CAMPINAS', 'SESI-SP / FRANCA BASQUETE',
            'CAC / CRAVINHOS BASKETBALL', 'F.R. MIRASSOL', 'F.R. TUPÃ',
            'SOROCABA BASQUETE', 'SANTANA DE PARNAÍBA/AJABASK', 'BASQUETE SANTOS / FUPES',
            'SEMELP / PINDAMONHANGABA BASQUETE PINDA', 'SL MANDIC BASQUETE',
            'GRUPO BT/CLUBE DE CAMPO DE TATUI', 'ARARAQUARA – ABA / FUNDESPORT',
            'TIME JUNDIAI-JUNBASKET', 'F.R. MARILIA', 'MOGI BASQUETE'
        ]

        # Mapeamento de variações de nomes
        mapeamento_nomes = {
            'CIRCULO MILITAR': 'CIRCULO MILITAR S.P.', 'PAULISTANO': 'C.A. PAULISTANO',
            'MONTE LIBANO': 'C.A. MONTE LIBANO', 'CLUBE CAMPINEIRO': 'CLUBE CAMPINEIRO DE REGATAS E NATAÇÃO',
            'REGATAS E NATAÇÃO': 'CLUBE CAMPINEIRO DE REGATAS E NATAÇÃO', 'ESPERIA': 'CLUBE ESPERIA',
            'PINHEIROS': 'E.C. PINHEIROS', 'SÃO PAULO': 'SÃO PAULO F.C.',
            'PALMEIRAS': 'S.E. PALMEIRAS', 'CORINTHIANS': 'S.C. CORINTHIANS PTA.',
            'TENIS CLUBE PAULISTA': 'T.C. PAULISTA', 'INTERNACIONAL': 'INTERNACIONAL DE REGATAS'
        }

        # Normalizar nomes das equipes
        df["Equipe 1"] = df["Equipe 1"].apply(lambda nome: normalizar_nome_equipe(nome, nomes_corretos, mapeamento_nomes))
        df["Equipe 2"] = df["Equipe 2"].apply(lambda nome: normalizar_nome_equipe(nome, nomes_corretos, mapeamento_nomes))

        # Se houver coluna de placar, normalizar
        if "Placar" in df.columns:
            df["Placar"] = df["Placar"].apply(corrigir_placar)

        # Normalizar categorias
        df["Categoria"] = df["Categoria"].str.replace(r"Masculino", "", regex=True).str.strip().str.upper()

        # Remover partidas duplicadas
        colunas_para_comparar = [col for col in ["Equipe 1", "Equipe 2", "Placar", "Categoria"] if col in df.columns]
        df = df.drop_duplicates(subset=colunas_para_comparar, keep="first")

        # Salvar CSV normalizado
        df.to_csv(output_file, index=False)
        print(f"CSV normalizado salvo em: {output_file}")
        print(f"Total de linhas processadas: {len(df)}")

    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")

# Exemplo de uso
input_file = 'data/proximas_partidas.csv'
output_file = 'data/proxima_partidas_normalizadas.csv'
normalize_csv(input_file, output_file)
