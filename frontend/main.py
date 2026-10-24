import requests
from queries import search_artist_album

def main():
    api_url = input("API URL: ")
    while True:
        artist = input("Artist name: ")
        album = input("Album name: ")
        results = search_artist_album(artist, album)
        for index, result in enumerate(results):
            print(f"{index}: {result["artist"]} - {result["title"]} ({result["year"]}) ({result["playlistId"]})")
        song = int(input("Which one: "))
        try:
            response = requests.post(f"{api_url}/add_music/song/{results[song]["playlistId"]}")
            print(response.json)
        except requests.exceptions.InvalidSchema:
            api_url = input("Type in the URL again: ")

if __name__ == "__main__":
    main()