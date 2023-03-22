# v1.0

from fuzzywuzzy import process
import re

from tidal_dl.events import *
from tidal_dl.settings import *
import tidal_dl.model


SETTINGS.audioQuality = AudioQuality.HiFi
SETTINGS.albumFolderFormat = R"{AlbumYear} - {AlbumTitle}"
SETTINGS.trackFileFormat = R"{TrackNumber} - {TrackTitle}"
SETTINGS.apiKeyIndex = 4
SETTINGS.checkExist = True
SETTINGS.includeEP = True
SETTINGS.saveCovers = False
SETTINGS.lyricFile = False
SETTINGS.showProgress = False
SETTINGS.showTrackInfo = False
SETTINGS.saveAlbumInfo = False
SETTINGS.usePlaylistFolder = False
SETTINGS.multiThread = True

TOKEN.read(getTokenPath())
test = TIDAL_API.apiKey = apiKey.getItem(SETTINGS.apiKeyIndex)

if not loginByConfig():
    loginByWeb()


def download(id, download_dir, dry_run=False):
    SETTINGS.downloadPath = download_dir
    try:
        etype, obj = TIDAL_API.getByString(id)
    except Exception as e:
        Printf.err(str(e) + " [" + id + "]")
        return

    try:
        album = obj if etype == Type.Album else TIDAL_API.getAlbum(obj.album.id)
        path = getAlbumPath(album)
    except Exception as e:
        Printf.err(str(e))
        return

    if not dry_run:
        try:
            start_type(etype, obj)
        except Exception as e:
            Printf.err(str(e))
            return

    return path


def download_album(album: tidal_dl.model.Album, download_dir, dry_run=False):
    SETTINGS.downloadPath = download_dir
    album = TIDAL_API.getAlbum(album.id)

    try:
        path = getAlbumPath(album)
    except Exception as e:
        Printf.err(str(e))
        return

    if not dry_run:
        try:
            start_album(album)
        except Exception as e:
            Printf.err(str(e))
            return
        
    return path



forbidden_search_terms = [
    "soundtrack",
    "best of",
    "karaoke",
    "acoustic",
    "remix",
    "now that's what i call music",
    "hits",
]

forbidden_regex = [
    re.compile(r"[\s({\[]*live([)}\]]|\s+|$)", re.IGNORECASE),  # live or (live) but not lives
]

def search(track, artist):
    """dont return remixes or singles that have albums"""

    search_string = f"{track} {artist}"
    while True:
        results = TIDAL_API.search(text=search_string, type=Type.Track).tracks.items

        best_candidate = None
        for track in results:
            normalized_track_title = track.title.lower()
            normalized_album_title = track.album.title.lower()

            forbidden_match = False
            for term in forbidden_search_terms:
                if term in normalized_track_title or term in normalized_album_title:
                    forbidden_match = True
                    break
            if forbidden_match:
                continue

            for regex in forbidden_regex:
                if regex.search(track.title):
                    forbidden_match = True
                    break
            if forbidden_match:
                continue

            if track.artist:
                if artist.lower() not in track.artist.name.lower():
                    continue
            else:
                if artist.lower() not in [a.name.lower() for a in track.artists]:
                    continue

            if track.version is not None:
                match, ratio = process.extractOne(track.version, ("Original Version", "Album Version", "Single Version"))
                if ratio < 90:
                    continue
            
            album = TIDAL_API.getAlbum(track.album.id)
            if album.artist.name == 'Various Artists':
                continue
            if album.artist and album.artist.name != artist:
                continue

            best_candidate = track

            if album.type == "SINGLE":
                continue

            return track
        else:
            if not best_candidate and re.search(r"\s?[\(\[].*?[\)\]]\s?", search_string):
                search_string = re.sub(r"\s?[\(\[].*?[\)\]]\s?", " ", search_string) # remove parantheses from search string
                continue
            return best_candidate
