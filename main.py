# Written by BRUHItsABunny on github.com/BRUHItsABunny
# File is part of https://github.com/BRUHItsABunny/cli_resizer_python
import argparse
import json
import logging
import os
import subprocess


def get_current_resolution(path: str):
    # ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of json input.mp4
    result = subprocess.run(
        ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'json',
         path], stdout=subprocess.PIPE)
    return json.loads(result.stdout.decode())["streams"]


def resize_video(path_new: str, path_old: str, width: int, height: int):
    # ffmpeg -i in -s 720x480 -c:a copy out
    result = subprocess.run(['ffmpeg', '-i', path_old, '-s', '%dx%d' % (width, height), '-c:a', 'copy', path_new],
                            stdout=subprocess.PIPE)
    logging.debug(result.stdout.decode())


def resize_photo(path_new: str, path_old: str, width: int, height: int):
    # ffmpeg -i in.jpg -vf scale=250x150 out.jpg
    result = subprocess.run(['ffmpeg', '-i', path_old, '-vf', 'scale=%dx%d' % (width, height), path_new],
                            stdout=subprocess.PIPE)
    logging.debug(result.stdout.decode())


def replace_file(path_new: str, path_old: str):
    os.remove(path_old)
    os.rename(path_new, path_old)
    pass


def calculate_new_resolution(old_width: int, old_height: int):
    old_ratio = float(old_width) / float(old_height)
    new_width = float(args.height) * old_ratio
    new_height = float(args.width) / old_ratio
    if new_height <= args.height:
        # found something
        logging.info("New resolution will be %fx%f" % (args.width, new_height))
        logging.debug("Old ratio = %f\nNew ratio = %f" % (old_ratio, float(args.width) / new_height))
        return args.width, int(round(new_height))
    elif new_width <= args.width:
        # found something
        logging.info("New resolution will be %fx%f" % (new_width, args.height))
        logging.debug("Old ratio = %f\nNew ratio = %f" % (old_ratio, new_width / float(args.height)))
        return int(round(new_width)), args.height


def main():
    for subdir, dirs, files in os.walk(args.dir):
        for file in files:
            if file.split(".")[-1].lower() in video_extensions and do_videos:
                # It's a video, we can check this
                resolution = get_current_resolution(os.path.join(subdir, file))[0]
                if resolution["width"] <= args.width and resolution["height"] <= args.height:
                    # ignore, it was already resized
                    pass
                else:
                    # Needs to be processed
                    logging.info("Processing video %s (%dx%d)" % (
                    os.path.join(subdir, file), resolution["width"], resolution["height"]))
                    old_file = os.path.join(subdir, file)
                    new_file = os.path.join(subdir, "resized_" + file)
                    new_width, new_height = calculate_new_resolution(resolution["width"], resolution["height"])
                    resize_video(new_file, old_file, new_width, new_height)
                    if args.replace:
                        replace_file(new_file, old_file)
            elif file.split(".")[-1].lower() in photo_extensions and do_photos:
                # It's an image, we can check this
                resolution = get_current_resolution(os.path.join(subdir, file))[0]
                if resolution["width"] <= args.width and resolution["height"] <= args.height:
                    # ignore, it was already resized
                    pass
                else:
                    # Needs to be processed
                    logging.info("Processing photo %s (%dx%d)" % (
                        os.path.join(subdir, file), resolution["width"], resolution["height"]))
                    old_file = os.path.join(subdir, file)
                    new_file = os.path.join(subdir, "resized_" + file)
                    new_width, new_height = calculate_new_resolution(resolution["width"], resolution["height"])
                    resize_photo(new_file, old_file, new_width, new_height)
                    if args.replace:
                        replace_file(new_file, old_file)


if __name__ == '__main__':
    # CONSTANTS
    video_extensions = ['mp4', 'm4a', 'm4v', 'f4v', 'f4a', 'm4b', 'm4r', 'f4b', 'mov', '3gp', '3gp2', '3g2', '3gpp',
                        '3gpp2', ' ogg', 'oga', 'ogv', 'ogx', 'wmv', 'webm', 'flv', 'avi']
    photo_extensions = ['bmp', 'gif', 'jpg', 'jpeg', 'jfif', 'pjpeg', 'png', 'webp']
    # BOOTSTRAPPING arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', dest='debug',
                        help="[OPTIONAL] This enables logging for debugging")
    parser.add_argument('--dir', default=".", required=False, dest='dir',
                        help="[OPTIONAL] This specifies which directory to crawl, default is the working directory of the process")
    parser.add_argument('--mode', required=True, dest='mode', type=int,
                        help="[REQUIRED] This specifies what files to resize, 1 = videos, 2 = photos and 0 = videos and photos")
    parser.add_argument('-r', '--replace', action='store_true', dest='replace',
                        help="[OPTIONAL] Adding this flag will make the program REPLACE the ORIGINAL")
    parser.add_argument('--width', required=True, type=int, dest='width',
                        help="[REQUIRED] This defines the target width")
    parser.add_argument('--height', required=True, type=int, dest='height',
                        help="[REQUIRED] This defines the target height")
    args = parser.parse_args()
    do_photos = False
    do_videos = False
    if args.mode == 1:
        do_videos = True
    elif args.mode == 2:
        do_photos = True
    elif args.mode == 0:
        do_photos = True
        do_videos = True
    else:
        print("Provide valid mode, 1 for videos, 2 for photos and 0 for both")
        exit()
    if args.debug:
        logging.basicConfig(filename='resizer.log', level=logging.DEBUG)
    else:
        logging.basicConfig(filename='resizer.log', level=logging.NOTSET)
    """
    Strategy:
    1. iterate through all subdirs (but not symlinks) to collect files, names and their location
    2. per file get the resolution
    3. calculate the new resolution that conforms to the constraints set in the constants (might be arguments later)
    4. resize video, delete original and then rename the new one to the original name
    """
    main()
