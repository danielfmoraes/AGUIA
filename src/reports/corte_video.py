import os

# Verificar se o arquivo de vídeo existe
if not os.path.exists("data/video.mp4"):
    print("❌ Erro: O arquivo de vídeo não foi encontrado após o download.")
    exit()

# Criar pasta 'cuts/' se não existir
os.makedirs("cuts", exist_ok=True)

# Função para converter tempo string "MM:SS" para segundos
def tempo_str_para_segundos(tempo_str):
    try:
        minutos, segundos = map(int, tempo_str.strip().split(":"))
        return minutos * 60 + segundos
    except:
        print(f"⚠️ Formato inválido: {tempo_str}. Use o formato MM:SS.")
        return None

# Solicitar ao usuário quantos cortes deseja fazer
try:
    num_cortes = int(input("Quantos cortes deseja fazer? "))
except ValueError:
    print("❌ Entrada inválida. Digite um número.")
    exit()

# Lista para armazenar os cortes
cortes = []

for i in range(1, num_cortes + 1):
    print(f"\n⏱️ Corte {i}:")
    inicio_str = input("  Início (MM:SS): ")
    fim_str = input("  Fim    (MM:SS): ")
    
    inicio = tempo_str_para_segundos(inicio_str)
    fim = tempo_str_para_segundos(fim_str)
    
    if inicio is None or fim is None:
        print("❌ Corte ignorado por erro de formato.")
        continue

    if fim <= inicio:
        print("⚠️ Tempo final deve ser maior que o inicial. Corte ignorado.")
        continue

    cortes.append((inicio, fim))

# Criar e salvar os cortes com ffmpeg
for i, (inicio_segundos, fim_segundos) in enumerate(cortes, start=1):
    output_file = f"cuts/video_corte2_{i}.mp4"
    comando = f'ffmpeg -i reports/sjcxpinheiros.mp4 -ss {inicio_segundos} -to {fim_segundos} -c:v copy -c:a copy "{output_file}"'
    
    print(f"🎬 Criando vídeo corte2_{i}: {inicio_segundos}s → {fim_segundos}s")
    os.system(comando)

print("\n✅ Cortes concluídos com sucesso! Arquivos salvos na pasta 'cuts/'")
