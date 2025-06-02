import yt_dlp

# Solicita ao usuário o link do vídeo
video_url = input("Digite o link do vídeo do YouTube: ")

# Opções de download
ydl_opts = {
    'format': 'best',
    'outtmpl': 'data/video.mp4',
}

# Realiza o download
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([video_url])

print("Download concluído!")
