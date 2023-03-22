import os

from fuzzywuzzy import fuzz

from fix_music_tags import scrub_filename


def find_existing_artists(media_dir):
    """Returns a list of all artists in media dir.\n
    Assumes second level of dir hierarchy is organized by artist"""
    root = os.path.normpath(media_dir)

    artist_list = {}
    for genre in os.listdir(root):
        for artist in os.listdir(os.path.join(root, genre)):
            artist_list[artist.lower()] = os.path.join(root, genre, artist)
            
    return artist_list


def find_existing_tracks(dir):
    existing_tracks = []
    for r, d, f in os.walk(dir):
        existing_tracks.extend(f)
    
    return existing_tracks


def subtract_existing_tracks(tracks_to_check, existing_tracks):
    """Returns tracks in tracks_to_check that do not exist in existing_tracks (fuzzy match)"""
    scrubbed_tracks_to_check = [(scrub_filename(t),t) for t in tracks_to_check]
    scrubbed_existing_tracks = [scrub_filename(t) for t in existing_tracks]

    missing_tracks = tracks_to_check.copy()
    for track, original_track in scrubbed_tracks_to_check:
        for existing_track in scrubbed_existing_tracks:
            if track in existing_track or fuzz.ratio(track, existing_track) > 90:
                missing_tracks.remove(original_track)
                break

    return missing_tracks
