# v1.0

import re

from tidal_dl.events import *
from tidal_dl.settings import *


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


def search(track, artist):
    """dont return remixes or singles that have albums"""

    search_string = f"{track} {artist}"
    while True:
        results = TIDAL_API.search(text=search_string, type=Type.Track).tracks.items

        best_candidate = None
        for track in results:
            if "karaoke" in track.album.title.lower():
                continue
            if "hits" in track.album.title.lower() and "hits" not in track.title.lower():
                continue

            if track.artist:
                if artist.lower() not in track.artist.name.lower():
                    continue
            else:
                if artist.lower() not in [a.name.lower() for a in track.artists]:
                    continue

            if track.version is not None and track.version not in ("Original Version", "Album Version"):
                continue
            else:
                best_candidate = track

            if track.title.lower() == track.album.title.lower():
                album = TIDAL_API.getAlbum(track.album.id)
                if album.type == "SINGLE":
                    continue
            return track
        else:
            if not best_candidate and re.search("\s?[\(\[].*?[\)\]]\s?", search_string):
                search_string = re.sub("\s?[\(\[].*?[\)\]]\s?", " ", search_string) # remove parantheses from search string
                continue
            return best_candidate
