import os
import shutil
import time
from pytube import YouTube, Playlist
from moviepy.editor import *
from rich import print
from rich.console import Console
from rich.prompt import Prompt

logo = """ 
  ___  _  _   __    _  _   ____  __  __  ____  ____ 
 / __)( \/ ) /__\  ( \( ) (_  _)(  )(  )(  _ \( ___)
( (__  \  / /(__)\  )  (    )(   )(__)(  ) _ < )__) 
 \___) (__)(__)(__)(_)\_)  (__) (______)(____/(____)
 
 """
console = Console()

prompt = Prompt()

os.mkdir('mp3')
os.mkdir('mp4')


def convertor(title):
    wd = os.getcwd()
    video = VideoFileClip(os.path.join(f"{wd}\mp4\{title}.mp4"))
    try:
        video.audio.write_audiofile(os.path.join(f"{wd}\mp3\{title}.mp3"))
    except :
        print("This file can't be converted into mp3.")
    video.close()


def download(url):
    wd = os.getcwd()
    folder = "\mp4"
    wd = wd + folder
    yt = YouTube(f'{url}')
    title = yt.title
    title = title.replace('|', '')
    title = title.replace(',', '')
    title = title.replace('/', '')
    title = title.replace('"', '')
    stream = yt.streams.get_lowest_resolution()
    stream.download(filename=(title + ".mp4"), output_path=wd)
    console.log(f"[bold green]Downloaded file {title}.")
    return title

def main():
    print(f"[bold cyan]{logo}[/bold cyan]")
    
    video_url = prompt.ask("[bold green]Enter The URL Of PlayList")
    new_url = video_url.split('?')
    if new_url[0] == "https://www.youtube.com/playlist":
        play_list = Playlist(video_url)
        for url in play_list.video_urls:
            title = download(url)
            convertor(title)
            time.sleep(10)
    else:
        title = download(video_url)
        convertor(title)
        time.sleep(10)
    
    console.status("[bold cyan] Deleting Trash...")
    pwd = os.getcwd()
    target = pwd + "\mp4"
    shutil.rmtree(target)


if __name__ == '__main__':
    main()
    



