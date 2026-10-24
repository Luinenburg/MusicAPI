from ytmusicapi import YTMusic, OAuthCredentials
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

CLIENT_ID = os.getenv("YT_TV_OAUTH_CLID")
CLIENT_SECRET = os.getenv("YT_TV_OAUTH_CLSECRET")

yt = YTMusic(str(Path(__file__).with_name("browser.json")))

def search_artist_album(artist, album):
    results = []
    search_results = yt.search(f"{artist} - {album}")
    for search_result in search_results:
        result = {}
        if search_result['resultType'] != 'album':
            continue
        result['title'] = search_result['title']
        result['artist'] = search_result['artists'][0]['name']
        result['year'] = search_result['year']
        result['playlist_id'] = search_result['playlistId']
        results.append(result)
    print(results)

if __name__=="__main__":
    search_artist_album("weezer", "pinkerton")