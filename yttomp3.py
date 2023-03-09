import pytube
import os
link = input('Enter the link:')
yt = pytube.YouTube(link)
yt.streams.get_highest_resolution()
yt.streams.get_audio_only().download()
print('Downloaded', link)
os.rename(f"C:/Users/ASUS/Desktop/Coding/Projects/{yt.title}.mp4", f"C:/Users/ASUS/Music/{yt.title}.mp3")