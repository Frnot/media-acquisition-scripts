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

# TODO check if there are duplicate files in an album (filename changed and didnt overwite existing)

env = dotenv_values(".env")
working_dir = env["dir"]

errorfile = "tagerror.txt"


def main():
    for artist_dir in [os.path.join(working_dir,d) for d in os.listdir(working_dir) if os.path.isdir(os.path.join(working_dir,d))]: # absolute aids
        for album_dir in [os.path.join(artist_dir,d) for d in os.listdir(artist_dir) if os.path.isdir(os.path.join(artist_dir,d))]:

            files = [os.path.join(album_dir,f) for f in os.listdir(album_dir) if os.path.isfile(os.path.join(album_dir,f))]

            tracks = [MusicTrack(file) for file in files if file.endswith(".flac")]

            if (not any([track.tidalsource for track in tracks])
            and all(track.album == tracks[0].album for track in tracks)):
                # log error
                continue

            #initial artist count:
            artist_count = {}
            for track in tracks:
                artist_count[track.ftag["tracknumber"].value] = track.ftag["artist"].values

            
            album = tracks[0].album
            artist = tracks[0].artist
            if not download_album(album, artist, artist_dir):
                continue


            # cleanup old files
            files = [os.path.join(album_dir,f) for f in os.listdir(album_dir) if os.path.isfile(os.path.join(album_dir,f))]
            tracks = [MusicTrack(file) for file in files if file.endswith(".flac")]
            for i in range(len(tracks)):
                for j in range(i+1, len(tracks)):
                    if tracks[i].tracknumber == tracks[j].tracknumber:
                        print(f"duplicate files: {tracks[i].title} | {tracks[j].title}")
                        try:
                            if tracks[i].tidalsource:
                                print(f"deleting file: {tracks[i].filepath}")
                                os.remove(tracks[i].filepath)
                                break
                            else:
                                print(f"deleting file: {tracks[j].filepath}")
                                os.remove(tracks[j].filepath)
                        except FileNotFoundError:
                            pass


            # new artist count
            files = [os.path.join(album_dir,f) for f in os.listdir(album_dir) if os.path.isfile(os.path.join(album_dir,f))]
            for track in [MusicTrack(file) for file in files if file.endswith(".flac")]:
                try:
                    if len(artist_count[track.tracknumber]) != len(track.ftag["artist"].values):
                        with open(errorfile, "a+") as file:
                            msg = f"mismatch artist count: {track.filepath} | before: {artist_count[track.tracknumber]} | after: {track.ftag['artist'].values}"
                            print(msg)
                            try:
                                file.write(msg+"\n")
                            except UnicodeEncodeError:
                                pass
                except KeyError:
                    pass

            


class MusicTrack:
    def __init__(self, filepath):
        self.filepath = filepath
        self.ftag = music_tag.load_file(filepath)
        self.flac = filepath.endswith(".flac")
        self.album = self.ftag["album"].value
        self.artist = self.ftag["artist"].value
        self.title = self.ftag["title"].value
        self.tracknumber = self.ftag["tracknumber"].value
        self.tidalsource = self.ftag["comment"].value[:11] == "tidalsource"



if __name__ == "__main__":
    main()