# Python 3 CLI media resizer
"Quickly"* batch resize recursively video's and or images from command line interfaces with Python 3 and FFmpeg.

## Requirements
* Python 3
* FFmpeg

## Usage
```
$ python main.py --help

usage: main.py [-h] [-d] [--dir DIR] --mode MODE [-r] --width WIDTH --height HEIGHT

optional arguments:
  -h, --help       show this help message and exit
  -d, --debug      [OPTIONAL] This enables logging for debugging
  --dir DIR        [OPTIONAL] This specifies which directory to crawl, default is the working directory of the process
  --mode MODE      [REQUIRED] This specifies what files to resize, 1 = videos, 2 = photos and 0 = videos and photos
  -r, --replace    [OPTIONAL] Adding this flag will make the program REPLACE the ORIGINAL
  --width WIDTH    [REQUIRED] This defines the target width
  --height HEIGHT  [REQUIRED] This defines the target height
```

### Eamples
* For video resizing only, resizes to fit 100x100 while keeping aspect ratio and replaces original file:
* ````python main.py --replace --width 100 --height 100 --mode 1```
* For image resizing only, resizes to fit 100x100 while keeping aspect ratio and replaces original file:
* ````python main.py --replace --width 100 --height 100 --mode 2```
* For video AND image resizing, resizes to fit 100x100 while keeping aspect ratio and WITHOUT replacing original file:
* ````python main.py --width 100 --height 100 --mode 0```

You can also add the --dir flag to specify which folder the program has to start iteration in. (--dir "path\to\folder")

## Limitations
* Does not support custom FFmpeg locations (to be added)
* Does not support parallel resizing to speed things up significantly (to be added in a better project)
* Requires Python to be installed (to be addressed in a better project)
* No UI/little UI feedback (to be added in better project)
These limitations will probably be tackled in a Golang project of the same or similar purpose.
Mostly because then it won't require an interpreter to be installed anymore and will just work with a single file you can execute.
