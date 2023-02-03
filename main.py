import os
import shutil
import time
from pytube import YouTube, Playlist
from moviepy.editor import *
from rich import print
from rich.console import Console
from rich.prompt import Prompt

logo = """ 
  ____                _____      _
 / ___|   _  __ _ _ _|_   _|   _| |__   ___
| |  | | | |/ _` | '_ \| || | | | '_ \ / _ \
| |__| |_| | (_| | | | | || |_| | |_) |  __/
 \____\__, |\__,_|_| |_|_| \__,_|_.__/ \___|
      |___/

Absolutely Proprietary
 """
console = Console()

prompt = Prompt()

os.mkdir('mp3')
os.mkdir('mp4')

# converter for mp4 -> mp3
def convertor(title):
    wd = os.getcwd()
    video = VideoFileClip(os.path.join(f"{wd}\mp4\{title}.mp4"))
    try:
        video.audio.write_audiofile(os.path.join(f"{wd}\mp3\{title}.mp3"))
    except :
        print("This file can't be converted into mp3.")
    video.close()


def download(url):

    # working directory
    wd = os.getcwd()
    folder = "\mp4"
    wd = wd + folder
    yt = YouTube(f'{url}')
    
    # setting up title
    title = yt.title
    title = title.replace('|', '')
    title = title.replace(',', '')
    title = title.replace('/', '')
    title = title.replace('"', '')

    # download and return title
    stream = yt.streams.get_lowest_resolution()
    stream.download(filename=(title + ".mp4"), output_path=wd)
    console.log(f"[bold green]Downloaded file {title}.")
    return title

def main():

    # console log logo
    print(f"[bold magenta]{logo}[/bold magenta]")
    
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
    



