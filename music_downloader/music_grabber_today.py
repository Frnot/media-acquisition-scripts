"""loads data from billbaord scraper and downloads it form tidal"""

import os
import time

from fuzzywuzzy import fuzz

import tidal_downloader
from billboard_scraper import top_40_no_country, group_by_artist
from fix_music_tags import update_dir, scrub_filename
from local_file_utils import find_existing_artists, find_existing_tracks, subtract_existing_tracks

media_dir = r"V:\media\audio\Music"
dest_dir = r"V:\media\audio\Music\Pop"

def main():
    tracks_to_get = group_by_artist(top_40_no_country())
    existing_artists = find_existing_artists(media_dir)

    errored_tracks = []

    for artist, tracks in tracks_to_get.items():
        raw_tracks = tracks # for debug
        download_dir = None

        print(f"\nSearching for tracks by {artist}")

        # dont download tracks that already exist
        if artist.lower() in existing_artists:
            tracks = subtract_existing_tracks(tracks, find_existing_tracks(existing_artists[artist.lower()]))

        if not tracks:
            print(f"\nAlready have every track for artist {artist}")
            continue

        # build list of albums to get by searching tidal for track name
        # remove duplicate albums (multiple tracks in same album)
        albums = {}
        for track in tracks.copy():
            try:
                album = tidal_downloader.search(track, artist).album
                if album.title in albums.keys():
                    albums[album.title][1].append(track)
                else:
                    albums[album.title] = (album, [track])
                print(f"album: {album.title} | {track}")
            except AttributeError as e:
                print(f"Error when searching for {track} {artist} | {e}")
                errored_tracks.append(f"{track} {artist}")
                tracks.remove(track)
                continue
            
        if not tracks:
            print("\nAll tracks for artist errored out.\n")
            continue

        # remove duplicate albums (ones we already have)
        if artist.lower() in existing_artists:
            download_dir = existing_artists[artist.lower()]
            print(f"\nAlready have music by artist: {artist} | ({download_dir})")
            existing_albums = [scrub_filename(a) for a in os.listdir(download_dir)]
            
            for album_to_get in list(albums.keys()):
                scrubbed_album_to_get = scrub_filename(album_to_get)
                for existing_album in existing_albums:
                    match_ratio = fuzz.ratio(scrubbed_album_to_get, existing_album)
                    if match_ratio >= 90:
                        print(f"Found existing album: {artist} - {scrubbed_album_to_get} ({album_to_get})")
                        del albums[album_to_get]
                        break

        if not albums:
            print(f"\nSkipping artist {artist}. already downloaded\n\n")
            continue


        print(f"\nWill download the following album(s) by '{artist}'")
        for album, tracks in albums.values():
            print(f"{album.title} | {tracks}")
        #choice = input("Hit enter to continue or any key to skip: ")
        #if choice != "":
        #    continue
        else:
            if not download_dir:
                download_dir = os.path.join(dest_dir, artist)
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)
                time.sleep(1)

            for album, tracks in albums.values():
                if ttg := subtract_existing_tracks(tracks, find_existing_tracks(download_dir)):
                    print(f"Downloading album {album} because we dont have song(s) {ttg}")
                    dlpath = tidal_downloader.download_album(album, download_dir)
                    if dlpath:
                        print(f"\nDownloaded {album} to {dlpath}")
                        update_dir(dlpath)
                else:
                    print(f"Not downloading {album} for {track} because a recently downloaded album included it")


if __name__ == "__main__":
    main()
