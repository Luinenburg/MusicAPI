import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from yt_search.queries import search_artist_album

def main():
    api_url = input("API URL")
    while True:
        artist = input("Artist name: ")
        album = input("Album name: ")
        results = search_artist_album(artist, album)
        for result in results:
            print(f"{result["artist"]} - {result["title"]} ({result["year"]}) ({result["playlistId"]})")


if __name__ == "__main__":
    main()