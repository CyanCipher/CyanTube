# CyanTube
A youtube video downloader built on python.


# Dependencies
```
    pytube == 12.1.2
    moviepy == 1.0.3
    rich == 13.3.1
```
## Usage
Just enter the URL of the video or the playlist when asked and relax for a while, the script will download videos convert them into MP3s and then it will delete any trash remaining.

## Important
If providing a playlist, gives some regex error, then goto your {python/env}/bin/pytube/cipher.py on line 30 change:

```{python}
    var_regex = re.compile(r"^\w+\W")
```

To - 

```{python}
    var_regex = re.compile(r"^\$*\w+\W")
```

Save it and it should work fine.
