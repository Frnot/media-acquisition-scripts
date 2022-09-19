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

TOKEN.read("/root/.tidal-dl.token.json")
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
