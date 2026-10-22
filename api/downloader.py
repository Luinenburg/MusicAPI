#!/usr/bin/env python3
import os
from textwrap import fill
from time import sleep
import yt_dlp
from tinytag import TinyTag
from dotenv import load_dotenv
load_dotenv()

BASE_DIRECTORY = os.getenv("DOWNLOAD_DIRECTORY")


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
    data = file.readlines()
    file.close()
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
def collect_files(youtube_url: str):
    goto_temp()
    for file in os.listdir():
        os.remove(file)
    
    ydl_opts = {
        'writethumbnail': True,
        'format': 'm4a/bestaudio/best',
        'cookiesfrombrowser': ('firefox', None, None, None),
        'forcethumbnail': True,
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            },
            {
                'key': 'FFmpegMetadata'
            },
            {
                'key': 'EmbedThumbnail'
            },
        ],
        'forcetitle': True,
        'embedmetadata': True,
        'embedthumbnail': True,
        'outtmpl': '%(title)s.%(ext)s',
        'extractor-args': {
            'youtube': {
                'player_client': 'default',
                'android_sdkless': True
            }
        }
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

def get_album_directory():
    for file in os.listdir():
        print(file)
        if file.find(".mp3") == -1: continue
        metadata = TinyTag.get(file)
        return [metadata.artist, metadata.album]
    print("no .mp3 found")
    quit()


# Remove original m4a files
def clean_folder():
    for filename in os.listdir():
        if filename.find(".mp3") or filename.find(".jpg") or filename.find(".png") == 1:
            continue
        print(filename)
        os.remove(filename)


def download(youtube_url: str):
    failure = 1
    enter_absolute_directory(BASE_DIRECTORY)
    while collect_files(youtube_url) == 1:
        if failure == 1:
            input("Press enter to try again...")
            for file in os.listdir():
                os.remove(file)
        continue
    album_dir = get_album_directory()
    clean_folder()
    enter_album_directory(album_dir)