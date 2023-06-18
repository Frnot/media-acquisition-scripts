# an attempt to update the entire library with lossless version from qobuz


from dotenv import dotenv_values
import music_tag
import os
from qobuz_downloader import download_album


#TODO: logs
# if new directory is created
# if a folder was skipped
# if qobuz doesnt find a match
# if only some files are tidalsource

env = dotenv_values(".env")
working_dir = env["dir"]


def main():
    for artist_dir in [os.path.join(working_dir,d) for d in os.listdir(working_dir) if os.path.isdir(os.path.join(working_dir,d))]: # absolute aids
        for album_dir in [os.path.join(artist_dir,d) for d in os.listdir(artist_dir) if os.path.isdir(os.path.join(artist_dir,d))]:

            files = [os.path.join(album_dir,f) for f in os.listdir(album_dir) if os.path.isfile(os.path.join(album_dir,f))]

            tracks = [MusicTrack(file) for file in files if file.endswith(".flac")]

            if (all([not track.tidalsource for track in tracks])
            and all(track.album == tracks[0].album for track in tracks)):
                # log error
                continue
            
            album = tracks[0].album
            artist = tracks[0].artist
            download_album(album, artist, artist_dir)
            print()

            


class MusicTrack:
    def __init__(self, filepath):
        ftag = music_tag.load_file(filepath)
        self.flac = filepath.endswith(".flac")
        self.album = ftag["album"].value
        self.artist = ftag["artist"].value
        self.tidalsource = ftag["comment"].value[:11] == "tidalsource"
        self.true=True



if __name__ == "__main__":
    main()