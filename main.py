"""
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>
"""


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


# To clear terminal screen
def clrscr():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

    console.rule("[bold cyan]Welcome")
    console.print(f"[bold cyan]{logo}[/bold cyan]")
    console.rule()


# converter for mp4 -> mp3
def convert(title, output_path, rem=1, cur=1):
    clrscr()
    console.rule(f"[bold white](Converting: [bold red]{title[0:30]})")
    console.print(f"[{cur}/{rem}]", justify="right")
    video = VideoFileClip(os.path.join(output_path, "MP4", f"{title}.mp4"))
    try:
        video.audio.write_audiofile(os.path.join(output_path, "MP3", f"{title}.mp3"))
    except:
        print("This file can't be converted into mp3.")
    video.close()


def download(url, output_path, rem=1, cur=1):

    clrscr()
    wd = os.path.join(output_path, "MP4")
    try:
        yt = YouTube(f'{url}')

        title = yt.title
        title = title.replace('|', '')
        title = title.replace(',', '')
        title = title.replace('/', '')
        title = title.replace('"', '')

        new_title = title[0:30]
        style = "bold white"
        console.rule(f"[bold white](Downloading: [bold blue]{new_title})")
        console.print(f"[{cur}/{rem}]", justify="right")

        with console.status("Downloading", spinner="simpleDots"):
            # download and return title
            stream = yt.streams.get_lowest_resolution()
            stream.download(filename=(title + ".mp4"), output_path=wd)
            console.log(f"[bold green]Downloaded file {title}.")
        return title

    except Exception as e:
        return False


# To delete all trash.
def delete_files(output_path):
    clrscr()
    console.rule("[bold cyan]Finishing UP")
    with console.status("[bold cyan] Deleting Trash...", spinner="simpleDots"):
        time.sleep(3)
        shutil.rmtree(os.path.join(output_path, "MP4"))


# List mechanism to present files in a nice manner.
def list_files(output_path):
    num = 0
    clrscr()
    console.rule("[bold white] Result")
    files = os.listdir(os.path.join(output_path, "MP3"))
    console.print("[bold blue]These are the downloaded MP3 files.[/bold blue]")
    for file in files:
        num += 1
        console.print(
            f"[bold white]{num} [/bold white] [bold red]- [/bold red] [bold green]{file}[/bold green]")


def main():
    i = 1
    clrscr()

    video_url = prompt.ask("[bold green]Enter The URL Of PlayList: ")
    for t in range(3):
        clrscr()
        output_path = prompt.ask("[bold green]Output Path? (Default=", default=os.getcwd())
        try:
            os.mkdir(os.path.join(output_path, 'MP3'))
            os.mkdir(os.path.join(output_path, 'MP4'))
            break
        except FileExistsError:
            pass
        except FileNotFoundError:
            console.print("[bold red]Folder not found... Retry")
            time.sleep(2)
            if t == 2:
                clrscr()
                console.print("[bold white] Multiple failed attempts using current folder as the target.", justify="center")
                output_path = os.getcwd()
                time.sleep(2)
            

    if "playlist" in video_url:
        play_list = Playlist(video_url)
        for url in play_list.video_urls:
            file_name = download(url, output_path, len(play_list), i)
            if file_name:
                convert(file_name, output_path, len(play_list), i)
            i += 1
    else:
        file_name = download(video_url, output_path)
        if file_name:
            convert(file_name, output_path)
        else:
            console.log("[bold red]Download failed, please try again.", justify="center")
            return 0

    delete_files(output_path)
    list_files(output_path)


if __name__ == '__main__':
    main()
