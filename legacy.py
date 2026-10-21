#!/usr/bin/env python3
import os
from textwrap import fill
from time import sleep
import yt_dlp

BASE_DIRECTORY = os.getcwd()


# Attempts to access specific directory, with catches for failure
def enter_absolute_directory(directory: str):
    try:
        os.chdir(directory)
    except:
        print("Failure changing directory. Quitting.")
        print("Current directory: " + os.getcwd())
        print("Attempted directory change: " + directory)
        quit()


# Enters given file and extracts song information from that file
def grab_from_file(filename: str):
    file = open(filename)
    data_str = file.readlines()
    file.close()
    data = [line.split(' ') for line in data_str]
    return data


# Get to the directory ./[artist]/[album], making the directories if they don't exist yet
def enter_album_directory(directories):
    enter_absolute_directory(BASE_DIRECTORY)
    old_directory = BASE_DIRECTORY

    for directory in directories:
        for filename in os.listdir():
            if filename == directory:
                print(f"Entering existing directory for ({filename})")
                enter_absolute_directory(os.getcwd() + "/" + filename)
                break
        if old_directory == os.getcwd():
            print(f"Making new ({directory}) directory inside of ({old_directory})")
            os.mkdir(directory)
            old_directory = os.getcwd() + "/" + directory
            enter_absolute_directory(old_directory)
        old_directory = os.getcwd()
    print(f"Current Directory: {os.getcwd()}\n")
    move_out_of_temp(old_directory)


def move_out_of_temp(new_directory: str):
    for file in os.listdir(BASE_DIRECTORY+"/temp"):
        print(f"Moving {BASE_DIRECTORY+"/temp/"+file}")
        os.replace(BASE_DIRECTORY+"/temp/"+file, new_directory+"/"+file)
        print(f"Now in {new_directory}")


def goto_temp():
    print("Entering temp directory...")
    try:
        os.chdir("temp")
    except:
        print("Could not find temp. Making.")
        os.mkdir("temp")
        os.chdir("temp")


# Gets image jpg and downloads songs from youtube
def collect_files(image_url: str, youtube_url: str):
    goto_temp()
    for file in os.listdir():
        os.remove(file)

    os.system("wget -O image {}".format(image_url))
    sleep(1)
    cover_image_old = os.listdir()[0]
    if cover_image_old.find(".") == -1:
        cover_image_old += ".jpg"
    extension = cover_image_old[cover_image_old.find("."):]
    os.rename(os.listdir()[0], "cover" + extension)
    
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'cookiesfrombrowser': ('firefox', None, None, None),
        'forcethumbnail': True,
        'forcetitle': True,
        'outtmpl': '%(playlist_index)d---%(title)s---%(album)s---%(artist,creator)s---%(genre)s---%(release_year)s.%(ext)s'
        ,
        'extractor-args': {'youtube': {'player_client': 'default', 'android_sdkless': True}}
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            error_code = ydl.download(youtube_url)
        except PermissionError:
            print("Permission error encountered")
            return 1
        if (error_code):
            print(f"fat ass {error_code}")
            return 1
    return 0


def get_metadata_from_filename(file: str):
    sections = file.split('---')
    metadata = {"index": sections[0], "title": sections[1], "album": sections[2], "artists": sections[3], "genre": sections[4], "year": sections[5]}
    if (metadata["index"] == "NA"):
        metadata["index"] = "0"
    if (metadata["artists"] == "NA"):
        metadata["artists"] = input("Enter artist(s) for {}: ".format(metadata["title"]))
    if (metadata["album"] == "NA"):
        metadata["album"] = metadata["title"]
    if (metadata["title"] == "NA"):
        metadata["title"] = "Unknown"
    if (metadata["genre"] == "NA"):
        metadata["genre"] = "Unknown"
    if (metadata["year"] == "NA"):
        metadata["year"] = "6769"
    return metadata

def get_album_directory():
    for file in os.listdir():
        print(file)
        if file.find(".m4a") == -1 and file.find(".mp4") == -1: continue
        metadata = get_metadata_from_filename(file)
        artist = metadata["artists"].split(",")[0]
        return [artist, metadata["album"]]
    print("no .m4a or mp4 found")
    quit()

# Convert the m4a files downloaded from youtube to mp3 and add in metadata
def convert_m4a_to_mp3():
    for file in os.listdir():
        if (file.find(".m4a") == -1 and file.find(".mp4") == -1): continue
        metadata = get_metadata_from_filename(file)
        filename = metadata["index"] + " " + metadata["title"]
        """query = f"ffmpeg -i \"{file}\" -i cover.jpg -map 0:0 -map 1:0 -id3v2_version 3 \
            -metadata artist=\"{metadata["artists"]}\" -metadata album=\"{metadata["album"]}\" -metadata year=\"{metadata["year"]}\" -metadata genre=\"{metadata["genre"]}\" \
            -metadata track=\"{metadata["index"]}\" -metadata title=\"{metadata["title"]}\" \
            \"{filename}.mp3\""
        """
        query = f"ffmpeg -i \"{file}\" \
            -metadata artist=\"{metadata["artists"]}\" -metadata album=\"{metadata["album"]}\" -metadata year=\"{metadata["year"]}\" -metadata genre=\"{metadata["genre"]}\" \
            -metadata track=\"{metadata["index"]}\" -metadata title=\"{metadata["title"]}\" \
            \"{filename}.mp3\""
        print(query)
        os.system(query)


# Remove original m4a files
def clean_folder():
    for filename in os.listdir():
        if filename.find(".m4a") == -1 and filename.find(".mp4") == -1:
            continue
        print(filename)
        os.remove(filename)


# Query user directly for album info
def fill_from_user_input():
    failure = 1
    url = input("Youtube URL to album: ").strip()
    image = input("URL to coverart: ").strip()
    enter_absolute_directory(BASE_DIRECTORY)
    while collect_files(image, url) == 1:
        if failure == 1:
            input("Press enter to try again...")
            for file in os.listdir():
                os.remove(file)
        continue
    album_dir = get_album_directory()
    convert_m4a_to_mp3()
    clean_folder()
    enter_album_directory(album_dir)


# Pull album data from files
def fill_from_file():
    albums = grab_from_file("songs.txt")
    for album_data in albums:
        failure = 1
        print(f"\n\nGoing to {BASE_DIRECTORY}...")
        enter_absolute_directory(BASE_DIRECTORY)
        url = album_data[0].strip()
        image = album_data[1].strip()
        while failure == 1:
            print("\n\nCollecting necessary files...")
            failure = collect_files(image, url)
            if failure == 1:
                input("Press enter to try again...")
                for file in os.listdir():
                    os.remove(file)
            continue
        album_dir = get_album_directory()
        print("\n\nConverting files to mp3")
        convert_m4a_to_mp3()
        print("\n\nCleaning temp")
        clean_folder()
        print(f"\n\nMoving files to {album_dir}")
        enter_album_directory(album_dir)


def main():
    enter_absolute_directory(BASE_DIRECTORY)
    fill_from_file()


if __name__ == "__main__":
    main()
