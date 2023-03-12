"""loads data from billbaord scraper and downloads it form tidal"""

import os
import shelve
from time import perf_counter as time

import fuzzywuzzy
import tidal_downloader

media_dir = r"V:\media\audio\Music"

def main():
    tracks_to_get = get_new_tracklist()
    existing_artists = generate_artist_list()

    #download(str(track.album.id), download_dir)


    for artist, tracks in tracks_to_get.items():
    
        # dont download tracks that already exist
        if artist in existing_artists:
            #get albums we have
            #existing_albums = [a.split(" - ")[1] for a in os.listdir(existing_artists[artist])]

            # get all files under artist dir
            existing_tracks = []
            for r, d, f in os.walk(existing_artists[artist]):
                existing_tracks.extend(f)

            # clean up filenames
            for idx, track in enumerate(existing_tracks):
                existing_tracks[idx] = ".".join(track.split(".")[:-1]).split(" - ")[-1]

            # remove duplicates from tracks to get
            for track in tracks:
                if track in existing_tracks: #TODO: fuzz this if needed
                    tracks.remove(track)


        # build list of albums to get by searching tidal for track name
        # remove duplicate albums (multiple tracks in same album)
        albums = {}
        for track in tracks:
            try:
                album = tidal_downloader.search(track, artist).album
            except AttributeError:
                print(f"Error when searching for {track} {artist}")
                raise AttributeError
            albums[album.title] = album
            print(f"album: {album.title} | {track}")


        # TODO: remove duplicate albums (ones we already have)

        
        print(albums)

        




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
            artist_list[artist] = os.path.join(root, genre, artist)
            
    return artist_list




if __name__ == "__main__":
    main()