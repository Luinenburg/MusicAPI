import requests
from pathlib import Path

api_url = input("API URL: ").rstrip("/")

filtered_list = []
for song in filtered_list:
    try:
        response = requests.post(f"{api_url}/add_music/song/{song}")
        print(response.json())
    except requests.exceptions.InvalidSchema:
        api_url = input("Type in the URL again: ")