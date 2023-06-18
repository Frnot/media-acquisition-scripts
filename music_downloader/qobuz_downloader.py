import logging
from qobuz_dl.core import QobuzDL
from qobuz_dl.utils import create_and_return_dir
from dotenv import dotenv_values, set_key
import re
from rapidfuzz import fuzz

logging.basicConfig(level=logging.INFO)

env = dotenv_values(".env")
email = env["email"]
password = env["password"]

qobuz = QobuzDL(directory=r"c:\Users\Frnot\Desktop\qobuzdownloads",
                folder_format="{year} - {album}",
                track_format="{tracknumber} - {tracktitle}",
                embed_art=True,
                overwrite=True,
                quality=5)

qobuz.get_tokens() # get 'app_id' and 'secrets' attrs
qobuz.initialize_client(email, password, qobuz.app_id, qobuz.secrets)

#qobuz.handle_url("https://play.qobuz.com/album/l172xgk2w8vpb")

query = "The playas manual"


def download_album(album_name, artist, dl_path):
    query = f"{artist} - {album_name}"
    search_results = qobuz.search_by_type(query, "album", limit=5)
    print(f"{search_results=}")

    url = None
    for result in search_results:
        trimmed_result = re.search(r"(.*) - \d\d:\d\d:\d\d", result['text']).group(1)
        if fuzz.ratio(trimmed_result.lower(), query.lower()) > 90:
            url = search_results[0]['url']
            break
    else:
        print(f"Didn't find a good match for query '{query}'")
        return False

    qobuz.directory = create_and_return_dir(dl_path)
    qobuz.handle_url(url)


def download_track(track_name, artist, dl_path):
    query = f"{artist} - {track_name}"
    search_results = qobuz.search_by_type(query, "track", limit=5)
    print(f"{search_results=}")

    url = None
    for result in search_results:
        trimmed_result = re.search(r"(.*) - \d\d:\d\d:\d\d", result['text']).group(1)
        if fuzz.ratio(trimmed_result.lower(), query.lower()) > 90:
            url = search_results[0]['url']
            break
    else:
        print(f"Didn't find a good match for query '{query}'")
        return False
    
    qobuz.directory = create_and_return_dir(dl_path)
    qobuz.handle_url(url)


#download_album("the playas manual", "ramirez", r"C:\Users\Frnot\Downloads")
download_track("Gold Thangs & Pinky Rangs (Da Hooptie)", "ramirez", r"C:\Users\Frnot\Downloads")