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
| |  | | | |/ _` | '_ \| || | | | '_ \ / _ \\
| |__| |_| | (_| | | | | || |_| | |_) |  __/
 \____\__, |\__,_|_| |_|_| \__,_|_.__/ \___|
      |___/

Absolutely Proprietary
 """
console = Console()

prompt = Prompt()

try:
    os.mkdir('mp3')
    os.mkdir('mp4')
except FileExistsError:
    pass


# To clear terminal screen
def clrscr():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


# converter for mp4 -> mp3
def convert(title, rem=1, cur=1):
    clrscr()
    console.rule(f"[bold white]Converting: [bold red]{title[0:30]}")
    console.print(f"[{cur}/{rem}]", justify="right")
    wd = os.getcwd()
    video = VideoFileClip(os.path.join(wd, "mp4", f"{title}.mp4"))
    try:
        video.audio.write_audiofile(os.path.join(wd, "mp3", f"{title}.mp3"))
    except :
        print("This file can't be converted into mp3.")
    video.close()


def download(url, rem=1, cur=1):

    # working directory
    clrscr()
    wd = os.getcwd()
    folder = "mp4"
    wd = os.path.join(wd, folder)
    yt = YouTube(f'{url}')
    
    # setting up title
    title = yt.title
    title = title.replace('|', '')
    title = title.replace(',', '')
    title = title.replace('/', '')
    title = title.replace('"', '')

    new_title = title[0:30]
    style = "bold white"
    console.rule(f"[bold white]Downloading: [bold blue]{new_title}")
    console.print(f"[{cur}/{rem}]", justify="right")
    with console.status("Downloading", spinner="simpleDots"):
        # download and return title
        stream = yt.streams.get_lowest_resolution()
        stream.download(filename=(title + ".mp4"), output_path=wd)
    console.log(f"[bold green]Downloaded file {title}.")
    return title


# To delete all trash.
def delete_files():
    clrscr()
    console.rule("[bold cyan]Finishing UP")
    with console.status("[bold cyan] Deleting Trash...", spinner="simpleDots"):
        time.sleep(3)
        shutil.rmtree(os.path.join(os.getcwd(), "mp4"))


# List mechanism to present files in a nice manner.
def list_files():
    num = 0
    clrscr()
    console.rule("[bold white] Result")
    files = os.listdir(os.path.join(os.getcwd(), "mp3"))
    console.print("[bold blue]These are the downloaded Mp3 files.[/bold blue]")
    for file in files:
        num += 1
        console.print(f"[bold white]{num} [/bold white] [bold red]- [/bold red] [bold green]{file}[/bold green]")



def main():

    i = 1
    clrscr()
    # console log logo
    print(f"[bold cyan]{logo}[/bold cyan]")
    
    video_url = prompt.ask("[bold green]Enter The URL Of PlayList")
    new_url = video_url.split('?')
    if new_url[0] == "https://www.youtube.com/playlist":
        play_list = Playlist(video_url)
        for url in play_list.video_urls:
            title = download(url, len(play_list), i)
            convert(title, len(play_list), i)
            i += 1
    else:
        title = download(video_url)
        convert(title)
    
    delete_files()
    list_files()



if __name__ == '__main__':
    main()
    



