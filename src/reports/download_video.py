import yt_dlp

video_url = "https://www.youtube.com/watch?v=NU4s2r84K5A"

ydl_opts = {
    'format': 'best',
    'outtmpl': 'data/video.mp4',
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([video_url])

print("Download concluído!")
