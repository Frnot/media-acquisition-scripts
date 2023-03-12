"""loads data from billbaord scraper and downloads it form tidal"""

import os
import re
import shelve
from time import perf_counter as time

from fuzzywuzzy import fuzz
import tidal_downloader
import tidal_dl

from fix_music_tags import update_dir

media_dir = r"V:\media\audio\Music"
dest_dir = r"V:\media\audio\Music\Pop"

def main():
    tracks_to_get = get_new_tracklist()
    existing_artists = generate_artist_list()

    #tracks_to_get = {}
    #tracks_to_get["Fetty Wap"] = ['679']#, 'I Feel It Coming', 'In The Night', 'The Hills', 'Blinding Lights', 'Die For You', 'Starboy', 'Sacrifice', 'Earned It (Fifty Shades Of Grey)']

    #download(str(track.album.id), download_dir)

    errored_tracks = []

    for artist, tracks in tracks_to_get.items():
        download_dir = None

        # dont download tracks that already exist
        """
        if artist.lower() in existing_artists:
            # get all files under artist dir
            existing_tracks = []
            for r, d, f in os.walk(existing_artists[artist.lower()]):
                existing_tracks.extend(f)

            # clean up filenames
            for idx, track in enumerate(existing_tracks):
                existing_tracks[idx] = ".".join(track.split(".")[:-1]).split(" - ")[-1]

            # remove duplicates from tracks to get
            for track in tracks:
                if track in existing_tracks: #TODO: fuzz this if needed
                    tracks.remove(track)
        """


        # build list of albums to get by searching tidal for track name
        # remove duplicate albums (multiple tracks in same album)
        albums = {}
        for track in tracks.copy():
            try:
                album = tidal_downloader.search(track, artist).album
                albums[album.title] = (album, track)
                print(f"album: {album.title} | {track}")
            except AttributeError as e:
                print(f"Error when searching for {track} {artist} | {e}")
                errored_tracks.append(f"{track} {artist}")
                tracks.remove(track)
                continue
            
        if not tracks:
            print("\nAll tracks for artist errored out.\n")


        # remove duplicate albums (ones we already have)
        if artist.lower() in existing_artists:
            print(f"\nAlready have music by artist: {artist}")
            download_dir = existing_artists[artist.lower()]
            existing_albums = [a.split(" - ")[-1].lower() for a in os.listdir(download_dir)]
            
            for album_to_get in list(albums.keys()):
                scrubbed_album_to_get = re.sub("\s?[\(\[].*?[\)\]]\s?", " ", album_to_get)
                for existing_album in existing_albums:
                    match_ratio = fuzz.partial_ratio(scrubbed_album_to_get.lower(), existing_album)
                    if match_ratio >= 90:
                        print(f"Found existing album: {artist} - {album_to_get}")
                        del albums[album_to_get]
                        break

        if not albums:
            print(f"\nSkipping artist {artist}. already downloaded")
            continue


        print(f"\nWill download the following album(s) by '{artist}'")
        for album, track in albums.values():
            print(f"{album.title} | {track}")
        #choice = input("Hit enter to continue or any key to skip: ")
        #if choice != "":
        #    continue
        else:
            if not download_dir:
                download_dir = os.path.join(dest_dir, artist)
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)

            for album, track in albums.values():
                dlpath = tidal_downloader.download_album(album, download_dir)
                if dlpath:
                    print(f"\nDownloaded {album} to {dlpath}")
                    update_dir(dlpath)

        




def get_new_tracklist():
    """get list of tracks to get"""
    track_dict = {}

    filename = "billboard_top40"
    with shelve.open(os.path.join("music_downloader\data", filename)) as db:
        try:
            date = db["date"]
            tracks = db["tracks"]
        except KeyError:
            pass
    #sorted_tracks = sorted(tracks, key=lambda e: e[1])

    for track, artist in tracks:
        artist = artist.split(" Featuring")[0] # remove featured artists from entry
        if artist in track_dict:
            track_dict[artist].append(track)
        else:
            track_dict[artist] = [track]

    sorted_tracks = set()
    for artist, tracks in track_dict.items():
        sorted_tracks.add((artist, ", ".join(tracks)))

    sorted_tracks = sorted(sorted_tracks, key=lambda e: e[0])

    return track_dict



def generate_artist_list():
    root = os.path.normpath(media_dir)

    artist_list = {}
    for genre in os.listdir(root):
        for artist in os.listdir(os.path.join(root, genre)):
            artist_list[artist.lower()] = os.path.join(root, genre, artist)
            
    return artist_list




if __name__ == "__main__":
    main()