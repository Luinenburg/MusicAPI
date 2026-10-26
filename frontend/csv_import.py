import csv
import queries
import requests
from pathlib import Path

api_url = input("API URL: ").rstrip("/")

with Path(__file__).with_name("list.csv").open(mode="r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)
    filtered_list = []
    for row in reader:
        results = queries.search_artist_album(row['Artist Name(s)'].split(';')[0], row['Album Name'])
        print(f"\n\n{row['Artist Name(s)'].split(';')[0]} - {row['Album Name']}")
        if len(results) > 0:
            print(f"Adding {results[0]['artist']} - {results[0]['title']}")
            filtered_list.append(results[0]['playlistId'])
        else:
            print("No results.")
    songs = open("yt_export", "w")
    songs.write(str(filtered_list))
    songs.close()
    for song in filtered_list:
        try:
            response = requests.post(f"{api_url}/add_music/song/{song}")
            print(response.json())
        except requests.exceptions.InvalidSchema:
            api_url = input("Type in the URL again: ")