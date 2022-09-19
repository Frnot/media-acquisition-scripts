# v2.0

import os
import re

import music_tag

regex_list = [
    re.compile(r"\s*[({\[]explicit[)}\]]", re.IGNORECASE),  # explicit
    re.compile(r"\s*[({\[]\s*\d*\s*re[-]*master[ed]*\s*\d*\s*[)}\]]", re.IGNORECASE),  # remastered
    re.compile(r"\s*[({\[]\s*album\s+version\s*[)}\]]", re.IGNORECASE)  # "album version"
]


def update_dir(dir_path, dry_run=False):
    root, dir = os.path.split(dir_path)
    for file in os.listdir(dir_path):
        filepath = os.path.join(root, file)
        update(filepath, dry_run)

    # Check directory names
    old_dirname = dirname = dir
    if dirname := clean(dirname):
        print(f"Old directory name: \"{old_dirname}\" ||| New directory name: \"{dirname}\"")
        if not dry_run:
            new_dirpath = os.path.join(root, dirname)
            os.rename(dir_path, new_dirpath)


def update(filepath, dry_run=False):
    root,file = os.path.split(filepath)
    try:
        ftag = music_tag.load_file(filepath)
        save_tags = False
    except KeyboardInterrupt:
        print("Exiting")
        quit()
    except:
        return None
    
    # Check title
    original_title = title = ftag['title'].value
    if title := clean(title):
        ftag['title'] = title
        save_tags = True

    # Check Album tag
    album = ftag['album'].value
    if album := clean(album):
        ftag['album'] = album
        save_tags = True

    # Save tags if somethign has changed
    if save_tags:
        print(f"Old title: \"{original_title}\" ||| New title: \"{title}\"")
        print(filepath)
        filetagcount += 1
        if not dry_run:
            ftag.save()
        
    # Check filename
    old_filename = filename = file
    if filename := clean(filename):
        print(f"Old filename: \"{old_filename}\" ||| New filename: \"{filename}\"")
        if not dry_run:
            new_filepath = os.path.join(root, filename)
            os.rename(filepath, new_filepath)


def clean(string):
    hits = 0
    for regex in regex_list:
        string, hit = regex.subn("", string)
        hits += hit

    return string.strip() if hits else None
